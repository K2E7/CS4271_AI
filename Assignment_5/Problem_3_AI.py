import tkinter as tk
from tkinter import messagebox
import numpy as np

# Constants
EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2
ROWS = 6
COLS = 7
WINDOW_SIZE = 80

class Connect4Game:
    def __init__(self):
        self.board = np.zeros((ROWS, COLS), dtype=int)
        self.current_player = PLAYER1
        self.game_over = False

    def drop_disc(self, col):
        if not self.game_over and self.is_valid_move(col):
            row = self.next_open_row(col)
            if row is not None:
                self.board[row][col] = self.current_player
                self.check_win(row, col)
                self.switch_player()

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
        else:
            self.current_player = PLAYER1

    def is_valid_move(self, col):
        return self.board[0][col] == EMPTY
    
    def next_open_row(self, col):
        for row in range(ROWS-1, -1, -1):
            if self.board[row][col] == EMPTY:
                return row
        return None  # Column is full

class Connect4AI:
    def __init__(self, game):
        self.game = game

    def ai_move(self):
        best_score = float('-inf')
        best_col = None
        for col in range(COLS):
            if self.game.is_valid_move(col):
                row = self.game.next_open_row(col)
                temp_board = self.game.board.copy()
                self.game.drop_disc(row, col)
                score = self.minimax(4, False, float('-inf'), float('inf'))  # Adjust depth as needed
                self.game.board = temp_board  # Undo move
                if score > best_score:
                    best_score = score
                    best_col = col
        return best_col

    def minimax(self, depth, maximizing_player, alpha, beta):
        if depth == 0 or self.game.game_over:
            return self.evaluate_board()

        if maximizing_player:
            max_eval = float('-inf')
            for col in range(COLS):
                if self.game.is_valid_move(col):
                    row = self.game.next_open_row(col)
                    self.game.drop_disc(row, col)
                    eval = self.minimax(depth - 1, False, alpha, beta)
                    self.game.board[row][col] = EMPTY  # Undo move
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float('inf')
            for col in range(COLS):
                if self.game.is_valid_move(col):
                    row = self.game.next_open_row(col)
                    self.game.drop_disc(row, col)
                    eval = self.minimax(depth - 1, True, alpha, beta)
                    self.game.board[row][col] = EMPTY  # Undo move
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    def evaluate_board(self):
        # Placeholder evaluation function
        return np.random.randint(-100, 100)  # Random evaluation for demonstration purposes

class Connect4GUI:
    def __init__(self, root):
        self.root = root
        self.game = Connect4Game()
        self.ai = Connect4AI(self.game)

        self.canvas = tk.Canvas(root, width=COLS * WINDOW_SIZE, height=ROWS * WINDOW_SIZE)
        self.canvas.pack()

        self.draw_grid()

        for col in range(COLS):
            button = tk.Button(root, text=f"Col {col+1}", width=8, height=2, command=lambda c=col: self.drop_disc(c))
            button.pack(side="left")

        reset_button = tk.Button(root, text="Reset Game", width=10, height=2, command=self.reset_game)
        reset_button.pack()

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
                    circle_size = min(WINDOW_SIZE // 2 - 10, ROWS * WINDOW_SIZE // 2 // ROWS - 10)*2
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
            winner = "Player 1" if self.game.current_player == PLAYER2 else "AI"
            messagebox.showinfo("Game Over", f"{winner} wins!")

root = tk.Tk()
root.title("Connect 4 Game")
app = Connect4GUI(root)
root.mainloop()