from flask import Flask, render_template, request, jsonify
from chess_ai import get_ai_move
import os

# Khai báo rõ đường dẫn thư mục templates và static để Render không bị lỗi Not Found
template_dir = os.path.abspath('templates')
static_dir = os.path.abspath('static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_ai_move', methods=('GET', 'POST'))
def ai_move_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'})
    board = data.get('board')
    level = int(data.get('level', 2))
    castle = data.get('castle')
    ep = data.get('ep')
    
    move = get_ai_move(board, level, castle, ep)
    return jsonify(move)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
