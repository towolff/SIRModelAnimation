import numpy as np

from UI.GUI import GUI
from Agents.Indiuvidual import Indiuvidual
from InfectionController.InfectionController import InfectionController


class MyApp:

    def __init__(self, title, num_balls, ball_size, max_ball_speed):
        self.Height = 800
        self.Width = 800
        self.infection_controller = InfectionController(num_balls)
        self.ui = GUI(app=self, height=self.Height, width=self.Width, title=title, start_animation_funct=self.init_ui,
                      restet_animation_fnct=self._delete_individuals, start_infection_fnct=self.start_infection)
        self.num_balls = num_balls
        self.ball_size = ball_size
        self.max_ball_speed = max_ball_speed
        self.individuals = []

    def init_ui(self):

        self.num_balls = int(self.ui.num_balls_entry.get())
        self.max_ball_speed = int(self.ui.ball_speed_entry.get())

        for ball in range(self.num_balls):
            height_rand = np.random.randint(0, self.Height - self.ball_size)
            width_rand = np.random.randint(0, self.Width - self.ball_size)
            rand_speed = np.random.randint(1, self.max_ball_speed)

            agent = Indiuvidual(canvas=self.ui.canvas, canvas_object_type='oval', coord_x=height_rand,
                                ball_size=self.ball_size, coord_y=width_rand, color='green',
                                xspeed=rand_speed, yspeed=rand_speed)

            self.individuals.append(agent)

        self.infection_controller.set_individuals(self.individuals)

    def _delete_individuals(self):
        self.ui.canvas.delete('all')
        self.individuals = None
        self.individuals = []

    def move_individuals(self):
        for ind in self.individuals:
            ind.move()
            self.ui.tk.update()

    def start_infection(self):
        infetected_ind = self.infection_controller.start_infection()

        for ind in infetected_ind:
            self.ui.canvas.itemconfig(ind.id_on_canvas, fill='red', outline='red')

    def start(self):
        self.ui.tk.mainloop()







