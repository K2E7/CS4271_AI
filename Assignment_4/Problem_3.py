from heapq import heappop, heappush
import tkinter as tk
from tkinter import ttk


def heuristic(state):
    # Define a heuristic function to estimate the cost from a state to the goal state
    m_left, c_left, b_left, m_right, c_right, b_right = state
    return m_left + c_left  # Example heuristic: total number of missionaries and cannibals on the left bank

def valid_state(m, c):
    if m < 0 or c < 0 or m > 3 or c > 3:
        return False
    return (m >= c or m == 0) and (3 - m >= 3 - c or 3 - m == 0)  # Ensure no more cannibals than missionaries on either side

def generate_moves(state):
    m_left, c_left, b_left, m_right, c_right, b_right = state
    moves = []
    if b_left:
        for i in range(3):
            for j in range(3):
                if i + j >= 1 and i + j <= 2:
                    if valid_state(m_left - i, c_left - j) and valid_state(m_right + i, c_right + j):
                        moves.append((i, j, "from left to right"))
    else:
        for i in range(3):
            for j in range(3):
                if i + j >= 1 and i + j <= 2:
                    if valid_state(m_left + i, c_left + j) and valid_state(m_right - i, c_right - j):
                        moves.append((i, j, "from right to left"))
    return moves

def solve():
    start_state = (3, 3, 1, 0, 0, 0)
    goal_state = (0, 0, 0, 3, 3, 1)
    heap = [(heuristic(start_state), 0, start_state, [])]  # Use a priority queue based on heuristic value
    visited = set()

    while heap:
        _, cost, state, path = heappop(heap)
        if state == goal_state:
            return path
        if state in visited:
            continue
        visited.add(state)
        moves = generate_moves(state)
        for move in moves:
            new_state = None
            if state[2]:  # If boat is on the left
                new_state = (state[0] - move[0], state[1] - move[1], 0, state[3] + move[0], state[4] + move[1], 1)
            else:  # If boat is on the right
                new_state = (state[0] + move[0], state[1] + move[1], 1, state[3] - move[0], state[4] - move[1], 0)
            if new_state not in visited:
                new_cost = cost + 1  # Uniform cost in this case
                priority = new_cost + heuristic(new_state)  # A* cost function
                heappush(heap, (priority, new_cost, new_state, path + [move]))

    return None

def display_solution(solution):
    root = tk.Tk()
    root.title("Missionaries and Cannibals Solution")

    table = ttk.Treeview(root, columns=("Step", "Missionaries", "Cannibals", "Direction", "Missionaries Left", "Cannibals Left", "Missionaries Right", "Cannibals Right"), show="headings")
    table.heading("Step", text="Step")
    table.heading("Missionaries", text="Missionaries")
    table.heading("Cannibals", text="Cannibals")
    table.heading("Direction", text="Direction")
    table.heading("Missionaries Left", text="Missionaries Left")
    table.heading("Cannibals Left", text="Cannibals Left")
    table.heading("Missionaries Right", text="Missionaries Right")
    table.heading("Cannibals Right", text="Cannibals Right")

    state = (3, 3, 1, 0, 0, 0)  # Initial state
    for step, move in enumerate(solution):
        m_left, c_left, b_left, m_right, c_right, b_right = state
        if move[2] == 'from left to right':
            m_left -= move[0]
            c_left -= move[1]
            m_right += move[0]
            c_right += move[1]
        else:
            m_left += move[0]
            c_left += move[1]
            m_right -= move[0]
            c_right -= move[1]
        missionaries_left = f"{m_left} {'→' if move[2] == 'from left to right' else '←'} {m_right}"
        cannibals_left = f"{c_left} {'→' if move[2] == 'from left to right' else '←'} {c_right}"
        table.insert("", "end", values=(step + 1, missionaries_left, cannibals_left, move[2], m_left, c_left, m_right, c_right))
        state = (m_left, c_left, b_left, m_right, c_right, b_right)

    table.pack(padx=10, pady=10)

    root.mainloop()

# Assuming solution is already computed
solution = solve()
if solution:
    display_solution(solution)
else:
    print("No solution found.")