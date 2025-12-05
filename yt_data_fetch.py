from googleapiclient.discovery import build
import pandas as pd
import isodate
from dateutil import parser

API_KEY = "[your API key]"
CHANNEL_ID = "[channel Id]"

youtube = build('youtube', 'v3', developerKey=API_KEY)

# 1)upload playlist
def get_uploads_playlist_id(channel_id):
    response = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()
    
    return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

# 2)videos from the uploaded playlist
def get_all_videos(playlist_id):
    videos = []
    next_page = None

    while True:
        response = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page
        ).execute()

        for item in response["items"]:
            videos.append({
                "video_id": item["snippet"]["resourceId"]["videoId"],
                "title": item["snippet"]["title"],
                "description": item["snippet"].get("description", ""),
                "published_at": item["snippet"]["publishedAt"],
            })

        next_page = response.get("nextPageToken")
        if next_page is None:
            break

    return pd.DataFrame(videos)

# 3)Adds statistics - views, likes, comments, duration
def add_video_stats(df):
    stats_list = []

    for i in range(0, len(df), 50):
        batch = df["video_id"][i:i+50].tolist()
        response = youtube.videos().list(
            part="statistics,contentDetails",
            id=",".join(batch)
        ).execute()

        for item in response["items"]:
            stats_list.append({
                "video_id": item["id"],
                "viewCount": int(item["statistics"].get("viewCount", 0)),
                "likeCount": int(item["statistics"].get("likeCount", 0)),
                "commentCount": int(item["statistics"].get("commentCount", 0)),
                "duration": isodate.parse_duration(item["contentDetails"]["duration"]).total_seconds(),
            })

    stats_df = pd.DataFrame(stats_list)
    return df.merge(stats_df, on="video_id")


if __name__ == "__main__":
    print("Fetching playlist ID...")
    playlist_id = get_uploads_playlist_id(CHANNEL_ID)

    print("Fetching videos...")
    df = get_all_videos(playlist_id)

    print("Fetching statistics...")
    df = add_video_stats(df)

    # Convert dates
    df["published_at"] = pd.to_datetime(df["published_at"])

    df.to_csv("youtube_videos.csv", index=False)
    print("Saved youtube_videos.csv successfully!")
    print("Total videos fetched:", len(df))
