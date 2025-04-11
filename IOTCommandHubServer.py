import os
import subprocess
import time
from datetime import datetime
from flask import Flask, request, jsonify, Response,Request
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

log_messages = []

def log(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_msg = f"[{timestamp}] {msg}"
    log_messages.append(full_msg)
    print(full_msg)


@app.route('/save_note', methods=['POST'])
def save_note():
    data = request.get_json()
    content = data.get('content', '')
    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    filename = f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join(desktop_path, filename)

    try:
        with open(filepath, 'w') as f:
            f.write(content)
        log(f"Note saved to {filename}")
        return jsonify({'status': f'Note saved as {filename} on Desktop'})
    except Exception as e:
        log(f"Error saving note: {str(e)}")
        return jsonify({'status': f'Error: {str(e)}'}), 500
    

@app.route('/launch_ide', methods=['POST'])
def launch_ide():
    data = request.get_json()
    ide = data.get('ide','msvs')
    try:
        if ide == 'vscode':
            subprocess.Popen(["C:\\Users\\bbdnet2864\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"])
        elif ide == 'pycharm':
            subprocess.Popen(["C:\\Program Files\\JetBrains\\PyCharm Community Edition 2024.3\\bin\\pycharm64.exe"])
        elif ide == 'msvs':
            subprocess.Popen(["C:\\Program Files\\Microsoft Visual Studio\\2022\\Professional\\Common7\\IDE\\devenv.exe"])
        else:
            raise ValueError("Unknown IDE")
        log(f"{ide.upper()} launched via web trigger.")
        return jsonify({'status': f'{ide.upper()} launched'})
    except Exception as e:
        log(f"Failed to launch IDE: {str(e)}")
        return jsonify({'status': f'Error: {str(e)}'}), 500


@app.route('/logs')
def stream_logs():
    def event_stream():
        last_index = 0
        while True:
            time.sleep(1)
            if last_index < len(log_messages):
                for msg in log_messages[last_index:]:
                    yield f"data: {msg}\n\n"
                last_index = len(log_messages)
    return Response(event_stream(), mimetype="text/event-stream")




# For standalone test
if __name__ == "__main__":
    log("Starting Flask app")
    log("Flask app started")
    log("Server is running...")
    app.run(host='0.0.0.0', port=5000)
    log("Flask app stopped")
    
    