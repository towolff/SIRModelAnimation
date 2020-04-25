from tkinter import *
import time
import numpy as np


class GUI:
    def __init__(self, app, height, width, title, start_animation_funct, restet_animation_fnct, start_infection_fnct):
        self.tk = Tk()
        self.app = app
        self.animation_active = False
        self._init_upper_ui()
        self._init_canvas(height, width)
        self._init_state_label()
        self._init_upper_button(start_animation_funct, restet_animation_fnct, start_infection_fnct)
        self.tk.title(title)
        self.tk.geometry('{}x{}'.format(height, width))

    def _init_upper_ui(self):
        self.num_balls_text = StringVar(value=400)
        self.num_balls_label = Label(self.tk, text='Individuals:', font=('bold', 14), pady=10)
        self.num_balls_label.grid(row=0, column=0, sticky=W)
        self.num_balls_entry = Entry(self.tk, textvariable=self.num_balls_text)
        self.num_balls_entry.grid(row=0, column=1, sticky=W)

        self.ball_speed_text = StringVar(value=5)
        self.ball_speed_label = Label(self.tk, text='Speed:', font=('bold', 14), pady=10, padx=-50)
        self.ball_speed_label.grid(row=0, column=2, sticky=W)
        self.ball_speed_entry = Entry(self.tk, textvariable=self.ball_speed_text)
        self.ball_speed_entry.grid(row=0, column=3, sticky=W)

    def _init_upper_button(self, btn1_fnct, btn2_fnct, btn3_fnct):
        self.load_config_btn = Button(master=self.tk, text='Load Config', command=btn1_fnct)
        self.load_config_btn.grid(row=1, column=0)

        self.reset_config_btn = Button(master=self.tk, text='Reset Config', command=btn2_fnct)
        self.reset_config_btn.grid(row=1, column=1)

        self.start_animation_btn = Button(master=self.tk, text='Start Animation', command=self.start_animation)
        self.start_animation_btn.grid(row=1, column=2)

        self.stop_animation_btn = Button(master=self.tk, text='Stop Animation', command=self.stop_animation)
        self.stop_animation_btn.grid(row=1, column=3)

        self.start_infection_btn = Button(master=self.tk, text='Start Infection', command=btn3_fnct)
        self.start_infection_btn.grid(row=2, column=0)

    def _init_state_label(self):
        string_susceptible = 'Susceptible: {}'.format(self.app.infection_controller.current_healthy)
        self.susceptible_text = Label(self.tk, text=string_susceptible)
        self.susceptible_text.grid(row=2, column=1, pady=10)

        string_infected = 'Infected: {}'.format(self.app.infection_controller.current_infected)
        self.infected_text = Label(self.tk, text=string_infected)
        self.infected_text.grid(row=2, column=2)

        string_removed = 'Removed: {}'.format(self.app.infection_controller.current_removed)
        self.removed_text = Label(self.tk, text=string_removed)
        self.removed_text.grid(row=2, column=3)

    def _init_canvas(self, height, width):
        self.canvas = Canvas(self.tk, width=width - (width / 100 * 10), height=height - (height / 100 * 20),
                             highlightthickness=2, highlightbackground="black")
        self.canvas.grid(row=3, column=0, columnspan=5, rowspan=5, pady=10, padx=20)

    def _clear_canvas(self):
        self.canvas.delete("all")

    def animate(self):
        while self.animation_active:
            self.app.move_individuals()
            self.tk.update()

    def start_animation(self):
        print('Started animation!')
        self.animation_active = True
        self.canvas.after(10, self.animate())

    def stop_animation(self):
        print('Stopped animation!')
        self.animation_active = False
        self.canvas.after(10, self.animate())
