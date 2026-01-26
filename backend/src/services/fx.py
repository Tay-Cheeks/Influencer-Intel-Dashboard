from __future__ import annotations

import time
from typing import Dict, List, Optional, Tuple

import requests

# Simple in-memory cache (good for MVP)
_CACHE: Dict[Tuple[str, str], Dict] = {}
_CACHE_EXPIRY_SECONDS = 10 * 60  # 10 minutes


class FXError(Exception):
    pass


def get_fx_rates(
    base: str = "USD",
    symbols: Optional[List[str]] = None,
) -> Dict:
    """
    Fetch FX rates (cached) from Frankfurter (ECB reference rates).
    Returns JSON-friendly dict:
      {
        "base": "USD",
        "date": "2026-01-26",
        "rates": {"ZAR": 18.5, "EUR": 0.92},
        "provider": "frankfurter.app",
        "cached": true/false
      }
    """
    base = (base or "USD").upper().strip()

    if symbols is None or len(symbols) == 0:
        symbols = ["ZAR", "EUR", "GBP"]
    symbols = [s.upper().strip() for s in symbols if s and s.strip()]

    # cache key includes base + sorted symbols
    symbols_key = ",".join(sorted(symbols))
    cache_key = (base, symbols_key)

    now = time.time()
    cached = _CACHE.get(cache_key)
    if cached and (now - cached["ts"] < _CACHE_EXPIRY_SECONDS):
        payload = dict(cached["data"])
        payload["cached"] = True
        return payload

    # Frankfurter endpoint
    url = "https://api.frankfurter.app/latest"
    params = {"base": base, "symbols": symbols_key}

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        raise FXError(f"Failed to fetch FX rates: {e}")

    payload = {
        "base": data.get("base", base),
        "date": data.get("date"),
        "rates": data.get("rates", {}),
        "provider": "frankfurter.app",
        "cached": False,
    }

    _CACHE[cache_key] = {"ts": now, "data": payload}
    return payload
