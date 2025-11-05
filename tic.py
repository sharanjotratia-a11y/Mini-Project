import tkinter as tk
from tkinter import messagebox

# --- Initialize Window ---
root = tk.Tk()
root.title("AI Tic Tac Toe 🧠")
root.resizable(False, False)
root.configure(bg="#222831")

player = "X"
ai = "O"

buttons = [[None for _ in range(3)] for _ in range(3)]
lines = []  # to store line coordinates for highlight

# --- Utility Functions ---
def is_full():
    return all(buttons[i][j]["text"] != "" for i in range(3) for j in range(3))

def check_winner(board):
    # Rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0], ("row", i)
    # Columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != "":
            return board[0][j], ("col", j)
    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0], ("diag", 0)
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2], ("diag", 1)
    return None, None

# --- Minimax AI Algorithm ---
def minimax(board, depth, is_maximizing):
    winner, _ = check_winner(board)
    if winner == ai:
        return 1
    elif winner == player:
        return -1
    elif is_full():
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = ai
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = player
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ""
                    best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = -float("inf")
    move = None
    board = [[buttons[i][j]["text"] for j in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = ai
                score = minimax(board, 0, False)
                board[i][j] = ""
                if score > best_score:
                    best_score = score
                    move = (i, j)
    if move:
        buttons[move[0]][move[1]].config(text=ai, fg="#00FF00", state="disabled")  # green O
        check_game_over()

def on_click(i, j):
    if buttons[i][j]["text"] == "":
        buttons[i][j].config(text=player, fg="#00BFFF", state="disabled")  # blue X
        check_game_over()
        ai_move()

def highlight_winner(win_type, index):
    # draw a red line through the winning combination
    canvas = tk.Canvas(root, width=300, height=300, bg="#222831", highlightthickness=0)
    canvas.place(x=50, y=70)

    if win_type == "row":
        y = 50 + index * 100 + 50
        canvas.create_line(20, y, 280, y, fill="red", width=5)
    elif win_type == "col":
        x = 50 + index * 100 + 50
        canvas.create_line(x, 20, x, 280, fill="red", width=5)
    elif win_type == "diag" and index == 0:
        canvas.create_line(20, 20, 280, 280, fill="red", width=5)
    elif win_type == "diag" and index == 1:
        canvas.create_line(280, 20, 20, 280, fill="red", width=5)

    lines.append(canvas)

def check_game_over():
    board = [[buttons[i][j]["text"] for j in range(3)] for i in range(3)]
    winner, win_pos = check_winner(board)
    if winner:
        highlight_winner(win_pos[0], win_pos[1])
        messagebox.showinfo("Game Over", f"{winner} wins!")
        reset_board()
    elif is_full():
        messagebox.showinfo("Game Over", "It's a Draw!")
        reset_board()

def reset_board():
    for line in lines:
        line.destroy()
    lines.clear()
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", state="normal")

# --- Create UI Board ---
frame = tk.Frame(root, bg="#222831")
frame.pack(pady=20, padx=50)

for i in range(3):
    for j in range(3):
        btn = tk.Button(
            frame, text="", font=("Arial", 24, "bold"), width=5, height=2,
            bg="#393E46", fg="white", activebackground="#00ADB5",
            command=lambda i=i, j=j: on_click(i, j)
        )
        btn.grid(row=i, column=j, padx=5, pady=5)
        buttons[i][j] = btn

tk.Button(
    root, text="Reset Game", font=("Arial", 12, "bold"), bg="#00ADB5",
    fg="white", command=reset_board
).pack(pady=10)

root.geometry("400x450")
root.mainloop()
