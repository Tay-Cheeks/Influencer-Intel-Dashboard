from __future__ import annotations

from typing import Any, Dict

from src.youtube.client import get_channel_stats, get_recent_videos
from src.metrics.metrics import InfluencerMetrics
from src.analysis.analyser import build_analysis


def run_youtube_analysis(youtube_input: str, video_count: int = 8) -> Dict[str, Any]:
    """
    End-to-end orchestrator for the YouTube analysis MVP.

    Input:
        youtube_input: channel URL / handle / channel ID / video URL
        video_count: number of recent uploads to analyze

    Output (JSON-friendly):
        {
          "channel": {...},
          "videos": [...],
          "metrics_report": {...},
          "analysis": {...}
        }
    """
    channel = get_channel_stats(youtube_input)
    if not channel:
        raise ValueError("Could not resolve a YouTube channel from the provided input.")

    videos = get_recent_videos(channel.get("uploads_playlist_id", ""), count=video_count)

    # Metrics layer (this produces the standardized keys our analyser expects)
    metrics = InfluencerMetrics(
        channel_name=channel.get("channel_name", ""),
        sub_count=int(channel.get("subscribers", 0)),
        video_data=videos,
        region=channel.get("region", "Global"),
        channel_url=channel.get("channel_url", ""),
    )
    report = metrics.get_performance_report()
    if not report:
        raise ValueError("No video data returned for this channel (or playlist is empty).")

    # Analysis layer (benchmarks + tiering)
    analysis = build_analysis(report)

    return {
        "channel": {
            "channel_id": channel.get("channel_id", ""),
            "channel_name": channel.get("channel_name", ""),
            "subscribers": int(channel.get("subscribers", 0)),
            "region": channel.get("region", "Global"),
            "channel_url": channel.get("channel_url", ""),
            "uploads_playlist_id": channel.get("uploads_playlist_id", ""),
        },
        "videos": videos,                 # raw list for frontend charting
        "metrics_report": report,         # computed rollups
        "analysis": analysis,             # benchmark comparisons + tiering
    }
