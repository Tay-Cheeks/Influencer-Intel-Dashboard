"""
src/youtube/parser.py
Cleans YouTube inputs and extracts a usable identifier.

Outputs:
    (identifier, id_type)

Where id_type is one of:
- "handle"      -> identifier like "@somehandle"
- "channel_id"  -> identifier like "UCxxxxxxxxxxxxxxxxxxxxxx" (24 chars)
- "video_id"    -> identifier like "dQw4w9WgXcQ"
"""

from __future__ import annotations

import re
from typing import Tuple


# Common patterns
_CHANNEL_ID_RE = re.compile(r"^UC[a-zA-Z0-9_-]{22}$")  # UC + 22 chars = 24 total
_HANDLE_RE = re.compile(r"^@[\w.\-]{3,}$")  # simple handle validation
_YT_HOST_RE = re.compile(r"(?:https?://)?(?:www\.)?(?:youtube\.com|youtu\.be)/", re.I)

# URL patterns
_URL_HANDLE_RE = re.compile(r"youtube\.com/@(?P<handle>[\w.\-]+)", re.I)
_URL_CHANNEL_RE = re.compile(r"youtube\.com/channel/(?P<cid>UC[a-zA-Z0-9_-]{22})", re.I)
_URL_VIDEO_WATCH_RE = re.compile(r"youtube\.com/watch\?.*v=(?P<vid>[a-zA-Z0-9_-]{6,})", re.I)
_URL_VIDEO_SHORT_RE = re.compile(r"youtu\.be/(?P<vid>[a-zA-Z0-9_-]{6,})", re.I)
_URL_SHORTS_RE = re.compile(r"youtube\.com/shorts/(?P<vid>[a-zA-Z0-9_-]{6,})", re.I)


def extract_identifier(input_value: str) -> Tuple[str, str]:
    """
    Accepts:
    - @handle
    - handle without @ (we'll normalize to @handle)
    - UC channel id
    - youtube.com/@handle
    - youtube.com/channel/UC...
    - youtube.com/watch?v=VIDEO_ID
    - youtu.be/VIDEO_ID
    - youtube.com/shorts/VIDEO_ID
    - messy strings with trailing slashes/spaces

    Returns:
        (identifier, id_type)
    """
    if not input_value or not str(input_value).strip():
        return "@", "handle"

    s = str(input_value).strip()
    # Remove trailing slash
    s = s.rstrip("/")

    # 1) Raw channel ID
    if _CHANNEL_ID_RE.match(s):
        return s, "channel_id"

    # 2) Raw handle
    if s.startswith("@"):
        # normalize minimal
        handle = "@" + s[1:].strip()
        return handle, "handle"

    # 3) If it looks like a URL, try URL parses first
    if _YT_HOST_RE.search(s):
        m = _URL_CHANNEL_RE.search(s)
        if m:
            return m.group("cid"), "channel_id"

        m = _URL_HANDLE_RE.search(s)
        if m:
            return f"@{m.group('handle')}", "handle"

        m = _URL_SHORTS_RE.search(s)
        if m:
            return m.group("vid"), "video_id"

        m = _URL_VIDEO_SHORT_RE.search(s)
        if m:
            return m.group("vid"), "video_id"

        m = _URL_VIDEO_WATCH_RE.search(s)
        if m:
            return m.group("vid"), "video_id"

        # Could be /c/ or /user/ vanity URL; return as "handle" fallback,
        # but WITHOUT forcing @ so the client can try a search fallback.
        # Example: youtube.com/c/SomeName -> "SomeName"
        vanity = _extract_vanity_path(s)
        if vanity:
            return vanity, "vanity"

    # 4) Non-URL input: could be handle without @ or custom name.
    # If it looks like a handle, normalize to @handle
    if _HANDLE_RE.match(f"@{s}"):
        return f"@{s}", "handle"

    # 5) Fallback: treat as vanity (custom) name
    return s, "vanity"


def _extract_vanity_path(url: str) -> str | None:
    """
    Extracts the last path segment after /c/ or /user/ if present.
    """
    m = re.search(r"youtube\.com/(?:c|user)/(?P<name>[\w.\-]+)", url, re.I)
    if m:
        return m.group("name")
    return None
