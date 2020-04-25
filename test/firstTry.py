from tkinter import *
import time
import numpy as np

tk = Tk()

Height = 1024
Width = 1024

canvas = Canvas(tk, width=Width, height=Height)
tk.title('First GUI')
canvas.pack()


num_balls = 100
balls_dict = {
    'balls': [],
    'xspeed': [],
    'yspeed': []
}

size = 20
max_speed = 3
for i in range(num_balls):
    height_rand = np.random.randint(0, Height-size)
    width_rand = np.random.randint(0, Width-size)

    balls_dict['balls'].append(canvas.create_oval(height_rand, width_rand, height_rand+size, width_rand+size, fill='green', outline='green'))
    rand_speed = np.random.randint(1, max_speed)
    balls_dict['xspeed'].append(rand_speed)
    balls_dict['yspeed'].append(rand_speed)


def coinFlip(p):
    # perform the binomial distribution (returns 0 or 1)
    result = np.random.binomial(1, p)

    # return flip to be added to numpy array
    return result


i = 0

while True:
    for j, ball in enumerate(balls_dict['balls']):
        canvas.move(ball, balls_dict['xspeed'][j], balls_dict['yspeed'][j])
        pos = canvas.coords(ball) #left, top, right, bottom

        if pos[2]>=Width:
            balls_dict['xspeed'][j] *= -1

        if pos[0]<=0:
            balls_dict['xspeed'][j] *= -1

        if pos[1] <=0:
            balls_dict['yspeed'][j] *= -1

        if pos[3] >=Height:
            balls_dict['yspeed'][j] *= -1

        tk.update()
        #time.sleep(0.00006)

        if coinFlip(0.04) == 1:
            xdir = -1 if coinFlip(0.5) == 0 else 1
            ydir = -1 if coinFlip(0.5) == 0 else 1
            balls_dict['xspeed'][j] = balls_dict['xspeed'][j] * xdir
            balls_dict['yspeed'][j] = balls_dict['yspeed'][j] * ydir

    i += 1
