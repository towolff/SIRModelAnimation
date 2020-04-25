from tkinter import *
import time
import numpy as np


class GUI:
    def __init__(self, Height, Width, title):
        self.tk = Tk()
        self.active = True
        self.canvas = Canvas(self.tk, width=Width, height=Height)
        self.tk.title(title)
        self.canvas.pack()

    def start_animation(self):
        while self.active:
            self.tk.update_idletasks()
            self.tk.update()