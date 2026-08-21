from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

def get_video_id(url):
    match = re.search(r'(?:v=|\/|embed\/|shorts\/)([0-9A-Za-z_-]{11})', url)
    return match.group(1) if match else None

@app.route('/download', methods=['POST'])
def get_download_link():
    data = request.json or {}
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({'error': 'URL enter karna zaroori hai!'}), 400

    video_id = get_video_id(video_url)
    if not video_id:
        return jsonify({'error': 'Ghalat YouTube URL. Sahi link enter karein.'}), 400

    # Reliable Open-Source Proxy Engine API
    cobalt_api_url = "https://co.wuk.sh/api/json"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    payload = {
        "url": video_url,
        "vQuality": "720"
    }

    try:
        response = requests.post(cobalt_api_url, json=payload, headers=headers, timeout=10)
        res_data = response.json()

        # Download URL Extraction
        download_link = res_data.get('url')
        
        if download_link:
            return jsonify({
                'title': f'YouTube Video ({video_id})',
                'download_url': download_link,
                'thumbnail': f'https://img.youtube.com/vi/{video_id}/hqdefault.jpg'
            })
        else:
            return jsonify({'error': 'Video extract nahi ho saki. Dusri video try karein.'}), 500

    except Exception as e:
        return jsonify({'error': f'Server Connection Error: {str(e)}'}), 500

# Vercel Serverless Function Entry Point
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
