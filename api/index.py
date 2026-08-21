from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

def extract_video_id(url):
    import re
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url)
    return match.group(1) if match else None

@app.route('/download', methods=['POST'])
def get_download_link():
    data = request.json or {}
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({'error': 'URL is required'}), 400

    video_id = extract_video_id(video_url)
    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400

    # Cobalt / Public Engine API Endpoint
    try:
        api_res = requests.post(
            'https://api.cobalt.tools/api/json',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            json={'url': video_url}
        )
        res_data = api_res.json()

        if 'url' in res_data:
            return jsonify({
                'title': 'YouTube Video',
                'download_url': res_data['url'],
                'thumbnail': f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
            })
        else:
            return jsonify({'error': 'Unable to fetch stream from API'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def handler(event, context):
    return app(event, context)
