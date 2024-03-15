import tkinter as tk

class EightQueensGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Eight Queens Problem")
        self.size = 8
        self.solution_generator = self.find_all_solutions()
        self.canvas = tk.Canvas(self.root, width=self.size * 50, height=self.size * 50, bg="white")
        self.canvas.pack()
        self.draw_board()
        
        self.solution_label = tk.Label(self.root, text="Solution: ")
        self.solution_label.pack()
        
        self.prev_button = tk.Button(self.root, text="Previous Solution", command=self.compute_previous_solution)
        self.prev_button.pack(side=tk.LEFT)
        
        self.next_button = tk.Button(self.root, text="Next Solution", command=self.compute_next_solution)
        self.next_button.pack(side=tk.RIGHT)

        self.current_solution_index = 0
        self.solutions = []
        self.populate_solutions()
        self.display_current_solution()

    def draw_board(self):
        for i in range(self.size):
            for j in range(self.size):
                color = "white" if (i + j) % 2 == 0 else "gray"
                self.canvas.create_rectangle(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill=color)

    def draw_queens(self, queens):
        self.canvas.delete("queen")
        for row, col in enumerate(queens):
            self.canvas.create_text(col * 50 + 25, row * 50 + 25, text="♕", font=("Arial", 24), tag="queen")

    def is_safe(self, queens, row, col):
        for r, c in enumerate(queens):
            if c == col or abs(row - r) == abs(col - c):
                return False
        return True

    def solve(self, queens, row=0):
        if row == self.size:
            yield queens
        else:
            for col in range(self.size):
                if self.is_safe(queens, row, col):
                    yield from self.solve(queens + [col], row + 1)

    def find_all_solutions(self):
        yield from self.solve([])

    def populate_solutions(self):
        for solution in self.solution_generator:
            self.solutions.append(solution)

    def display_current_solution(self):
        self.draw_queens(self.solutions[self.current_solution_index])
        self.solution_label.config(text="Solution: " + str(self.current_solution_index + 1) + "/" + str(len(self.solutions)))

    def compute_previous_solution(self):
        if self.current_solution_index > 0:
            self.current_solution_index -= 1
            self.display_current_solution()

    def compute_next_solution(self):
        if self.current_solution_index < len(self.solutions) - 1:
            self.current_solution_index += 1
            self.display_current_solution()

    def run(self):
        self.root.mainloop()


def main():
    EightQueensGUI().run()


if __name__ == "__main__":
    main()
