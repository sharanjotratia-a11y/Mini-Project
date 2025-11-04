import tkinter as tk
from tkinter import messagebox
import random
import time
import threading
from collections import deque

# ----------------------------
# Treasure Hunt Game (Player vs BFS)
# ----------------------------

ROWS, COLS = 15, 15
CELL_SIZE = 30

root = tk.Tk()
root.title("💎 Treasure Hunt Race — You vs BFS")
root.resizable(False, False)

canvas = tk.Canvas(root, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg="white")
canvas.pack()

# Maze generation
maze = [[random.choice([0, 1]) for _ in range(COLS)] for _ in range(ROWS)]
maze[0][0] = 0

# Random treasure
treasure = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
while treasure == (0, 0) or maze[treasure[0]][treasure[1]] == 1:
    treasure = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))

# Player and AI positions
player_pos = [0, 0]
ai_pos = [0, 0]
ai_path = []
ai_running = False

# Draw maze and entities
def draw():
    canvas.delete("all")
    for r in range(ROWS):
        for c in range(COLS):
            x1, y1 = c * CELL_SIZE, r * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            color = "black" if maze[r][c] == 1 else "white"
            if (r, c) == tuple(player_pos):
                color = "orange"  # player
            elif (r, c) == tuple(ai_pos):
                color = "#00b4d8"  # AI
            elif (r, c) == treasure:
                color = "#e63946"  # treasure
            elif (r, c) in ai_path:
                color = "#90e0ef"  # AI path
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

# Neighbors
def get_neighbors(r, c):
    for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] == 0:
            yield nr, nc

# BFS algorithm
def bfs_path(start, goal):
    queue = deque([start])
    parent = {start: None}
    while queue:
        r, c = queue.popleft()
        if (r, c) == goal:
            path = []
            while (r, c) is not None:
                path.append((r, c))
                r, c = parent[(r, c)]
            return path[::-1]
        for nr, nc in get_neighbors(r, c):
            if (nr, nc) not in parent:
                parent[(nr, nc)] = (r, c)
                queue.append((nr, nc))
    return []

# AI BFS movement
def ai_move():
    global ai_running, ai_path, ai_pos
    ai_running = True
    ai_path = bfs_path(tuple(ai_pos), treasure)
    for pos in ai_path[1:]:
        if not ai_running:
            return
        ai_pos[0], ai_pos[1] = pos
        draw()
        root.update()
        time.sleep(0.15)
        if tuple(ai_pos) == treasure:
            messagebox.showinfo("😢 You Lost!", "BFS found the treasure first!")
            ai_running = False
            return

# Player movement
def move_player(dr, dc):
    if ai_running is False:
        threading.Thread(target=ai_move, daemon=True).start()

    nr, nc = player_pos[0] + dr, player_pos[1] + dc
    if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] == 0:
        player_pos[0], player_pos[1] = nr, nc
    draw()

    # Check win
    if tuple(player_pos) == treasure:
        messagebox.showinfo("🏆 You Win!", "You found the treasure before BFS!")
        stop_game()

# Stop AI after win
def stop_game():
    global ai_running
    ai_running = False

# Regenerate maze
def new_game():
    global maze, treasure, player_pos, ai_pos, ai_path, ai_running
    maze = [[random.choice([0, 1]) for _ in range(COLS)] for _ in range(ROWS)]
    maze[0][0] = 0
    treasure = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
    while treasure == (0, 0) or maze[treasure[0]][treasure[1]] == 1:
        treasure = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
    player_pos = [0, 0]
    ai_pos = [0, 0]
    ai_path = []
    ai_running = False
    draw()

# Key bindings
root.bind("<Up>", lambda e: move_player(-1, 0))
root.bind("<Down>", lambda e: move_player(1, 0))
root.bind("<Left>", lambda e: move_player(0, -1))
root.bind("<Right>", lambda e: move_player(0, 1))

# Buttons
frame = tk.Frame(root)
frame.pack(pady=5)
tk.Button(frame, text="New Game", command=new_game, width=15, bg="#2a9d8f").grid(row=0, column=0, padx=5)
tk.Button(frame, text="Quit", command=root.destroy, width=15, bg="#e63946").grid(row=0, column=1, padx=5)

draw()
root.mainloop()
