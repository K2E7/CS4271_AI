import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import copy

# Define the initial and final states
initial_state = {'man': 'left', 'wolf': 'left', 'goat': 'left', 'cabbage': 'left'}
final_state = {'man': 'right', 'wolf': 'right', 'goat': 'right', 'cabbage': 'right'}

# Define the valid moves based on the current state
def find_moves(state):
    moves = [['man']]
    for obj in ['wolf', 'goat', 'cabbage']:
        if state[obj] == state['man']:
            moves.append(['man', obj])
    return moves

# Update the state based on the move and check if it's valid
def update_state(state, move):
    new_state = copy.deepcopy(state)
    for m in move:
        new_state[m] = 'right' if state[m] == 'left' else 'left'
    if is_valid(new_state):
        return new_state
    else:
        return False

# Check if the state is valid (constraints not violated)
def is_valid(state):
    if (state['goat'] == state['wolf']) and (state['man'] != state['wolf']):
        return False
    if (state['goat'] == state['cabbage']) and (state['man'] != state['cabbage']):
        return False
    return True

# Solve the problem using backtracking
def solve(state, final_state, moves, state_list):
    if state == final_state:
        return True
    else:
        for move in moves:
            new_state = update_state(state, move)
            if new_state and new_state not in state_list:
                state_list.append(new_state)
                new_moves = find_moves(new_state)
                if solve(new_state, final_state, new_moves, state_list):
                    return True
        return False

# Create the GUI window
def create_window():
    window = tk.Tk()
    window.title("Farmer, Wolf, Goat, and Cabbage Problem")
    return window

# Function to handle the "Next Move" button click
def next_move():
    global current_state, state_list, display_table
    if state_list:
        current_state = state_list.pop(0)
        update_display(current_state)
    else:
        messagebox.showinfo("No More Moves", "No more valid moves!")

# Function to update the display with the current state in a tabular format
def update_display(state):
    display_table.insert('', 'end', values=[state['man'], state['wolf'], state['goat'], state['cabbage']])

# Main function to initialize the GUI
def main():
    global current_state, state_list, display_table

    # Initialize GUI elements
    window = create_window()

    display_table = tk.ttk.Treeview(window, columns=('Man', 'Wolf', 'Goat', 'Cabbage'), show='headings')
    display_table.heading('Man', text='Man')
    display_table.heading('Wolf', text='Wolf')
    display_table.heading('Goat', text='Goat')
    display_table.heading('Cabbage', text='Cabbage')
    display_table.pack()

    next_move_btn = tk.Button(window, text="Next Move", command=next_move)
    next_move_btn.pack()

    # Solve the problem and populate state_list with solution steps
    state_list = [initial_state]
    solve(initial_state, final_state, find_moves(initial_state), state_list)

    # Set the initial state for display
    current_state = state_list.pop(0)
    update_display(current_state)

    window.mainloop()

if __name__ == "__main__":
    main()
