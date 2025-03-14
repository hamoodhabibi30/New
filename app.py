from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Set your preferred Invidious instance
INVIDIOUS_INSTANCE = "https://inv.nadeko.net"

def fetch_live_streams():
    """Fetch YouTube live streams using Invidious API."""
    search_query = "gta rp on soulcity"
    search_url = f"{INVIDIOUS_INSTANCE}/api/v1/search?q={search_query}&type=video"

    try:
        response = requests.get(search_url)
        data = response.json()

        # Filter live streams only
        live_streams = [
            {
                "title": video.get("title"),
                "channel": video.get("author"),
                "url": f"https://www.youtube.com/watch?v={video.get('videoId')}",
                "thumbnail": video.get("videoThumbnails")[-1]["url"],
                "viewers": video.get("viewCount", "Unknown"),
            }
            for video in data if video.get("isLive")
        ]

        if not live_streams:
            return {"error": "No live streams found."}
        
        return live_streams

    except Exception as e:
        return {"error": f"Invidious API error: {str(e)}"}

@app.route("/api/live-streams")
def get_live_streams():
    live_streams = fetch_live_streams()
    return jsonify(live_streams)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
