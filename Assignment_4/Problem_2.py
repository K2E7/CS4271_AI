import tkinter as tk
from tkinter import messagebox
import random
import math

class MonkeyRoomGUI:
    def __init__(self, master, width, height):
        self.master = master
        self.width = width
        self.height = height
        self.cell_size = 50
        self.canvas_width = width * self.cell_size
        self.canvas_height = height * self.cell_size
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.create_grid()
        self.monkey_id = None
        self.box_id = None
        self.banana_id = None
        self.reset_button = tk.Button(master, text="Reset", command=self.reset)
        self.reset_button.pack()
        self.solve_button = tk.Button(master, text="Solve", command=self.solve)
        self.solve_button.pack()
        self.moves_text = tk.Text(master, height=5, width=30)
        self.moves_text.pack()

        self.reset()

    def create_grid(self):
        for i in range(0, self.canvas_width, self.cell_size):
            self.canvas.create_line(i, 0, i, self.canvas_height, fill='black')
        for j in range(0, self.canvas_height, self.cell_size):
            self.canvas.create_line(0, j, self.canvas_width, j, fill='black')

    def reset(self):
        self.canvas.delete('monkey', 'box', 'banana')

        self.monkey_x = 0
        self.monkey_y = 0
        self.banana_x = random.randint(0, self.width - 1)
        self.banana_y = random.randint(0, self.height - 1)
        self.box_x = random.randint(0, self.width - 1)
        self.box_y = 0

        self.monkey_id = self.canvas.create_polygon((self.monkey_x + 0.2) * self.cell_size, (self.monkey_y + 0.2) * self.cell_size,
                                                    (self.monkey_x + 0.8) * self.cell_size, (self.monkey_y + 0.2) * self.cell_size,
                                                    (self.monkey_x + 1) * self.cell_size, (self.monkey_y + 0.5) * self.cell_size,
                                                    (self.monkey_x + 0.8) * self.cell_size, (self.monkey_y + 0.8) * self.cell_size,
                                                    (self.monkey_x + 0.2) * self.cell_size, (self.monkey_y + 0.8) * self.cell_size,
                                                    fill='brown', outline='black', tags='monkey')
        self.box_id = self.canvas.create_rectangle((self.box_x + 0.2) * self.cell_size, (self.box_y + 0.6) * self.cell_size,
                                                    (self.box_x + 0.8) * self.cell_size, (self.box_y + 0.8) * self.cell_size, fill='gray', tags='box')
        self.banana_id = self.canvas.create_oval((self.banana_x + 0.2) * self.cell_size, (self.banana_y + 0.2) * self.cell_size,
                                                  (self.banana_x + 0.8) * self.cell_size, (self.banana_y + 0.8) * self.cell_size, fill='yellow', tags='banana')

    def move_monkey(self, dx, dy, move_text):
        new_x = self.monkey_x + dx
        new_y = self.monkey_y + dy
        if 0 <= new_x < self.width and 0 <= new_y < self.height:
            self.monkey_x = new_x
            self.monkey_y = new_y
            self.canvas.move('monkey', dx * self.cell_size, dy * self.cell_size)
            self.moves_text.insert(tk.END, move_text + "\n")

    def push_box(self):
        if abs(self.box_x - self.monkey_x) == 1 and self.box_y == 0:
            if self.box_x < self.monkey_x:
                self.box_x -= 1
            else:
                self.box_x += 1
            self.canvas.move('box', (self.box_x - self.monkey_x) * self.cell_size, 0)
            self.moves_text.insert(tk.END, "Pushed box\n")

    def climb_box(self):
        if self.monkey_x == self.box_x and self.monkey_y == 0:
            self.monkey_y += 1
            self.canvas.move('monkey', 0, self.cell_size)
            self.moves_text.insert(tk.END, "Climbed box\n")

    def grab_banana(self):
        if self.monkey_x == self.banana_x and self.monkey_y == self.banana_y:
            self.canvas.delete('banana')
            self.moves_text.insert(tk.END, "Grabbed banana\n")
            messagebox.showinfo("Message", "Banana grabbed successfully!")
        else:
            self.moves_text.insert(tk.END, "No steps available\n")
            messagebox.showinfo("Message", "No steps available!")

    def is_banana_reachable(self):
        return abs(self.banana_x - self.monkey_x) <= 1 and abs(self.banana_y - self.monkey_y) <= 1

    def solve(self):
        if self.is_banana_reachable():
            if self.banana_y == 1:  # Banana is above monkey
                self.push_box()
                self.climb_box()
                self.move_monkey(self.banana_x - self.monkey_x, self.banana_y - self.monkey_y, "Grabbed banana")
            else:  # Banana is reachable directly
                self.move_monkey(self.banana_x - self.monkey_x, self.banana_y - self.monkey_y, "Grabbed banana")
        else:
            messagebox.showinfo("Message", "Banana is unreachable!")
            self.moves_text.insert(tk.END, "Banana is unreachable\n")

# Create the GUI
root = tk.Tk()
root.title("Monkey and Banana")

monkey_room_gui = MonkeyRoomGUI(root, 5, 2)  # Create a 5x2 grid for the room

root.mainloop()
