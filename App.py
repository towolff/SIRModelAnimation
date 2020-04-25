import numpy as np

from UI.GUI import GUI
from Agents.Indiuvidual import Indiuvidual


class MyApp:

    def __init__(self, title, num_balls, ball_size, max_ball_speed):
        self.Height = 1024
        self.Width = 1024
        self.ui = GUI(Height=self.Height, Width=self.Width, title=title)
        self.num_balls = num_balls
        self.ball_size = ball_size
        self.max_ball_speed = max_ball_speed
        self.individuals = []
        self.init_ui()

    def init_ui(self):
        for ball in range(self.num_balls):
            height_rand = np.random.randint(0, self.Height - self.ball_size)
            width_rand = np.random.randint(0, self.Width - self.ball_size)
            rand_speed = np.random.randint(1, self.max_ball_speed)

            agent = Indiuvidual(canvas=self.ui.canvas, canvas_object_type='oval', coord_x=height_rand,
                                ball_size=self.ball_size, coord_y=width_rand, color='green',
                                xspeed=rand_speed, yspeed=rand_speed)

            self.individuals.append(agent)

    def start(self):
        self.ui.start_animation()








