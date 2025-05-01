from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

# Game state
board = [[None for _ in range(3)] for _ in range(3)]
current_player = 'X'


def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None


def is_draw():
    return all(cell is not None for row in board for cell in row)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('make_move')
def handle_move(data):
    global board, current_player
    row, col = data['row'], data['col']
    if board[row][col] is None and data['player'] == current_player:
        board[row][col] = current_player
        winner = check_winner()
        if winner:
            emit('game_update', {'board': board, 'winner': winner}, broadcast=True)
            return
        elif is_draw():
            emit('game_update', {'board': board, 'draw': True}, broadcast=True)
            return
        # Switch player
        current_player = 'O' if current_player == 'X' else 'X'
        emit('game_update', {'board': board, 'current_player': current_player}, broadcast=True)
    else:
        emit('invalid_move', {'message': 'Invalid move'}, broadcast=False)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=1920, debug=False)
