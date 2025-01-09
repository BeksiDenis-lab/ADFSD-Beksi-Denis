import tkinter as tk
from tkinter import ttk
import random
import time

# Helper function for generating colors
def generate_colors(array, current_index, next_index):
    colors = []
    for index in range(len(array)):
        if index == current_index or index == next_index:
            colors.append("red")
        else:
            colors.append("blue")
    return colors

# Sorting Algorithms
def bubble_sort(array, draw_func, delay):
    n = len(array)
    for i in range(n):
        for j in range(n - i - 1):
            draw_func(array, generate_colors(array, j, j + 1))
            time.sleep(delay)
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    draw_func(array, ["green" for _ in range(len(array))])

def insertion_sort(array, draw_func, delay):
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and key < array[j]:
            draw_func(array, generate_colors(array, j, j + 1))
            time.sleep(delay)
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
        draw_func(array, ["green" if index <= i else "blue" for index in range(len(array))])
    draw_func(array, ["green" for _ in range(len(array))])

def selection_sort(array, draw_func, delay):
    for i in range(len(array)):
        min_idx = i
        for j in range(i + 1, len(array)):
            draw_func(array, generate_colors(array, j, min_idx))
            time.sleep(delay)
            if array[j] < array[min_idx]:
                min_idx = j
        array[i], array[min_idx] = array[min_idx], array[i]
        draw_func(array, ["green" if index <= i else "blue" for index in range(len(array))])
    draw_func(array, ["green" for _ in range(len(array))])

# Visualization GUI
def draw_data(array, color_array):
    canvas.delete("all")
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    bar_width = canvas_width / len(array)
    for i, value in enumerate(array):
        x0 = i * bar_width
        y0 = canvas_height - (value / max(array) * canvas_height)
        x1 = (i + 1) * bar_width
        y1 = canvas_height
        canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i])
    root.update_idletasks()

def generate_data():
    global data
    data = [random.randint(1, 100) for _ in range(size.get())]
    draw_data(data, ["blue" for _ in range(len(data))])

def start_sorting():
    if algo_menu.get() == "Bubble Sort":
        bubble_sort(data, draw_data, speed.get())
    elif algo_menu.get() == "Insertion Sort":
        insertion_sort(data, draw_data, speed.get())
    elif algo_menu.get() == "Selection Sort":
        selection_sort(data, draw_data, speed.get())

# Main Application
root = tk.Tk()
root.title("Sorting Algorithm Visualizer")
root.geometry("900x600")

# Variables
data = []
speed = tk.DoubleVar(value=0.1)
size = tk.IntVar(value=30)

# UI Frame
ui_frame = tk.Frame(root, width=900, height=200, bg="grey")
ui_frame.grid(row=0, column=0, padx=10, pady=5)

# Canvas
canvas = tk.Canvas(root, width=900, height=400, bg="white")
canvas.grid(row=1, column=0, padx=10, pady=5)

# UI Elements
algo_label = tk.Label(ui_frame, text="Algorithm: ", bg="grey")
algo_label.grid(row=0, column=0, padx=5, pady=5)
algo_menu = ttk.Combobox(ui_frame, values=["Bubble Sort", "Insertion Sort", "Selection Sort"], state="readonly")
algo_menu.grid(row=0, column=1, padx=5, pady=5)
algo_menu.current(0)

speed_label = tk.Label(ui_frame, text="Speed: ", bg="grey")
speed_label.grid(row=1, column=0, padx=5, pady=5)
speed_scale = tk.Scale(ui_frame, from_=0.01, to=1.0, length=200, digits=2, resolution=0.01, orient=tk.HORIZONTAL, variable=speed)
speed_scale.grid(row=1, column=1, padx=5, pady=5)

size_label = tk.Label(ui_frame, text="Size: ", bg="grey")
size_label.grid(row=2, column=0, padx=5, pady=5)
size_scale = tk.Scale(ui_frame, from_=5, to=100, length=200, digits=2, resolution=1, orient=tk.HORIZONTAL, variable=size)
size_scale.grid(row=2, column=1, padx=5, pady=5)

generate_button = tk.Button(ui_frame, text="Generate", command=generate_data, bg="lightblue")
generate_button.grid(row=0, column=2, padx=5, pady=5)
start_button = tk.Button(ui_frame, text="Start", command=start_sorting, bg="green")
start_button.grid(row=1, column=2, padx=5, pady=5)

root.mainloop()