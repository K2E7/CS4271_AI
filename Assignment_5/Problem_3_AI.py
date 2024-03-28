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
        if not self.game_over:
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
        else:
            self.current_player = PLAYER1

    def get_next_player(self):
        return PLAYER2 if self.current_player == PLAYER1 else PLAYER1

    def get_next_move(self):
        for col in range(COLS):
            if self.is_valid_move(col):
                # Check if placing a disc in this column leads to a win for the current player
                if self.check_win_move(col, self.current_player):
                    return col
                # Check if placing a disc in this column prevents the opponent from winning
                elif self.check_win_move(col, self.get_next_player()):
                    return col
        # If no winning or blocking move found, prioritize seven formation and middle column placement
        if self.is_valid_move(COLS // 2):
            return COLS // 2
        return self.find_seven_formation()

    def is_valid_move(self, col):
        return self.board[0][col] == EMPTY

    def check_win_move(self, col, player):
        temp_board = np.copy(self.board)
        for row in range(ROWS-1, -1, -1):
            if temp_board[row][col] == EMPTY:
                temp_board[row][col] = player
                if self.check_win(row, col, temp_board, player):
                    return True
                break
        return False

    def find_seven_formation(self):
        for col in range(COLS):
            if self.is_valid_move(col):
                temp_board = np.copy(self.board)
                for row in range(ROWS-1, -1, -1):
                    if temp_board[row][col] == EMPTY:
                        temp_board[row][col] = self.current_player
                        if self.check_seven_formation(row, col, temp_board):
                            return col
                        break
        return self.find_middle_column()

    def check_seven_formation(self, row, col, board):
        # Check if placing a disc in this position forms a "seven" formation
        player = board[row][col]
        count = 0
        for r in range(max(row-3, 0), min(row+4, ROWS)):
            for c in range(max(col-3, 0), min(col+4, COLS)):
                if board[r][c] == player:
                    count += 1
                    if count >= 7:
                        return True
                else:
                    count = 0
        return False

    def find_middle_column(self):
        middle_col = COLS // 2
        for offset in range(1, COLS // 2 + 1):
            left_col = middle_col - offset
            right_col = middle_col + offset
            if self.is_valid_move(left_col):
                return left_col
            elif self.is_valid_move(right_col):
                return right_col
        return None

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

        # Add AI button and text box
        ai_button = tk.Button(root, text="AI Move", width=10, height=2, command=self.ai_move)
        ai_button.pack()
        self.ai_text = tk.Text(root, height=1, width=20)
        self.ai_text.pack()

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

    def ai_move(self):
        next_move = self.game.get_next_move()
        self.ai_text.delete("1.0", tk.END)
        self.ai_text.insert(tk.END, f"AI suggests column {next_move+1}")

root = tk.Tk()
root.title("Connect 4 Game")
app = Connect4GUI(root)
root.mainloop()
