from Individual import Individual
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# SIMULATION PARAMETERS
N_INDIVIDUALS = 400  # number of individuals
PRCT_INFECTED = 2  # percentage of infected people at the beginning of the simulation (0-100%)
R_CONTAGION = 2.1  # radius of transmission in pixels (0-100)
P_CONTAGION = 4  # probability of transmission in percentage (0-100%)
P_QUARANTINE = 0  # percentage of the people in quarantine (0-100%)
T_RECOVERY = 60   # time taken to recover in number of frames (0-infinity)

n_infected = 0
individuals = []

# creating all the individuals in random positions and infecting some of them.
for i in range(N_INDIVIDUALS):
    p = Individual(i, np.random.random() * 100, np.random.random() * 100,
                   np.random.random() * 100, np.random.random() * 100,
                   (np.random.random()+0.5) * 100, T_RECOVERY, False)

    if np.random.random() < PRCT_INFECTED/100:
        p.infect(0)
        n_infected = n_infected + 1
    if np.random.random() < P_QUARANTINE/100:
        p.fixedQuarantine = True

    individuals.append(p)

# this creates all the graphics
fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot(1, 2, 1)
cx = fig.add_subplot(1, 2, 2)
ax.axis('off')
cx.axis([0, 1000, 0, N_INDIVIDUALS])
scatter = ax.scatter([p.posx for p in individuals],
                     [p.posy for p in individuals], c='blue', s=8)
box = plt.Rectangle((0, 0), 100, 100, fill=False)
ax.add_patch(box)
cvst, = cx.plot(n_infected, color="red", label="Infected")
rvst, = cx.plot(n_infected, color="gray", label="Removed")
svst, = cx.plot(n_infected, color='blue', label='Susceptible')

cx.legend(handles=[svst, cvst, rvst])
cx.set_xlabel("Time")
cx.set_ylabel("Individuals")

list_susceptible = [N_INDIVIDUALS]
list_infected = [n_infected]
list_removed = [0]
list_time = [0]


# function excecuted frame by frame
def update(frame, removed, infected, susceptible, t):
    count_susceptible = N_INDIVIDUALS
    count_infected = 0
    count_removed = 0
    individual_colors = []
    individual_sizes = [9 for p in individuals]

    for p in individuals:
        # check how much time the person has been sick
        p.check_infection(frame)
        # animate the movement of each person
        p.update_pos(0, 0)
        if p.removed:
            count_removed += 1  # count the amount of recovered
            count_susceptible -= 1
        if p.infected:
            count_infected = count_infected + 1  # count the amount of infected
            # check for people around the sick individual and infect the ones within the
            # transmission radius given the probability
            for ind in individuals:
                if ind.idx == p.idx or ind.infected or ind.removed:
                    pass
                else:
                    d = p.get_dist(ind.posx, ind.posy)
                    if d < R_CONTAGION:
                        if np.random.random() < P_CONTAGION / 100:
                            ind.infect(frame)
                            individual_sizes[ind.idx] = 80

        individual_colors.append(p.get_color())  # change dot color according to the person's status

    # update the plotting data
    infected.append(count_infected)
    removed.append(count_removed)
    susceptible.append(count_susceptible)
    t.append(frame)

    # transfer the data to the matplotlib graphics
    offsets = np.array([[p.posx for p in individuals],
                       [p.posy for p in individuals]])
    scatter.set_offsets(np.ndarray.transpose(offsets))
    scatter.set_color(individual_colors)
    scatter.set_sizes(individual_sizes)
    cvst.set_data(t, infected)
    rvst.set_data(t, removed)
    svst.set_data(t, susceptible)
    return scatter, cvst, rvst, svst


# run the animation indefinitely
animation = FuncAnimation(fig, update, interval=25, fargs=(list_removed, list_infected, list_susceptible, list_time), blit=True)

plt.show()
