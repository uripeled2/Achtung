import neat
import os
import random
from new_snake import *
import numpy


# input = [] * 500 * 500
# input[i] = 0 -> safe, 1 -> danger, 2 -> last, 3 -> my current pos, 4 ->  enemy current pos

def crete_default_input(lst_of_snakes: list) -> list:
    """"""

    lst = []
    for x in range(WIDTH):
        for y in range(LENGTH):
            if x < RADUIS or x + RADUIS > WIDTH or y < RADUIS or y + RADUIS > LENGTH:
                lst.append(1)
            else:
                lst.append(0)

    for s in lst_of_snakes:
        for x in s.history:
            for y in s.history[x]:
                for rx in range(2 * RADUIS):
                    if rx > RADUIS:
                        rx = RADUIS - rx
                    for ry in range(2 * RADUIS):
                        if ry > RADUIS:
                            ry = RADUIS - ry
                        lst[x + rx][y + ry] = 2
                # lst[x][y] = 1

    return lst


def set_input(default_input: list, snake: Snake) -> list:
    input_s = []
    input_s.extend(default_input)
    #input_s = default_input

    for rx in range(2 * RADUIS):
        if rx > RADUIS:
            rx = RADUIS - rx
        for ry in range(2 * RADUIS):
            if ry > RADUIS:
                ry = RADUIS - ry
            input_s[snake.last[0] + rx][snake.last[1] + ry] = 2

    for rx in range(2 * RADUIS):
        if rx > RADUIS:
            rx = RADUIS - rx
        for ry in range(2 * RADUIS):
            if ry > RADUIS:
                ry = RADUIS - ry
            input_s[snake.int_pos[0] + rx][snake.int_pos[1] + ry] = 3

    return input_s


def eval_genomes(genomes, config):
    def split_genomes(gens, size_of_group=4):
        """
        split the genomes randomly into groups, each group suppose to play different game
        """
        lst_of_groups = [[]]
        lst_i = 0
        while gens:
            i = random.randrange(len(gens))
            if len(lst_of_groups[lst_i]) <= size_of_group:
                lst_of_groups[lst_i].append(gens[i])
            else:
                lst_i += 1
                lst_of_groups.append([])
                lst_of_groups[lst_i].append(gens[i])
            del gens[i]
        return lst_of_groups

    lst_of_groups = split_genomes(genomes)

    def play_game(group: list, rounds: int=3) -> None:
        """
        run a game between the group, set there fitness
        """
        lst_of_snakes = []
        start_places_x = []
        start_places_y = []
        nets = []

        # crate snakes
        for player_id, player in group:
            player.fitness = 0

            # set the net
            net = neat.nn.FeedForwardNetwork.create(player, config)
            nets.append(net)

            # crate x and y
            x = random.randrange(20, 480)
            while x not in start_places_x:
                x = random.randrange(20, 480)
            start_places_x.append(x)
            y = random.randrange(20, 480)
            while y not in start_places_y:
                y = random.randrange(20, 480)
            start_places_y.append(y)

            lst_of_snakes.append(Snake(x, y, math.pi / 4, None))

        default_input = crete_default_input(lst_of_snakes)

        # run round
        while True:
            # stop if only one or less is alive
            temp = 0
            for s in lst_of_snakes:
                if not s.is_dead:
                    temp += 1
            if temp <= 1:
                break

            # change angle
            for i, snake in enumerate(lst_of_snakes):
                input_s = set_input(default_input, snake)
                # input_s = tuple(input_s)
                output = nets[i].activate(input_s)






def run(config_file):
    """
    runs NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


# Determine path to configuration file. This path manipulation is
# here so that the script will run successfully regardless of the
# current working directory.
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config.txt')
run(config_path)


