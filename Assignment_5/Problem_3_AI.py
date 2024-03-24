import tkinter as tk
from tkinter import messagebox
import numpy as np
import random

# Constants
EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2
AI_PLAYER = 3  # New constant for AI player
ROWS = 6
COLS = 7
WINDOW_SIZE = 80

class Connect4Game:
    def __init__(self):
        self.board = np.zeros((ROWS, COLS), dtype=int)
        self.current_player = PLAYER1
        self.game_over = False

    def drop_disc(self, col):
        if not self.game_over and self.board[0][col] == EMPTY:
            for row in range(ROWS-1, -1, -1):
                if self.board[row][col] == EMPTY:
                    self.board[row][col] = self.current_player
                    self.check_win(row, col)
                    self.switch_player()
                    break

    def check_win(self, row, col):
        # Check horizontal
        for c in range(COLS - 3):
            if self.board[row][c] == self.current_player and \
               self.board[row][c+1] == self.current_player and \
               self.board[row][c+2] == self.current_player and \
               self.board[row][c+3] == self.current_player:
                self.game_over = True
                return

        # Check vertical
        for r in range(ROWS - 3):
            if self.board[r][col] == self.current_player and \
               self.board[r+1][col] == self.current_player and \
               self.board[r+2][col] == self.current_player and \
               self.board[r+3][col] == self.current_player:
                self.game_over = True
                return

        # Check diagonal (down-right)
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if self.board[r][c] == self.current_player and \
                   self.board[r+1][c+1] == self.current_player and \
                   self.board[r+2][c+2] == self.current_player and \
                   self.board[r+3][c+3] == self.current_player:
                    self.game_over = True
                    return

        # Check diagonal (up-right)
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if self.board[r][c] == self.current_player and \
                   self.board[r-1][c+1] == self.current_player and \
                   self.board[r-2][c+2] == self.current_player and \
                   self.board[r-3][c+3] == self.current_player:
                    self.game_over = True
                    return

    def switch_player(self):
        if self.current_player == PLAYER1:
            self.current_player = PLAYER2
        elif self.current_player == PLAYER2:
            self.current_player = AI_PLAYER  # Switch to AI player
        else:
            self.current_player = PLAYER1

    def ai_move(self):
        if not self.game_over:
            col = random.randint(0, COLS - 1)
            self.drop_disc(col)
            self.switch_player()

class Connect4GUI:
    def __init__(self, root):
        self.root = root
        self.game = Connect4Game()
        self.buttons = []

        self.canvas = tk.Canvas(root, width=COLS * WINDOW_SIZE, height=ROWS * WINDOW_SIZE)
        self.canvas.pack()

        self.draw_grid()

        # Pack column buttons horizontally
        for col in range(COLS):
            button = tk.Button(root, text=f"Col {col+1}", width=8, height=2, command=lambda c=col: self.drop_disc(c))
            button.pack(side="left")

        # Pack reset button below column buttons
        reset_button = tk.Button(root, text="Reset Game", width=10, height=2, command=self.reset_game)
        reset_button.pack()

        # Pack AI play button below reset button
        ai_play_button = tk.Button(root, text="AI Play", width=10, height=2, command=self.ai_play)
        ai_play_button.pack()

    def reset_game(self):
        self.game = Connect4Game()
        self.canvas.delete("disc")  # Clear existing discs
        self.draw_grid()

    def draw_grid(self):
        for row in range(ROWS):
            for col in range(COLS):
                x0 = col * WINDOW_SIZE
                y0 = row * WINDOW_SIZE
                x1 = (col + 1) * WINDOW_SIZE
                y1 = (row + 1) * WINDOW_SIZE
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue")
                if self.game.board[row][col] == EMPTY:
                    circle_size = min(WINDOW_SIZE // 2 - 10, ROWS * WINDOW_SIZE // 2 // ROWS - 10) * 2
                    self.canvas.create_oval(x0 + (WINDOW_SIZE - circle_size) // 2, y0 + (WINDOW_SIZE - circle_size) // 2,
                                            x0 + (WINDOW_SIZE + circle_size) // 2, y0 + (WINDOW_SIZE + circle_size) // 2,
                                            fill="white")

    def drop_disc(self, col):
        self.game.drop_disc(col)
        self.update_board()

    def update_board(self):
        self.canvas.delete("disc")  # Clear existing discs

        for row in range(ROWS):
            for col in range(COLS):
                if self.game.board[row][col] != EMPTY:
                    disc_color = "yellow" if self.game.board[row][col] == PLAYER1 else "red"
                    circle_size = min(WINDOW_SIZE // 2 - 10, ROWS * WINDOW_SIZE // 2 // ROWS - 10) * 2
                    x0 = col * WINDOW_SIZE + (WINDOW_SIZE - circle_size) // 2
                    y0 = row * WINDOW_SIZE + (WINDOW_SIZE - circle_size) // 2
                    x1 = x0 + circle_size
                    y1 = y0 + circle_size
                    self.canvas.create_oval(x0, y0, x1, y1, fill=disc_color, tags="disc")

        if self.game.game_over:
            winner = "Player 1" if self.game.current_player == PLAYER2 else "Player 2"
            messagebox.showinfo("Game Over", f"{winner} wins!")

    def ai_play(self):
        self.game.ai_move()
        self.update_board()

root = tk.Tk()
root.title("Connect 4 Game")
app = Connect4GUI(root)
root.mainloop()
