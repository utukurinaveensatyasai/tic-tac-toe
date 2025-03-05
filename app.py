import os
from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

def init_board():
    return [[" " for _ in range(3)] for _ in range(3)]

board = init_board()

def check_winner():
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != " ":
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]
    return None

def is_full():
    return all(cell != " " for row in board for cell in row)

def minimax(depth, is_maximizing):
    winner = check_winner()
    if winner == "X":
        return -10 + depth
    if winner == "O":
        return 10 - depth
    if is_full():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    score = minimax(depth + 1, False)
                    board[i][j] = " "
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score = minimax(depth + 1, True)
                    board[i][j] = " "
                    best_score = min(best_score, score)
        return best_score

def best_move():
    best_score = -math.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(0, False)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    global board
    data = request.json
    row, col = data['row'], data['col']

    if board[row][col] == " ":
        board[row][col] = "X"

        if check_winner() == "X":
            return jsonify({"status": "win", "winner": "X", "board": sum(board, [])})

        if is_full():
            return jsonify({"status": "draw", "board": sum(board, [])})

        ai_move = best_move()
        if ai_move:
            board[ai_move[0]][ai_move[1]] = "O"

            if check_winner() == "O":
                return jsonify({"status": "win", "winner": "O", "board": sum(board, [])})

        if is_full():
            return jsonify({"status": "draw", "board": sum(board, [])})

        return jsonify({"status": "continue", "board": sum(board, [])})

    return jsonify({"status": "invalid", "message": "Cell already occupied", "board": sum(board, [])})

@app.route('/reset', methods=['POST'])
def reset():
    global board
    board = init_board()
    return jsonify({"message": "Game Reset", "board": sum(board, [])})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
