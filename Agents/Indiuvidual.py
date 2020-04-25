import numpy as np

class Indiuvidual:

    def __init__(self, canvas, canvas_object_type, coord_x, coord_y, color, xspeed, yspeed, ball_size,
                 social_distance_factor=None):
        self.canvas = canvas
        self.ball_size = ball_size
        self.id_on_canvas = self.canvas.create_oval(coord_x, coord_y, coord_x + self.ball_size,
                                                    coord_y + self.ball_size, fill='green', outline='green')
        self.canvas_object_type = canvas_object_type
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.social_distance_factor = social_distance_factor
        self.color = color
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.health_state = 'healthy'
        self.infection_probability = 0.0

    def move(self, coord_x=None, coord_y=None):
        if coord_x is None and coord_y is None:

            pos = self.canvas.coords(self.id_on_canvas)  # left, top, right, bottom
            if len(pos) > 0:
                if pos[2] >= self.canvas.winfo_width():
                    self.xspeed *= -1

                if pos[0] <= 0:
                    self.xspeed *= -1

                if pos[1] <= 0:
                    self.yspeed *= -1

                if pos[3] >= self.canvas.winfo_height():
                    self.yspeed *= -1

                elif self.coinFlip(0.04) == 1:
                    xdir = -1 if self.coinFlip(0.5) == 0 else 1
                    ydir = -1 if self.coinFlip(0.5) == 0 else 1
                    self.xspeed = self.xspeed * xdir
                    self.yspeed = self.yspeed * ydir

        self.canvas.move(self.id_on_canvas, self.xspeed, self.yspeed)

    def coinFlip(self, p):
        # perform the binomial distribution (returns 0 or 1)
        result = np.random.binomial(1, p)

        # return flip to be added to numpy array
        return result