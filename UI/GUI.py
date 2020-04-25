from tkinter import *
import time
import numpy as np


class GUI:
    def __init__(self, Height, Width, title, btn1_fnct, btn2_fnct, btn3_fnct):
        self.tk = Tk()
        self.active = True
        self._init_upper_ui()
        self._init_canvas(Height, Width)
        self._init_upper_button(btn1_fnct, btn2_fnct, btn3_fnct)
        self.tk.title(title)
        self.tk.geometry('{}x{}'.format(Height, Width))

    def _init_upper_ui(self):
        self.num_balls_text = StringVar(value=100)
        self.num_balls_label = Label(self.tk, text='Individuals:', font=('bold', 14), pady=20)
        self.num_balls_label.grid(row=0, column=0, sticky=E)
        self.num_balls_entry = Entry(self.tk, textvariable=self.num_balls_text)
        self.num_balls_entry.grid(row=0, column=1, sticky=E)

        self.ball_speed_text = StringVar(value=5)
        self.ball_speed_label = Label(self.tk, text='Max. Ball Speed:', font=('bold', 14), pady=20, padx=20)
        self.ball_speed_label.grid(row=0, column=2, sticky=E)
        self.ball_speed_entry = Entry(self.tk, textvariable=self.ball_speed_text)
        self.ball_speed_entry.grid(row=0, column=3, sticky=E)

        self.ball_size_text = StringVar(value=10)
        self.ball_size_label = Label(self.tk, text='Ball Size:', font=('bold', 14), pady=20, padx=20)
        self.ball_size_label.grid(row=0, column=4, sticky=E)
        self.ball_size_entry = Entry(self.tk, textvariable=self.ball_size_text)
        self.ball_size_entry.grid(row=0, column=5, sticky=E)

    def _init_upper_button(self, btn1_fnct, btn2_fnct, btn3_fnct):
        self.load_config_btn = Button(master=self.tk, text='Load Config', command=btn1_fnct)
        self.load_config_btn.grid(row=1, column=0)

        self.reset_config_btn = Button(master=self.tk, text='Reset Config', command=btn2_fnct)
        self.reset_config_btn.grid(row=1, column=1)

        self.start_animation_btn = Button(master=self.tk, text='Start Animation', command=btn3_fnct)
        self.start_animation_btn.grid(row=1, column=2)

    def _init_canvas(self, Height, Width):
        self.canvas = Canvas(self.tk, width=Width - (Width / 100 * 10), height=Height - (Height / 100 * 10),
                             highlightthickness=2, highlightbackground="black")
        self.canvas.grid(row=2, column=0, columnspan=6, rowspan=6, pady=10, padx=20)

    def _clear_canvas(self):
        self.canvas.delete("all")

    def start_animation(self):
        print('Hi!!')
        while self.active:
            self.tk.update_idletasks()
            self.tk.update()