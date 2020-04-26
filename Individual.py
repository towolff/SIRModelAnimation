import math
import numpy as np


class Individual:
    def __init__(self,i, posx, posy, objx, objy, v, recover_time, fixedQuarantine):
        self.velociety = v
        self.objx = objx
        self.objy = objy
        self.idx = i
        self.name = "Individual " + str(i)
        self.infected = False
        self.susceptible = True
        self.removed = False
        self.posx = posx
        self.posy = posy
        self.fixedQuarantine = fixedQuarantine

        # displacement per iteration
        if self.fixedQuarantine or self.removed:
            self.deltax = 0
            self.deltay = 0
        else:
            self.deltax = (self.objx - self.posx) / self.velociety
            self.deltay = (self.objy - self.posy) / self.velociety
        # time in which the individual was infected
        self.infection_time = -1
        # time that the infection lasts, recover time
        self.recover_time = recover_time

    def __str__(self):
        return self.name + " on position (" + str(self.posx) + ", " + str(self.posy) + ")"

    def infect(self, i):
        # infect
        self.infected = True
        self.susceptible = False
        self.removed = False
        self.infection_time = i

    def remove(self):
        # heal/ remove
        self.removed = True
        self.susceptible = False
        self.infected = False

    def move(self, objx, objy):
        # this function is used to create a new target position
        self.objx = objx
        self.objy = objy
        if self.fixedQuarantine:
            self.deltax = 0
            self.deltay = 0
        else:
            self.deltax = (self.objx - self.posx) / self.velociety
            self.deltay = (self.objy - self.posy) / self.velociety

    def check_infection(self, i):
        # this function is used to remove the person if the established infection time has passed
        if self.infection_time > -1:
            if i - self.infection_time > self.recover_time:
                self.remove()

    def update_pos(self, n_posx, n_posy):
        # this funcion animates the movement
        if n_posx == 0 and n_posy == 0:
            self.posx = self.posx + self.deltax
            self.posy = self.posy + self.deltay
        else:
            self.posx = n_posx
            self.posy = n_posy

        if abs(self.posx-self.objx) < 3 and abs(self.posy-self.objy) < 3:
            self.move(np.random.random() * 100, np.random.random() * 100)
        if self.posx > 100:
            self.posx = 100
        if self.posy > 100:
            self.posy = 100
        if self.posx < 0:
            self.posx = 0
        if self.posy < 0:
            self.posy = 0

    def get_color(self):
        if self.infected:
            return 'red'
        if self.susceptible:
            return 'blue'
        if self.removed:
            return 'gray'

    def get_pos(self):
        return self.posx, self.posy

    def get_dist(self, x, y):
        # this funcion calculates the distance between this person an another.
        return math.sqrt((self.posx-x)**2+(self.posy-y)**2)
