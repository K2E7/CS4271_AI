import sys
import tkinter as tk
from tkinter import messagebox, simpledialog

import copy
from collections import deque

def evaluate(board):
    """
    Evaluate the current state of the Tic Tac Toe board.
    Returns 1 if the computer wins, -1 if the player wins, 0 for a draw, and None if the game is ongoing.
    """
    for i in range(3):
        # Check rows and columns
        if board[i][0] == board[i][1] == board[i][2] != "":
            return 1 if board[i][0] == "O" else -1
        if board[0][i] == board[1][i] == board[2][i] != "":
            return 1 if board[0][i] == "O" else -1

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != "":
        return 1 if board[0][0] == "O" else -1
    if board[0][2] == board[1][1] == board[2][0] != "":
        return 1 if board[0][2] == "O" else -1

    # Check for draw
    for row in board:
        for cell in row:
            if cell == "":
                return None
    return 0

def bfs(board, depth, maximizing_player):
    """
    Perform a breadth-first search to evaluate the game tree and determine the most optimal move.
    """
    queue = deque([(board, maximizing_player, depth)])
    while queue:
        current_board, current_player, current_depth = queue.popleft()
        if evaluate(current_board) is not None or current_depth == 0:
            if evaluate(current_board) == 1:
                return 10 - current_depth
            elif evaluate(current_board) == -1:
                return current_depth - 10
            else:
                return 0
        empty_cells = [(i, j) for i in range(3) for j in range(3) if current_board[i][j] == ""]
        for i, j in empty_cells:
            new_board = copy.deepcopy(current_board)
            new_board[i][j] = "O" if current_player else "X"
            queue.append((new_board, not current_player, current_depth - 1))

def make_move(board):
    """
    Make a move for the computer player using BFS to find the most optimal move.
    """
    best_score = float('-inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                new_board = copy.deepcopy(board)
                new_board[i][j] = "O"
                score = bfs(new_board, 9, False)
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

class TicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.current_player = None  # To be determined by player choice
        self.computer_player = None  # To be determined by player choice
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.init_game()

    def init_game(self):
        unit = simpledialog.askstring("Select Unit", "Choose your unit:", parent=self.root, 
                                      show="info", choices=["X", "O"])
        if unit:
            self.current_player = unit
            self.computer_player = "O" if unit == "X" else "X"
            self.create_board()
            if self.current_player == self.computer_player:
                self.computer_move()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text="", width=10, height=3,
                                   command=lambda row=i, col=j: self.clicked(row, col))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    def clicked(self, row, col):
        if self.board[row][col] == "":
            self.buttons[row][col].config(text=self.current_player)
            self.board[row][col] = self.current_player
            if self.check_winner(row, col):
                messagebox.showinfo("Winner!", f"{self.current_player} wins!")
                self.reset_board()
            elif self.check_draw():
                messagebox.showinfo("Draw!", "It's a draw!")
                self.reset_board()
            else:
                self.switch_player()
                if self.current_player == self.computer_player:
                    self.computer_move()

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self, row, col):
        # Check row
        if self.board[row][0] == self.board[row][1] == self.board[row][2] == self.current_player:
            return True
        # Check column
        if self.board[0][col] == self.board[1][col] == self.board[2][col] == self.current_player:
            return True
        # Check diagonals
        if (row == col and
                self.board[0][0] == self.board[1][1] == self.board[2][2] == self.current_player):
            return True
        if (row + col == 2 and
                self.board[0][2] == self.board[1][1] == self.board[2][0] == self.current_player):
            return True
        return False

    def check_draw(self):
        for row in self.board:
            for cell in row:
                if cell == "":
                    return False
        return True

    def reset_board(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="")

    def computer_move(self):
        """
        Make a move for the computer player.
        """
        best_move = make_move(self.board)
        if best_move:
            row, col = best_move
            self.buttons[row][col].config(text=self.computer_player)
            self.board[row][col] = self.computer_player
            if self.check_winner(row, col):
                messagebox.showinfo("Winner!", f"{self.computer_player} wins!")
                self.reset_board()
            elif self.check_draw():
                messagebox.showinfo("Draw!", "It's a draw!")
                self.reset_board()
            else:
                self.switch_player()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
