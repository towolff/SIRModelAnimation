

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

    def move(self, coord_x, coord_y):
        pass