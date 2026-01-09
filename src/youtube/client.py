""" 
Fetches YouTube channel and video data via YouTube Data API v3.
"""
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
from .parser import extract_identifier

#Load API key from .env
load_dotenv()
YT_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not YT_API_KEY:
    raise ValueError("You must set YOUTUBE_API_KEY in your .env file")

#Create the YouTube API client
youtube = build("youtube", "v3", developerKey=YT_API_KEY)


def get_channel_stats(channel_input: str):
    """
    Retrieves subscriber count, region, and uploads playlist ID.
    
    Returns a dict:
    {
        "channel_name": str,
        "subscribers": int,
        "region": str,
        "uploads_playlist_id": str
    }
    Or None if API fails or channel not found
    """
    identifier, id_type = extract_identifier(channel_input)

    try:
        if id_type == "handle":
            request = youtube.channels().list(
                part="snippet,statistics,contentDetails",
                forHandle=identifier
            )
        else:  #Channel ID
            request = youtube.channels().list(
                part="snippet,statistics,contentDetails",
                id=identifier
            )

        response = request.execute()

        if not response.get("items"):
            return None

        item = response["items"][0]

        return {
            "channel_name": item["snippet"]["title"],
            "subscribers": int(item["statistics"]["subscriberCount"]),
            "region": item["snippet"].get("country", "Global"), #defaults to Global
            "uploads_playlist_id": item["contentDetails"]["relatedPlaylists"]["uploads"]
        }

    except Exception as e:
        print(f"[YouTube API Error] {e}")
        return None


def get_recent_videos(playlist_id: str, count: int = 8):
    """
    Fetches the most recent N videos from a playlist, along with views, likes, comments.
    
    Returns a list of dicts:
    [
        {"views": int, "likes": int, "comments": int},
        ...
    ]
    """
    try:
        #Step 1: Get video IDs from the uploads playlist
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=count
        )
        response = request.execute()

        video_ids = [item["contentDetails"]["videoId"] for item in response.get("items", [])]
        if not video_ids:
            return []

        #Step 2: Get video statistics
        stats_request = youtube.videos().list(
            part="statistics",
            id=",".join(video_ids)
        )
        stats_response = stats_request.execute()

        video_data = []
        for item in stats_response.get("items", []):
            stats = item["statistics"]
            video_data.append({
                "views": int(stats.get("viewCount", 0)),
                "likes": int(stats.get("likeCount", 0)),
                "comments": int(stats.get("commentCount", 0))
            })

        return video_data

    except Exception as e:
        print(f"[YouTube API Error] {e}")
        return []
