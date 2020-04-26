import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from Simulation import SIRSimulation
import numpy as np


class MyApp:

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry('{}x{}'.format(1000, 800))
        self.root.wm_title("SIR Model Animation")
        self.simulation = None
        self.canvas = None
        self._init_ui()
        self.root.mainloop()
        self.topFrame = None
        self.bottomFrame = None

    def _init_ui(self):
        self.topFrame = tkinter.Frame(self.root)
        self.bottomFrame = tkinter.Frame(self.root)
        self.topFrame.pack(side=tkinter.TOP)
        self.bottomFrame.pack(side=tkinter.BOTTOM,  fill=tkinter.BOTH, expand=True)
        self.btnStartStopText = tkinter.StringVar()
        self.btnStartStopText.set('Pause')
        self.btnLoad = tkinter.Button(master=self.root, text='Load', command=self.load_simulation)
        self.btnStart = tkinter.Button(master=self.root, text='Start', command=self.run_simulation)
        self.btnStop = tkinter.Button(master=self.root, textvariable=self.btnStartStopText, command=self.stop_cont_simulation)
        self.btnStop.pack(in_=self.bottomFrame, side=tkinter.BOTTOM)
        self.btnStart.pack(in_=self.bottomFrame, side=tkinter.BOTTOM)
        self.btnLoad.pack(in_=self.bottomFrame, side=tkinter.BOTTOM)

    def load_simulation(self):
        if self.simulation is None:
            self.simulation = SIRSimulation()
            self.canvas = FigureCanvasTkAgg(self.simulation.fig, master=self.root)  # A tk.DrawingArea.
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(in_=self.topFrame, side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    def run_simulation(self):
        if not self.simulation.isRunning:
            self.simulation.run()

    def stop_cont_simulation(self):
        if self.simulation.isRunning:
            self.simulation.pause_simualtion()
            self.btnStartStopText.set('Continue')
        elif self.simulation.wasStarted:
            self.simulation.continue_simulation()
            self.btnStartStopText.set('Pause')


if __name__ == '__main__':
    app = MyApp()
