# src/analysis/benchmarks.py

BENCHMARK_TIERS = {
    "nano": {
        "subs_range": (1_000, 10_000),
        "engagement_rate": (4.0, 8.0),
        "loyalty_percent": (10, 25),
    },
    "micro": {
        "subs_range": (10_000, 100_000),
        "engagement_rate": (3.0, 6.0),
        "loyalty_percent": (8, 20),
    },
    "mid": {
        "subs_range": (100_000, 500_000),
        "engagement_rate": (2.0, 5.0),
        "loyalty_percent": (5, 15),
    },
    "macro": {
        "subs_range": (500_000, 10_000_000),
        "engagement_rate": (1.5, 4.0),
        "loyalty_percent": (3, 10),
    }
}

def get_creator_tier(subscribers: int):
    for tier, data in BENCHMARK_TIERS.items():
        low, high = data["subs_range"]
        if low <= subscribers < high:
            return tier
    return "macro"
