from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

# GitHub JSON URL
GITHUB_JSON_URL = "https://raw.githubusercontent.com/autonomus-optimus/testfile123/main/liveurl.json"

@app.route('/')
def index():
    # Serve the index.html file
    return render_template('index.html')

@app.route('/get-video-url', methods=['GET'])
def get_video_url():
    try:
        # Fetch the JSON file from GitHub
        response = requests.get(GITHUB_JSON_URL)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # Extract video URLs and isEnabled flag
        live_url = data.get("liveurl")
        default_url = data.get("defaulturl")
        is_enabled = data.get("isEnabled", False)

        # Determine the video URL to return
        video_url = live_url if is_enabled else default_url

        return jsonify({"videoUrl": video_url}), 200

    except requests.exceptions.RequestException as e:
        # Handle network or HTTP errors
        return jsonify({"error": "Failed to fetch video URL", "details": str(e)}), 500
    except ValueError as e:
        # Handle JSON parsing errors
        return jsonify({"error": "Invalid JSON response", "details": str(e)}), 500

if __name__ == '__main__':
    app.run()