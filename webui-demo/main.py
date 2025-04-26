from flask import Flask, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)  # Enable CORS for all routes

@app.route('/')
def serve_main_html():
    return send_from_directory('./web', 'main.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('./web', path)
