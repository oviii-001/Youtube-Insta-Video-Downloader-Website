from flask import Flask, request, jsonify, render_template
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    quality = data.get('quality', 'best')  # Default to 'best' if not provided

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        # Set yt_dlp options with user-selected quality
        ydl_opts = {
            'format': quality,
            'outtmpl': '%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return jsonify({'message': f'Video downloaded in {quality} quality successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
