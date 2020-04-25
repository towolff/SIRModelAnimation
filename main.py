from App import MyApp
import sys


def main(title, num_balls, ball_size, max_ball_speed):
    app = MyApp(title, num_balls, ball_size, max_ball_speed)
    app.start()


if __name__ == '__main__':
    print(sys.version)
    num_balls = 200
    ball_size = 20
    max_ball_speed = 5

    main('SIR Model', num_balls, ball_size, max_ball_speed)
