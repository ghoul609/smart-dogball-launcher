#!/usr/bin/env python3

from flask import Flask, request, jsonify, Response, render_template
from flask import send_from_directory
import os
from launcher import launchBall
from camera import robust_camera_feed
from sql_connector import fetch_data, insert_data

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'html'), 'index.html')

@app.route('/logo.jpeg')
def logo():
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'html'), 'logo.jpeg')

@app.route('/launch')
def launch():
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'html'), 'launcher.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(robust_camera_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/statistics')
def statistics():
    try:
        records = fetch_data()
        if not records:
            records =  []
        return render_template('statistics.html', records=records)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/launch', methods=['POST'])
def launch_api():
    data = request.get_json(silent=True)
    if not data or 'speed' not in data:
        return jsonify({'error': 'Missing or invalid speed value'}), 400
    speed = data.get('speed')
    try:
        launchBall(TARGET_SPEED=speed)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({'status': 'launched', 'speed': speed}), 200

@app.route('/api/database', methods=['GET','POST'])
def database():
    if request.method == 'GET':
        return jsonify(fetch_data()), 200
    if request.method == 'POST':
        data = request.get_json(silent=True)
        print(data)
        if not data or 'speed' not in data:
            return jsonify({'error': 'Missing or invalid speed value'}), 400
        speed = data.get('speed')
        launched = data.get('launched')
        try:
            insert_data(speed_value=speed, launched=launched)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        return jsonify({'status': 'inserted', 'speed': speed}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
