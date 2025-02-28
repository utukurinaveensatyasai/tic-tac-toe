import tkinter as tk
from tkinter import messagebox
import math

# Initialize Board
board = [[" " for _ in range(3)] for _ in range(3)]

# Check Winner
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

# Check if board is full
def is_full():
    return all(cell != " " for row in board for cell in row)

# Minimax Algorithm
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

# Get Best Move for AI
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

# Handle Button Click
def on_click(row, col):
    global board
    if board[row][col] == " ":
        board[row][col] = "X"
        buttons[row][col].config(text="X", state="disabled", disabledforeground="blue")

        if check_winner() == "X":
            messagebox.showinfo("Game Over", "You win! 🎉")
            reset_board()
            return

        if is_full():
            messagebox.showinfo("Game Over", "It's a draw! 🤝")
            reset_board()
            return

        ai_move = best_move()
        if ai_move:
            board[ai_move[0]][ai_move[1]] = "O"
            buttons[ai_move[0]][ai_move[1]].config(text="O", state="disabled", disabledforeground="red")

        if check_winner() == "O":
            messagebox.showinfo("Game Over", "AI wins! 🤖🏆")
            reset_board()
            return

        if is_full():
            messagebox.showinfo("Game Over", "It's a draw! 🤝")
            reset_board()
            return

# Reset Board
def reset_board():
    global board
    board = [[" " for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=" ", state="normal")

# Create GUI Window
root = tk.Tk()
root.title("Tic Tac Toe - AI (Minimax)")

buttons = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text=" ", font=("Arial", 24), width=5, height=2,
                                  command=lambda row=i, col=j: on_click(row, col))
        buttons[i][j].grid(row=i, column=j)

root.mainloop()
