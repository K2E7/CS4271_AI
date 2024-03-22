import tkinter as tk
from tkinter import messagebox

class Cell:
    def __init__(self, x, y, obstacle=False):
        self.x = x
        self.y = y
        self.obstacle = obstacle
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

class AStarGUI:
    def __init__(self, master, size):
        self.master = master
        self.size = size
        self.grid = [[Cell(x, y) for y in range(size)] for x in range(size)]
        self.start = None
        self.target = None
        self.path = []
        self.obstacle_mode = False
        self.create_gui()

    def create_gui(self):
        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()
        self.create_grid()
        self.canvas.bind('<Button-1>', self.handle_click)
        self.add_start_end_button = tk.Button(self.master, text='Add Start/End', command=self.toggle_add_start_end)
        self.add_start_end_button.pack()
        self.find_path_button = tk.Button(self.master, text='Find Path', command=self.find_path)
        self.find_path_button.pack()

    def create_grid(self):
        self.draw_grid()
        self.reset_start_target()

    def draw_grid(self):
        for x in range(self.size):
            for y in range(self.size):
                self.canvas.create_rectangle(x * 40, y * 40, (x + 1) * 40, (y + 1) * 40)
                self.canvas.create_text(x * 40 + 20, y * 40 + 20, text=f'{x},{y}')

    def reset_start_target(self):
        self.start = None
        self.target = None
        self.draw_cells()

    def draw_cells(self):
        for x in range(self.size):
            for y in range(self.size):
                cell = self.grid[x][y]
                color = 'white' if not cell.obstacle else 'black'
                self.canvas.itemconfig(self.canvas.create_rectangle(x * 40, y * 40, (x + 1) * 40, (y + 1) * 40, fill=color))

    def toggle_add_start_end(self):
        self.obstacle_mode = not self.obstacle_mode
        if self.obstacle_mode:
            self.add_start_end_button.config(text='Add Obstacles')
        else:
            self.add_start_end_button.config(text='Add Start/End')

    def handle_click(self, event):
        x = event.x // 40
        y = event.y // 40
        if self.obstacle_mode:
            cell = self.grid[x][y]
            cell.obstacle = not cell.obstacle
            self.draw_cell(cell)
        else:
            if self.start is None:
                self.start = self.grid[x][y]
                self.draw_cell(self.start, 'green')
            elif self.target is None:
                self.target = self.grid[x][y]
                self.draw_cell(self.target, 'red')
            else:
                self.reset_start_target()

    def draw_cell(self, cell, color_name=None):
        if color_name:
            self.canvas.itemconfig(self.canvas.create_rectangle(cell.x * 40, cell.y * 40, (cell.x + 1) * 40, (cell.y + 1) * 40, fill=color_name))
        else:
            self.canvas.itemconfig(self.canvas.create_rectangle(cell.x * 40, cell.y * 40, (cell.x + 1) * 40, (cell.y + 1) * 40, fill='white' if not cell.obstacle else 'black'))

    def find_path(self):
        if self.start is None or self.target is None:
            messagebox.showinfo('Error', 'Please select start and target cells.')
            return

        self.path.clear()
        open_set = [self.start]
        closed_set = []

        while open_set:
            current = min(open_set, key=lambda x: x.f)
            open_set.remove(current)
            closed_set.append(current)

            if current == self.target:
                self.path.append(current)
                while current.parent:
                    self.path.append(current.parent)
                    current = current.parent
                self.highlight_path()
                return

            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                if neighbor in closed_set or neighbor.obstacle:
                    continue

                tentative_g = current.g + 1
                if neighbor not in open_set or tentative_g < neighbor.g:
                    neighbor.parent = current
                    neighbor.g = tentative_g
                    neighbor.h = self.distance(neighbor, self.target)
                    neighbor.f = neighbor.g + neighbor.h
                    if neighbor not in open_set:
                        open_set.append(neighbor)

        messagebox.showinfo('No Path', 'No path found!')

    def get_neighbors(self, cell):
        neighbors = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            nx, ny = cell.x + dx, cell.y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                neighbors.append(self.grid[nx][ny])
        return neighbors

    def distance(self, cell1, cell2):
        return abs(cell1.x - cell2.x) + abs(cell1.y - cell2.y)

    def highlight_path(self):
        for cell in self.path:
            self.draw_cell(cell, 'yellow')

def main():
    root = tk.Tk()
    root.title('A* Search Pathfinding')
    size = 10  # Adjust grid size here
    astar_gui = AStarGUI(root, size)
    root.mainloop()

if __name__ == "__main__":
    main()