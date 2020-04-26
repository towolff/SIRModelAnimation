from Simulation import SIRSimulation
import sys
import getopt


def main(argv):
    print ('+++' * 10)
    print('Using Python Version: {}'.format(sys.version))
    print('Started SIR Model Animation by Torge Wolff.')
    n_individuals = 400  # number of individuals
    prct_infected = 2  # percentage of infected people at the beginning of the simulation (0-100%)
    infection_radius = 2.5  # radius of transmission in pixels (0-100)
    infection_prob = 6  # probability of transmission in percentage (0-100%)
    prct_quarantine = 0  # percentage of the people in quarantine (0-100%)
    time_infected = 40  # time taken to recover/ remove in number of frames (0-infinity)
    random_recovery_time = False  # Different random recovery time for each individual; default is False
    print('Number of passed arguments:', len(sys.argv))

    try:
        opts, args = getopt.getopt(argv, "hn:p:r:i:q:t:z:", ["help", "n_individuals=", "prct_infected=",
                                                             "infection_radius=", "infection_prob=", "prct_quarantine=",
                                                             "time_infected=", "random_recovery_time="])
    except getopt.GetoptError as e:
        print('Excpetion!')
        print(e)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            txt = """
            ###############################################################################################
            --n_individuals          number of individuals; default is 400
            -n                       number of individuals; default is 400
            ###############################################################################################
            --prct_infected          Staring percentage of infected individuals; default is 2
            -p                       Staring percentage of infected individuals; default is 2
            ###############################################################################################
            --infection_radius       Radius of virus transmission in pixels; default is 2.5
            -r                       Radius of virus transmission in pixels; default is 2.5
            ###############################################################################################
            --infection_prob         Probability of virus infection of an individum; default is 6
            -i                       Probability of virus infection of an individum; default is 6
            ###############################################################################################
            --prct_quarantine        Percentage of individuals in quarantine; default is 0
            -q                       Percentage of individuals in quarantine; default is 0
            ###############################################################################################
            --time_infected          Time until an infected individum is removed; default is 40
            -t                       Time until an infected individum is removed; default is 40
            ###############################################################################################
            --random_recovery_time   Different random recovery time for each individual; default is False            
            -z                       Different random recovery time for each individual; default is False
            ###############################################################################################
            """
            print(txt)
            sys.exit()
        elif opt in ("--n_individuals", "-n"):
            n_individuals = int(arg)
        elif opt in ("--prct_infected", "-p"):
            prct_infected = float(arg)
        elif opt in ("--infection_radius", '-r'):
            infection_radius = float(arg)
        elif opt in ("infection_prob", "-i"):
            infection_prob = int(arg)
        elif opt in ("--prct_quarantine", '-q'):
            prct_quarantine = int(arg)
        elif opt in ('--time_infected', '-t'):
            time_infected = int(arg)
        elif opt in ('-z', '--random_recovery_time'):
            random_recovery_time = bool(int(arg))

    print('+++ Parameter +++')
    print('n_individuals: {}'.format(n_individuals))
    print('prct_infected: {}'.format(prct_infected))
    print('infection_radius: {}'.format(infection_radius))
    print('infection_prob: {}'.format(infection_prob))
    print('prct_quarantine: {}'.format(prct_quarantine))
    print('time_infected: {}'.format(time_infected))
    print('random_recovery_time: {}'.format(random_recovery_time))
    print('+++++++++++++++++')

    sim = SIRSimulation(n_individuals=n_individuals,prct_infected=prct_infected, r_infection=infection_radius,
                        p_infection=infection_prob, p_quarantine=prct_quarantine, t_recovery=time_infected,
                        different_recovery_times=random_recovery_time)
    sim.run()


if __name__ == '__main__':
    main(sys.argv[1:])
