from flask import Flask, jsonify
import subprocess
import json

app = Flask(__name__)

def fetch_live_streams():
    search_query = "gta rp on soulcity"  # Modify as needed
    yt_search_url = f"https://www.youtube.com/results?search_query={search_query}&sp=EgJAAQ%253D%253D"  # Filters for live videos

    try:
        # Run yt-dlp to fetch search results
        result = subprocess.run(
            ["yt-dlp", "-j", yt_search_url], capture_output=True, text=True
        )
        output_lines = result.stdout.strip().split("\n")

        # Extract live streams
        live_streams = []
        for line in output_lines:
            video_data = json.loads(line)
            if video_data.get("is_live"):
                live_streams.append({
                    "title": video_data.get("title"),
                    "channel": video_data.get("channel"),
                    "url": f"https://www.youtube.com/watch?v={video_data.get('id')}",
                    "thumbnail": video_data.get("thumbnail"),
                    "viewers": video_data.get("view_count", "Unknown"),
                })

        return live_streams

    except Exception as e:
        return {"error": str(e)}

@app.route("/api/live-streams")
def get_live_streams():
    live_streams = fetch_live_streams()
    return jsonify(live_streams)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
