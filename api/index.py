from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def get_download_link():
    data = request.json or {}
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({'error': 'URL is required'}), 400

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        # YouTube Bot Block bypass karne ke liye iOS/Android client parameters:
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android']
            }
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({
                'title': info.get('title'),
                'download_url': info.get('url'),
                'thumbnail': info.get('thumbnail')
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel Serverless Function Handle
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
