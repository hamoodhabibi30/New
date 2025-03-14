from flask import Flask, jsonify
import subprocess
import json
import requests
import random

app = Flask(__name__)

# Free Proxy API (Fetches fresh proxies)
PROXY_API = "https://www.proxy-list.download/api/v1/get?type=http"

def get_free_proxy():
    """Fetch a free proxy from the online list."""
    try:
        response = requests.get(PROXY_API)
        proxy_list = response.text.strip().split("\r\n")

        # Randomly choose a proxy
        if proxy_list:
            return random.choice(proxy_list)
    except Exception as e:
        print("Error fetching proxy:", e)
    return None

def fetch_live_streams():
    search_query = "gta rp on soulcity"
    yt_search_url = f"https://www.youtube.com/results?search_query={search_query}&sp=EgJAAQ%253D%253D"

    proxy = get_free_proxy()  # Get a free proxy
    print(f"Using Proxy: {proxy}")

    try:
        command = ["yt-dlp", "-j", yt_search_url]

        if proxy:
            command.insert(1, "--proxy")
            command.insert(2, f"http://{proxy}")  # Format proxy correctly

        result = subprocess.run(command, capture_output=True, text=True)

        print("Raw yt-dlp Output:", result.stdout)  # Debugging Output

        if not result.stdout.strip():
            return {"error": "yt-dlp returned no results. YouTube might be blocking requests."}

        output_lines = result.stdout.strip().split("\n")
        live_streams = []

        for line in output_lines:
            try:
                video_data = json.loads(line)
                if video_data.get("is_live"):
                    live_streams.append({
                        "title": video_data.get("title"),
                        "channel": video_data.get("channel"),
                        "url": f"https://www.youtube.com/watch?v={video_data.get('id')}",
                        "thumbnail": video_data.get("thumbnail"),
                        "viewers": video_data.get("view_count", "Unknown"),
                    })
            except json.JSONDecodeError as e:
                print("JSON Decode Error:", e)

        if not live_streams:
            return {"error": "No live streams found."}

        return live_streams

    except Exception as e:
        return {"error": f"yt-dlp error: {str(e)}"}

@app.route("/api/live-streams")
def get_live_streams():
    live_streams = fetch_live_streams()
    return jsonify(live_streams)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
