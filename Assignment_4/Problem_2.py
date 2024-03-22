import tkinter as tk

class MonkeyBananaGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Monkey and Banana Problem")

        # Initialize variables
        self.grid_size = 5  # Size of the grid
        self.room_grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]  # Room grid
        self.monkey_pos = (4, 0)  # Monkey's initial position on the ground
        self.box_pos = (4, 2)  # Box's initial position
        self.banana_pos = (3, 3)  # Banana's position

        # Create canvas for the grid
        self.canvas = tk.Canvas(master, width=300, height=300, borderwidth=2, relief="ridge")
        self.canvas.pack()

        # Draw the grid
        cell_size = 60
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x0, y0 = j * cell_size, i * cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size
                self.room_grid[i][j] = self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")

        # Place objects in the grid
        self.update_grid()

        # Create buttons for monkey's actions
        self.walk_button = tk.Button(master, text="Walk", command=self.walk)
        self.walk_button.pack(side=tk.LEFT)

        self.climb_button = tk.Button(master, text="Climb", command=self.climb)
        self.climb_button.pack(side=tk.LEFT)

        self.push_button = tk.Button(master, text="Push", command=self.push)
        self.push_button.pack(side=tk.LEFT)

        self.grab_button = tk.Button(master, text="Grab", command=self.grab)
        self.grab_button.pack(side=tk.LEFT)

        # Create reset button
        self.reset_button = tk.Button(master, text="Reset", command=self.reset)
        self.reset_button.pack()

    def walk(self):
        # Implement walk action logic
        new_pos = (self.monkey_pos[0], self.monkey_pos[1] + 1)
        if self.is_valid_position(new_pos):
            self.monkey_pos = new_pos
            self.update_grid()
        else:
            print("Walking is not possible in this direction.")

    def climb(self):
        # Implement climb action logic
        left_box_pos = (self.monkey_pos[0], self.monkey_pos[1] - 1)
        right_box_pos = (self.monkey_pos[0], self.monkey_pos[1] + 1)
        if self.box_pos == left_box_pos or self.box_pos == right_box_pos:
            self.monkey_pos = self.box_pos
            self.update_grid()
        else:
            print("Climbing is not possible.")

    def push(self):
        # Implement push action logic
        new_box_pos = (self.box_pos[0], self.box_pos[1] + 1)
        if self.is_valid_position(new_box_pos):
            self.box_pos = new_box_pos
            self.update_grid()
        else:
            print("Pushing the box is not possible in this direction.")

    def grab(self):
        # Implement grab action logic
        if self.monkey_pos == self.box_pos and self.monkey_pos == self.banana_pos:
            self.banana_pos = self.box_pos
            self.update_grid()
        else:
            print("Grabbing the banana is not possible.")

    def reset(self):
        # Reset positions of monkey, box, and banana
        self.monkey_pos = (4, 0)
        self.box_pos = (2, 2)
        self.banana_pos = (0, 4)
        self.update_grid()

    def update_grid(self):
        # Update the grid to reflect current positions
        self.canvas.delete("all")
        cell_size = 60
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x0, y0 = j * cell_size, i * cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size
                self.room_grid[i][j] = self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")

        # Place monkey, box, and banana on the grid
        self.canvas.create_oval(self.monkey_pos[1] * cell_size, self.monkey_pos[0] * cell_size,
                                (self.monkey_pos[1] + 1) * cell_size, (self.monkey_pos[0] + 1) * cell_size,
                                fill="brown")
        self.canvas.create_rectangle(self.box_pos[1] * cell_size, self.box_pos[0] * cell_size,
                                     (self.box_pos[1] + 1) * cell_size, (self.box_pos[0] + 1) * cell_size,
                                     fill="gray")
        self.canvas.create_rectangle(self.banana_pos[1] * cell_size, self.banana_pos[0] * cell_size,
                                     (self.banana_pos[1] + 1) * cell_size, (self.banana_pos[0] + 1) * cell_size,
                                     fill="yellow")

    def is_valid_position(self, pos):
        # Check if the position is within the grid bounds
        return 0 <= pos[0] < self.grid_size and 0 <= pos[1] < self.grid_size

def main():
    root = tk.Tk()
    app = MonkeyBananaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
