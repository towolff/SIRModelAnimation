from Individual import Individual
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider


class SIRSimulation:

    def __init__(self, n_individuals=400, prct_infected=2, r_infection=2.5,
                 p_infection=6, p_quarantine=0, t_recovery=40, different_recovery_times=False):
        # SIMULATION PARAMETERS
        self.isRunning = False
        self.wasStarted = False
        self.animation = None
        self.N_INDIVIDUALS = n_individuals  # number of individuals
        self.PRCT_INFECTED = prct_infected  # percentage of infected people at the beginning of the simulation (0-100%)
        self.INFECTION_RADIUS = r_infection  # radius of transmission in pixels (0-100)
        self.INFECTION_PROBABILITY = p_infection  # probability of transmission in percentage (0-100%)
        self.P_QUARANTINE = p_quarantine  # percentage of the people in quarantine (0-100%)
        self.T_RECOVERY = t_recovery  # time taken to recover in number of frames (0-infinity)
        self.different_recovery_times = different_recovery_times  # rand recovery t for each ind btw.. 1 and t_recovery
        self.n_infected = 0
        self.individuals = []
        self._init_individuals()
        self._init_figure()

    def _init_individuals(self):
        # creating all the individuals in random positions and infecting some of them.
        for i in range(self.N_INDIVIDUALS):
            if self.different_recovery_times:
                if np.random.uniform(0, 1, 1) > 0.5:
                    recovery_time = np.random.randint(1, self.T_RECOVERY)
                else:
                    recovery_time = self.T_RECOVERY
            else:
                recovery_time = self.T_RECOVERY

            p = Individual(i, np.random.random() * 100, np.random.random() * 100,
                           np.random.random() * 100, np.random.random() * 100,
                           (np.random.random() + 0.5) * 100, recovery_time, False)

            if np.random.random() < self.PRCT_INFECTED / 100:
                p.infect(0)
                self.n_infected = self.n_infected + 1
            if np.random.random() < self.P_QUARANTINE / 100:
                p.fixedQuarantine = True

            self.individuals.append(p)

    def _init_figure(self):
        # create all the graphics
        self.fig = plt.figure(figsize=(20, 10))
        self.fig.suptitle('SIR Model Animation', fontsize=20)
        self.fig.canvas.set_window_title('SIR Model Animation')
        self.ax = self.fig.add_subplot(1, 2, 1)
        self.cx = self.fig.add_subplot(1, 2, 2)
        self.ax.axis('off')
        self.cx.axis([0, 300, 0, self.N_INDIVIDUALS])
        self.scatter = self.ax.scatter([p.posx for p in self.individuals],
                             [p.posy for p in self.individuals], c='blue', s=12)
        self.box = plt.Rectangle((0, 0), 100, 100, fill=False)
        self.ax.add_patch(self.box)
        self.cvst, = self.cx.plot(self.n_infected, color="red", label="Infected")
        self.rvst, = self.cx.plot(self.n_infected, color="gray", label="Removed")
        self.svst, = self.cx.plot(self.n_infected, color='blue', label='Susceptible')

        self.cx.legend(handles=[self.svst, self.cvst, self.rvst])
        self.cx.set_xlabel("Time")
        self.cx.set_ylabel("Individuals")

        self.list_susceptible = [self.N_INDIVIDUALS]
        self.list_infected = [self.n_infected]
        self.list_removed = [0]
        self.list_time = [0]

    def update(self, frame, removed, currently_infected, susceptible, t):
        # function excecuted frame by frame
        count_susceptible = self.N_INDIVIDUALS
        count_infected = 0
        count_removed = 0
        individual_colors = []
        individual_sizes = [12 for p in self.individuals]

        for p in self.individuals:
            # check how much time the person has been sick
            p.check_infection(frame)
            # animate the movement of each individuum
            if not p.removed:
                p.update_pos(0, 0)
            if p.removed:
                count_removed += 1  # count the amount of removed
                count_susceptible -= 1
            if p.infected:
                count_infected = count_infected + 1  # count the amount of infected
                count_susceptible -= 1
                # check for people around the sick individual and infect the ones within the
                # transmission radius given the probability
                for ind in self.individuals:
                    if ind.idx == p.idx or ind.infected or ind.removed:
                        pass
                    else:
                        d = p.get_dist(ind.posx, ind.posy)
                        if d < self.INFECTION_RADIUS:
                            if np.random.random() < self.INFECTION_PROBABILITY / 100:
                                ind.infect(frame)
                                individual_sizes[ind.idx] = 80

            individual_colors.append(p.get_color())  # change dot color according to the person's status

        # update the plotting data
        currently_infected.append(count_infected)
        removed.append(count_removed)
        susceptible.append(count_susceptible)
        t.append(frame)

        # check for termination
        self._check_for_termination(currently_infected)

        # transfer the data to the matplotlib graphics
        offsets = np.array([[p.posx for p in self.individuals], [p.posy for p in self.individuals]])
        self.scatter.set_offsets(np.ndarray.transpose(offsets))
        self.scatter.set_color(individual_colors)
        self.scatter.set_sizes(individual_sizes)
        self.cvst.set_data(t, currently_infected)
        self.rvst.set_data(t, removed)
        self.svst.set_data(t, susceptible)

        return self.scatter, self.cvst, self.rvst, self.svst

    def pause_simualtion(self):
        self.isRunning = False
        self.animation.event_source.stop()

    def continue_simulation(self):
        self.isRunning = True
        self.animation.event_source.start()

    def _check_for_termination(self, infected):
        if infected[-1] == 0:
            self.pause_simualtion()

    def run(self):
        # run the animation indefinitely
        self.isRunning = True
        self.wasStarted = True
        self.animation = FuncAnimation(self.fig, self.update, interval=25,
                                       fargs=(self.list_removed, self.list_infected, self.list_susceptible,
                                              self.list_time), blit=True)

        plt.show()

