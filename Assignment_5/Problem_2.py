import tkinter as tk
import heapq

class Cell:
    def __init__(self, x, y, obstacle=False):
        self.x = x
        self.y = y
        self.obstacle = obstacle
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

class RatPathFinderGUI:
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
        self.canvas = tk.Canvas(self.master, width=self.size * 40, height=self.size * 40)
        self.canvas.pack()
        self.create_grid()
        self.canvas.bind('<Button-1>', self.handle_click)
        self.add_obstacle_button = tk.Button(self.master, text='Add Obstacles', command=self.toggle_obstacle_mode)
        self.add_obstacle_button.pack()
        self.find_path_button = tk.Button(self.master, text='Find Path', command=self.find_path)
        self.find_path_button.pack()

    def create_grid(self):
        for x in range(self.size):
            for y in range(self.size):
                self.draw_cell(self.grid[x][y])

    def draw_cell(self, cell, color=None):
        fill_color = 'white' if not cell.obstacle else 'black'
        if color:
            fill_color = color
        self.canvas.itemconfig(self.canvas.create_rectangle(cell.x * 40, cell.y * 40, (cell.x + 1) * 40, (cell.y + 1) * 40, fill=fill_color))

    def toggle_obstacle_mode(self):
        self.obstacle_mode = not self.obstacle_mode
        if self.obstacle_mode:
            self.add_obstacle_button.config(text='Add Start/End')
        else:
            self.add_obstacle_button.config(text='Add Obstacles')

    def handle_click(self, event):
        x = event.x // 40
        y = event.y // 40
        cell = self.grid[x][y]
        if self.obstacle_mode:
            cell.obstacle = not cell.obstacle
            self.draw_cell(cell)
        else:
            if cell.obstacle:
                return
            if self.start is None:
                self.start = cell
                self.draw_cell(cell, 'green')
            elif self.target is None:
                self.target = cell
                self.draw_cell(cell, 'red')

    def find_path(self):
        if self.start is None or self.target is None:
            tk.messagebox.showinfo('Error', 'Please select start and target cells.')
            return

        self.path.clear()
        open_set = [(0, self.start)]
        closed_set = set()

        while open_set:
            current = open_set[0][1]

            if current == self.target:
                self.path.append(current)
                while current.parent:
                    self.path.append(current.parent)
                    current = current.parent
                self.highlight_path()
                return

            if current in closed_set:
                heapq.heappop(open_set)
                continue

            closed_set.add(current)

            for neighbor in self.get_neighbors(current):
                if neighbor.obstacle or neighbor in closed_set:
                    continue

                tentative_g = current.g + 1
                if (tentative_g, neighbor) not in open_set:
                    neighbor.parent = current
                    neighbor.g = tentative_g
                    neighbor.h = self.distance(neighbor, self.target)
                    heapq.heappush(open_set, (neighbor.g + neighbor.h, neighbor))

            heapq.heappop(open_set)

        tk.messagebox.showinfo('No Path', 'No path found!')

    def get_neighbors(self, cell):
        x, y = cell.x, cell.y
        neighbors = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
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
    root.title('Rat Path Finder')
    size = 10  # Adjust grid size here
    rat_path_finder_gui = RatPathFinderGUI(root, size)
    root.mainloop()

if __name__ == "__main__":
    main()
