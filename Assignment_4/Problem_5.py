import heapq
import copy
import tkinter as tk
from tkinter import messagebox

# Define the goal state for the 8-puzzle
goal_state = ((1, 2, 3), (4, 5, 6), (7, 8, 0))  # 0 represents the empty space

def get_possible_moves(board):
    moves = []
    empty_pos = None
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                empty_pos = (i, j)
                break

    if empty_pos is None:
        return moves  # No empty space found

    # Check possible moves (up, down, left, right)
    if empty_pos[0] > 0:
        moves.append((empty_pos[0] - 1, empty_pos[1]))  # Move up
    if empty_pos[0] < len(board) - 1:
        moves.append((empty_pos[0] + 1, empty_pos[1]))  # Move down
    if empty_pos[1] > 0:
        moves.append((empty_pos[0], empty_pos[1] - 1))  # Move left
    if empty_pos[1] < len(board[0]) - 1:
        moves.append((empty_pos[0], empty_pos[1] + 1))  # Move right

    return moves


def calculate_manhattan_distance(board):
    distance = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            value = board[i][j]
            if value != 0:
                goal_pos = divmod(value - 1, len(board[0]))
                distance += abs(i - goal_pos[0]) + abs(j - goal_pos[1])
    return distance


def solve_puzzle(initial_state):
    open_set = [(calculate_manhattan_distance(initial_state), 0, initial_state)]
    heapq.heapify(open_set)
    came_from = {}
    g_score = {initial_state: 0}

    while open_set:
        _, moves, current = heapq.heappop(open_set)

        if current == goal_state:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        empty_pos = None
        for i in range(len(current)):
            for j in range(len(current[i])):
                if current[i][j] == 0:
                    empty_pos = (i, j)
                    break

        possible_moves = get_possible_moves(current)
        for move in possible_moves:
            new_board = list(map(list, current))
            new_board[empty_pos[0]][empty_pos[1]], new_board[move[0]][move[1]] = \
                new_board[move[0]][move[1]], new_board[empty_pos[0]][empty_pos[1]]
            new_board = tuple(map(tuple, new_board))

            tentative_g_score = g_score[current] + 1
            if new_board not in g_score or tentative_g_score < g_score[new_board]:
                g_score[new_board] = tentative_g_score
                heapq.heappush(open_set, (tentative_g_score + calculate_manhattan_distance(new_board), moves + 1, new_board))
                came_from[new_board] = current

    return None  # No solution found


class PuzzleSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")

        self.init_frame = tk.Frame(root)
        self.init_frame.pack()

        self.init_entries = [[None] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.init_entries[i][j] = tk.Entry(self.init_frame, width=6)
                self.init_entries[i][j].grid(row=i, column=j)

        self.init_button = tk.Button(root, text="Set Initial State", command=self.set_initial_state)
        self.init_button.pack()

        self.board = tk.Frame(root)
        self.board.pack()

        self.buttons = [[None] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.board, text='', width=6, height=3, command=lambda i=i, j=j: self.move_tile(i, j))
                self.buttons[i][j].grid(row=i, column=j)

        self.next_move_button = tk.Button(root, text="Next Move", command=self.next_move)
        self.next_move_button.pack()

        self.current_step = 0
        self.solution_path = None

    def set_initial_state(self):
        initial_state = []
        for row in self.init_entries:
            initial_state.append([int(entry.get()) for entry in row])
        self.solution_path = solve_puzzle(tuple(map(tuple, initial_state)))
        if self.solution_path:
            self.current_state = copy.deepcopy(initial_state)
            self.update_board()
            self.init_frame.pack_forget()
        else:
            messagebox.showerror("Error", "Invalid initial state or unsolvable puzzle.")

    # Other methods remain unchanged

    def init_board(self):
        self.current_state = copy.deepcopy(goal_state)
        self.update_board()

    def update_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=str(self.current_state[i][j]) if self.current_state[i][j] != 0 else '', state=tk.DISABLED if self.current_state[i][j] == 0 else tk.NORMAL)

    def move_tile(self, row, col):
        empty_pos = None
        for i in range(3):
            for j in range(3):
                if self.current_state[i][j] == 0:
                    empty_pos = (i, j)
                    break
        
        if (row, col) in self.get_possible_moves(empty_pos):
            self.current_state[empty_pos[0]][empty_pos[1]], self.current_state[row][col] = self.current_state[row][col], self.current_state[empty_pos[0]][empty_pos[1]]
            self.update_board()

    def get_possible_moves(self, empty_pos):
        moves = []
        if empty_pos[0] > 0:
            moves.append((empty_pos[0] - 1, empty_pos[1]))  # Move up
        if empty_pos[0] < 2:
            moves.append((empty_pos[0] + 1, empty_pos[1]))  # Move down
        if empty_pos[1] > 0:
            moves.append((empty_pos[0], empty_pos[1] - 1))  # Move left
        if empty_pos[1] < 2:
            moves.append((empty_pos[0], empty_pos[1] + 1))  # Move right
        return moves

    def next_move(self):
        if self.current_step < len(self.solution_path):
            self.current_state = self.solution_path[self.current_step]
            self.update_board()
            self.current_step += 1
        else:
            print("No more moves!")

    

root = tk.Tk()
app = PuzzleSolverGUI(root)
root.mainloop()
