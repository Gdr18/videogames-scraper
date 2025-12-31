from flask import Flask, render_template, request, jsonify, send_file
from config import CONFIG

from src.scraper import get_data
from src.post_videogame import post_game
from src.json_maker import create_json
from src.platform_enum import PlatformScrapperEnum

def create_app(config: dict) -> Flask:
    application = Flask(__name__)
    application.config.from_object(config)
    return application

app = create_app(CONFIG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search/<int:page>', methods=['POST'])
def search(page):
    platform = request.form.get('platform', '')
    direction = request.form.get('direction', '')
    
    if (not platform) or (platform.replace("-", "_").upper() not in [platform.name for platform in PlatformScrapperEnum]):
        return render_template('index.html', error="Por favor selecciona una plataforma")
    
    page -= 1
    
    if direction:
        page += 1 if direction == 'next' else -1
    
    data = get_data(platform, page)
    
    return render_template('results.html', platform=platform, data=data, page=page + 1)

@app.route('/download', methods=['POST'])
def download_json():
    data = request.get_json()
    
    if not data or 'data' not in data:
        return jsonify({"error": "No hay datos para descargar"}), 400
    
    filepath, filename = create_json(data['data'])
    
    return send_file(filepath, as_attachment=True, download_name=filename)

@app.route('/send-db', methods=['POST'])
def send_data():
    data = request.get_json()
    
    if not data or 'data' not in data:
        return jsonify({"error": "No hay datos para enviar"}), 400
    
    games = data['data']
    success_count = 0
    
    try:
        for game in games:
            result = post_game(game)
            if result == "success":
                success_count += 1
        
        return jsonify({
            "success": True,
            "message": f"Se enviaron {success_count} registros a la base de datos"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
