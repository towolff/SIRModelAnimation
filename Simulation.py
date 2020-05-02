from Individual import Individual
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.animation import FuncAnimation
from datetime import datetime


class SIRSimulation:

    def __init__(self, n_individuals=400, prct_infected=2, r_infection=2.5,
                 p_infection=6, p_quarantine=0, t_recovery=40, different_recovery_times=False, save_figure=False,
                 simulation_mode=False):
        self.isRunning = False
        self.wasStarted = False
        self.simulation_mode = simulation_mode
        self.animation = None
        self.N_INDIVIDUALS = n_individuals  # number of individuals
        self.PRCT_INFECTED = prct_infected  # percentage of infected people at the beginning of the simulation (0-100%)
        self.INFECTION_RADIUS = r_infection  # radius of transmission in pixels (0-100)
        self.INFECTION_PROBABILITY = p_infection  # probability of transmission in percentage (0-100%)
        self.P_QUARANTINE = p_quarantine  # percentage of the people in quarantine (0-100%)
        self.T_RECOVERY = t_recovery  # time taken to recover in number of frames (0-infinity)
        self.different_recovery_times = different_recovery_times  # rand recovery t for each ind btw.. 1 and t_recovery
        self.save_figure = save_figure
        self.fig_path = os.path.join(os.getcwd(), 'figs')
        self.n_infected = 0
        self.current_r_list = [0.0]
        self.r_template_txt = 'R: {:.2f}'
        self.individuals = []
        self.list_r_txt = [self.r_template_txt.format(self.current_r_list[-1])]
        self.list_susceptible = [self.N_INDIVIDUALS]
        self.list_infected = [self.n_infected]
        self.list_removed = [0]
        self.list_time = [0]
        self.time = []
        self.iteration = []
        self._init_individuals()
        self._init_figure()

    def _init_individuals(self):
        # creating all the individuals in random positions and infecting some of them.
        for i in range(self.N_INDIVIDUALS):
            # sample different infectrion probabilities for each individual, if True
            if self.different_recovery_times:
                if np.random.uniform(0, 1, 1) > 0.5:
                    recovery_time = np.random.randint(1, self.T_RECOVERY)
                else:
                    recovery_time = self.T_RECOVERY
            else:
                recovery_time = self.T_RECOVERY
            # Dicide for each individual if quarantine or not with given quarantine probability
            if self.P_QUARANTINE > 0:
                prob_quarantine = np.random.choice(np.arange(0, 2), p=[1 - float(self.P_QUARANTINE / 100),
                                                                       float(self.P_QUARANTINE / 100)])
                prob_quarantine = bool(prob_quarantine)
            else:
                prob_quarantine = False

            p = Individual(i, np.random.random() * 100, np.random.random() * 100,
                           np.random.random() * 100, np.random.random() * 100,
                           (np.random.random() + 0.5) * 100, recovery_time, prob_quarantine)

            # Infect individual by given prct
            if np.random.random() < self.PRCT_INFECTED / 100:
                p.infect(0)
                self.n_infected = self.n_infected + 1

            self.individuals.append(p)

    def _init_figure(self):
        # create all the graphics
        self.fig = plt.figure(figsize=(20, 10))
        self.gridspec = self.fig.add_gridspec(ncols=2, nrows=3)
        description = '- Number of individuals: {}\n'\
                      '- Percent of initially infected individuals: {}\n' \
                      '- Infection radius of an individual: {}\n' \
                      '- Infection probabilty of an individual.: {}\n' \
                      '- Quarantine probability: {}\n' \
                      '- Timesteps until infected individual is removed: {}\n' \
                      '- Different recovery times for each indiviual: {}\n' \
                      '- Save Figure: {}'.format(self.N_INDIVIDUALS,
                                                 self.PRCT_INFECTED,
                                                 self.INFECTION_RADIUS,
                                                 self.INFECTION_PROBABILITY,
                                                 self.P_QUARANTINE,
                                                 self.T_RECOVERY,
                                                 self.different_recovery_times,
                                                 self.save_figure)

        title = 'SIR Model Animation'
        self.fig.suptitle(title, fontsize=20)
        self.fig.canvas.set_window_title('SIR Model Animation')
        self.text_plot = self.fig.add_subplot(self.gridspec[0, 1])
        self.text_plot.text(0.05, 0, description, fontsize=18,  bbox=dict(facecolor='lightgreen', alpha=0.5))
        self.kpis_plot = self.fig.add_subplot(self.gridspec[0:-1, 0])  # first: row, second: column
        self.r_plot = self.fig.add_subplot(self.gridspec[-1, 0])
        self.population_scatter = self.fig.add_subplot(self.gridspec[1:, 1])
        self.population_scatter.axis('off')
        self.text_plot.axis('off')
        self.kpis_plot.axis([0, 300, 0, self.N_INDIVIDUALS])
        self.r_plot.axis([0, 300, 0, 4.0])
        self.scatter = self.population_scatter.scatter([p.posx for p in self.individuals],
                                                       [p.posy for p in self.individuals], c='blue', s=12)
        self.box = plt.Rectangle((0, 0), 100, 100, fill=False)
        self.population_scatter.add_patch(self.box)
        self.cvst, = self.kpis_plot.plot(self.n_infected, color="red", label="Infected")
        self.rvst, = self.kpis_plot.plot(self.n_infected, color="gray", label="Removed")
        self.svst, = self.kpis_plot.plot(self.n_infected, color='blue', label='Susceptible')
        self.r_line2d, = self.r_plot.plot(self.current_r_list[-1], color='orange', label='R-Factor')
        self.r_text_obj = self.population_scatter.text(0, 0, ' ', fontsize=20)

        self.kpis_plot.legend(handles=[self.svst, self.cvst, self.rvst])
        self.r_plot.legend(handles=[self.r_line2d])
        self.kpis_plot.set_xlabel("Time")
        self.kpis_plot.set_ylabel("Individuals")
        self.r_plot.set_xlabel("Time")
        self.r_plot.set_ylabel("R-Factor")

    def update(self, frame, removed, currently_infected, susceptible, t, current_r):
        # function excecuted frame by frame
        count_susceptible = self.N_INDIVIDUALS
        count_infected = 0
        count_removed = 0
        current_r_val = 0.0
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

        # calculate R-factor
        r_factor = 0.0
        if t[-1] != 0:
            r_factor = self._calculate_r_factor()

        self.r_text_obj.set_text(self.r_template_txt.format(r_factor))

        # update the plotting data
        currently_infected.append(count_infected)
        removed.append(count_removed)
        susceptible.append(count_susceptible)
        t.append(frame)
        current_r.append(r_factor)

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
        self.r_line2d.set_data(t, current_r)

        return self.scatter, self.cvst, self.rvst, self.svst, self.r_text_obj, self.r_line2d

    def save_fig(self):
        now = datetime.now().strftime('%Y%m%d')
        figname = "{}_Simulation_n_individuals_{}_prct_infected_{}_infection_radius_{}_infection_prob_{}" \
                  "_p_quarantine_{}_t_infected_{}_diff_recovery_times_{}.png".format(now, self.N_INDIVIDUALS,
                                                                                     self.PRCT_INFECTED,
                                                                                     self.INFECTION_RADIUS,
                                                                                     self.INFECTION_PROBABILITY,
                                                                                     self.P_QUARANTINE,
                                                                                     self.T_RECOVERY,
                                                                                     self.different_recovery_times)
        full_figname = os.path.join(self.fig_path, figname)
        self.fig.savefig(full_figname, dpi=400)
        print('[SIM] Saved figure: {}'.format(full_figname))

    def pause_simualtion(self):
        self.isRunning = False
        self.animation.event_source.stop()
        if self.save_figure:
            self.save_fig()
        if self.simulation_mode:
            self.fig.close()

    def continue_simulation(self):
        self.isRunning = True
        self.animation.event_source.start()

    def _check_for_termination(self, infected):
        if infected[-1] == 0:
            self.pause_simualtion()

    def _calculate_r_factor(self):
        r_divisor = self.list_infected[-4]
        r_dividend = self.list_infected[-1]
        r_factor = float(r_dividend / r_divisor)
        return r_factor

    def run(self):
        # run the animation indefinitely
        self.isRunning = True
        self.wasStarted = True
        self.animation = FuncAnimation(self.fig, self.update, interval=25,
                                       fargs=(self.list_removed, self.list_infected, self.list_susceptible,
                                              self.list_time, self.current_r_list), blit=True)

        plt.show()

