from flask import Flask, render_template, request, jsonify
from chess_ai import get_ai_move

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_ai_move', methods=['POST'])
def ai_move_endpoint():
    data = request.get_json()
    board = data.get('board')
    level = int(data.get('level', 2))
    castle = data.get('castle')
    ep = data.get('ep')
    
    move = get_ai_move(board, level, castle, ep)
    return jsonify(move)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
