"""
DAA Project: 8-Queens Problem Visualization in Python (Tkinter)
Algorithm: Backtracking
Author: Auto-generated

Q1   Q2   Q3   Q4   Q5   Q6   Q7   Q8
"""

import tkinter as tk
from tkinter import messagebox
import time

BOARD_SIZE = 8
CELL_SIZE = 60
DELAY = 0.3  # seconds delay for visualization

class EightQueensApp:
    def __init__(self, root):
        self.root = root
        root.title("DAA: 8-Queens Problem")
        self.canvas = tk.Canvas(root, width=BOARD_SIZE*CELL_SIZE, height=BOARD_SIZE*CELL_SIZE)
        self.canvas.pack()

        self.board = [[0]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.rects = [[None]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.draw_board()

        self.btn_start = tk.Button(root, text="Solve 8-Queens", command=self.start_solver)
        self.btn_start.pack(pady=10)

        self.solutions = []

    def draw_board(self):
        colors = ["#f0d9b5", "#b58863"]
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                x1 = j*CELL_SIZE
                y1 = i*CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=colors[(i+j)%2])
                self.rects[i][j] = rect

    def place_queen(self, row, col):
        x = col*CELL_SIZE + CELL_SIZE//2
        y = row*CELL_SIZE + CELL_SIZE//2
        r = CELL_SIZE//3
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="Black", tags="queen")
        self.root.update()
        time.sleep(DELAY)

    def remove_queen(self, row, col):
        # remove last queen drawn
        items = self.canvas.find_withtag("queen")
        if items:
            self.canvas.delete(items[-1])
        self.root.update()
        time.sleep(DELAY/2)

    def is_safe(self, row, col):
        # check column
        for i in range(row):
            if self.board[i][col] == 1:
                return False
        # check upper-left diagonal
        i, j = row-1, col-1
        while i>=0 and j>=0:
            if self.board[i][j]==1:
                return False
            i-=1
            j-=1
        # check upper-right diagonal
        i, j = row-1, col+1
        while i>=0 and j<BOARD_SIZE:
            if self.board[i][j]==1:
                return False
            i-=1
            j+=1
        return True

    def solve_queens(self, row=0):
        if row == BOARD_SIZE:
            solution = [r[:] for r in self.board]
            self.solutions.append(solution)
            return True  # return True to find first solution

        for col in range(BOARD_SIZE):
            if self.is_safe(row, col):
                self.board[row][col] = 1
                self.place_queen(row, col)
                if self.solve_queens(row+1):
                    return True  # comment this line to find all solutions
                self.board[row][col] = 0
                self.remove_queen(row, col)
        return False

    def start_solver(self):
        self.canvas.delete("queen")
        self.board = [[0]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.solutions = []
        solved = self.solve_queens()
        if solved:
            messagebox.showinfo("Solved", f"8-Queens solution found! Total solutions stored: {len(self.solutions)}")
        else:
            messagebox.showinfo("No solution", "No solution exists.")

if __name__ == '__main__':
    root = tk.Tk()
    app = EightQueensApp(root)
    root.mainloop()