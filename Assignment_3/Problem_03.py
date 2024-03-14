import tkinter as tk
from tkinter import messagebox, ttk
import random
import math

class TSPSolver:
    def __init__(self, cities, connect_to_first=True):
        self.cities = cities
        self.connect_to_first = connect_to_first
        self.num_cities = len(cities)
        self.best_path = None
        self.best_distance = float('inf')
        self.distances = [[0] * self.num_cities for _ in range(self.num_cities)]

    def distance(self, city1, city2):
        # Calculate Euclidean distance between two cities
        x1, y1 = city1
        x2, y2 = city2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def calculate_distances(self):
        for i in range(self.num_cities):
            for j in range(self.num_cities):
                self.distances[i][j] = self.distance(self.cities[i], self.cities[j])

    def total_distance(self, path):
        # Calculate the total distance of a given path
        total = 0
        for i in range(self.num_cities - 1):
            total += self.distances[path[i]][path[i + 1]]
        if self.connect_to_first:
            total += self.distances[path[-1]][path[0]]  # Return to starting city
        return total

    def hill_climbing(self):
        # Hill climbing algorithm to find the shortest path
        current_path = list(range(self.num_cities))
        random.shuffle(current_path)
        current_distance = self.total_distance(current_path)

        while True:
            neighbor_path = current_path[:]
            # Swap two random cities in the path
            idx1, idx2 = random.sample(range(self.num_cities), 2)
            neighbor_path[idx1], neighbor_path[idx2] = neighbor_path[idx2], neighbor_path[idx1]

            neighbor_distance = self.total_distance(neighbor_path)
            if neighbor_distance < current_distance:
                current_path = neighbor_path
                current_distance = neighbor_distance
            else:
                break

        if current_distance < self.best_distance:
            self.best_path = current_path
            self.best_distance = current_distance

        return self.best_path, self.best_distance


class TSPVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TSP Solver with Hill Climbing")

        self.canvas = tk.Canvas(root, width=600, height=600, bg="white")
        self.canvas.pack()
        
        self.draw_grid()

        self.cities = []
        self.labels = []
        self.solver = None
        self.connect_checkbox_var = tk.BooleanVar()
        self.connect_checkbox_var.set(True)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.solve_button = tk.Button(root, text="Solve", command=self.solve)
        self.reset_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.solve_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.connect_checkbox = ttk.Checkbutton(root, text="Connect Last City to First", variable=self.connect_checkbox_var)
        self.connect_checkbox.pack(side=tk.BOTTOM, padx=10, pady=10)

        self.canvas.bind("<Button-1>", self.add_city)

        self.info_text = tk.Text(root, height=10, width=40)
        self.info_text.pack(side=tk.BOTTOM, padx=10, pady=10)

    def draw_grid(self):
        for i in range(0, 601, 50):
            self.canvas.create_line(i, 0, i, 600, fill="gray", dash=(2, 2))
            self.canvas.create_line(0, i, 600, i, fill="gray", dash=(2, 2))

    def add_city(self, event):
        x, y = event.x, event.y
        x = (x // 50) * 50 + 25  # Snap to grid
        y = (y // 50) * 50 + 25  # Snap to grid
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="black")
        self.cities.append((x, y))

        city_label = f"City {len(self.cities)}"
        label = self.canvas.create_text(x, y - 15, text=city_label)
        self.labels.append(label)

        self.update_distances()

    def update_distances(self):
        self.solver = TSPSolver(self.cities, self.connect_checkbox_var.get())
        self.solver.calculate_distances()

        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, "Distances between cities:\n")
        for i in range(len(self.cities)):
            for j in range(i + 1, len(self.cities)):
                dist = self.solver.distances[i][j]
                self.info_text.insert(tk.END, f"City {i+1} to City {j+1}: {dist:.2f}\n")

    def solve(self):
        if len(self.cities) < 2:
            messagebox.showerror("Error", "Add at least 2 cities.")
            return

        best_path, best_distance = self.solver.hill_climbing()

        # Clear canvas
        self.canvas.delete("all")
        self.draw_grid()
        
        # Draw all possible routes in grey
        for i in range(len(self.cities)):
            for j in range(i + 1, len(self.cities)):
                x1, y1 = self.cities[i]
                x2, y2 = self.cities[j]
                if (self.cities[i], self.cities[j]) in zip(best_path, best_path[1:] + [best_path[0]]) or (self.cities[j], self.cities[i]) in zip(best_path, best_path[1:] + [best_path[0]]):
                    self.canvas.create_line(x1, y1, x2, y2, fill="green", width=2)
                else:
                    self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=1)

        # Highlight the optimal path in green
        for i in range(len(best_path) - 1):
            x1, y1 = self.cities[best_path[i]]
            x2, y2 = self.cities[best_path[i + 1]]
            self.canvas.create_line(x1, y1, x2, y2, fill="green", width=2)
        if self.connect_checkbox_var.get():
            x1, y1 = self.cities[best_path[-1]]
            x2, y2 = self.cities[best_path[0]]
            self.canvas.create_line(x1, y1, x2, y2, fill="green", width=2)

        # Display shortest distance
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, f"Shortest Distance: {best_distance}\n")
        self.info_text.insert(tk.END, "Distances between cities:\n")
        for i in range(len(self.cities)):
            for j in range(i + 1, len(self.cities)):
                dist = self.solver.distances[i][j]
                self.info_text.insert(tk.END, f"City {i+1} to City {j+1}: {dist:.2f}\n")

    def reset(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.cities = []
        self.labels = []
        self.solver = None
        self.info_text.delete("1.0", tk.END)
        

if __name__ == "__main__":
    root = tk.Tk()
    app = TSPVisualizerApp(root)
    root.mainloop()
