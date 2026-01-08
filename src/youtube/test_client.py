from .client import get_channel_stats, get_recent_videos

channel = "@MrBeast"
stats = get_channel_stats(channel)
print(stats)

if stats:
    videos = get_recent_videos(stats["uploads_playlist_id"], count=5)
    print(videos)
