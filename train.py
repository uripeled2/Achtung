import neat
import os
from snake import *
import pickle

pop_size = 256


def eval_genomes(genomes, config):

    if len(genomes) != pop_size:
        print("shit")

    for player_id, player in genomes:
        player.fitness = 0

    def split(genomes) -> list:
        size_of_group = 4
        gen = list(genomes)
        lst = [[]]
        i = 0
        while gen:
            lst[i].append(gen.pop(random.randrange(len(gen))))
            if len(lst[i]) >= size_of_group:
                lst.append([])
                i += 1
        return lst

    def play_game(group: list, rounds: int = 1) -> None:
        """
        run a game between the group, set there fitness
        """
        nets = []
        ge = []
        # set the net
        for player_id, player in group:
            player.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(player, config)
            nets.append(net)
            ge.append(player)

        # run
        num = 0
        while num < rounds:
            # set the game
            history_game = [[0] * WIDTH for _ in range(LENGTH)]
            cs1 = Snake(random.randrange(10, 490), random.randrange(10, 490), math.pi / random.randrange(1, 5), None)
            cs2 = Snake(random.randrange(10, 490), random.randrange(10, 490), math.pi / random.randrange(1, 5), None)
            cs3 = Snake(random.randrange(10, 490), random.randrange(10, 490), math.pi / random.randrange(1, 5), None)
            cs4 = Snake(random.randrange(10, 490), random.randrange(10, 490), math.pi / random.randrange(1, 5), None)
            # cs1 = Snake(100, 100, math.pi / 2, None)
            # cs2 = Snake(200, 200, math.pi / 2, None)
            # cs3 = Snake(300, 300, math.pi / 2, None)
            # cs4 = Snake(400, 400, math.pi / 2, None)

            lst_of_snakes = [cs1, cs2, cs3, cs4]
            history_game = cs1.add(history_game)
            history_game = cs2.add(history_game)
            history_game = cs3.add(history_game)
            history_game = cs4.add(history_game)
            num += 1
            # run round
            run = True
            # print("round start...")
            while run:
                # stop if only one or less is alive
                temp = 0
                for s in lst_of_snakes:
                    if not s.is_dead:
                        temp += 1
                if temp <= 1:
                    for i, s in enumerate(lst_of_snakes):
                        ge[i].fitness += s.survival_time
                    run = False
                    break

                # change angle
                for i, snake in enumerate(lst_of_snakes):
                    if not snake.is_dead:
                        output = nets[i].activate(snake.crete_input_nearest_well(history_game))
                        snake.change_angle(output.index(max(output)))

                # move the snakes
                for s in lst_of_snakes:
                    if s.is_dead:
                        continue

                    if s.is_hop:
                        s.when_to_stop -= 1
                        if s.when_to_stop <= 0:
                            s.is_hop = False
                            s.when_to_hop = random.choice(WIATUNTILHOP)
                    elif s.when_to_hop <= 0:
                        s.is_hop = True
                        s.when_to_stop = HOPINGTIME
                    else:
                        s.when_to_hop -= 1

                    s.last = s.int_pos
                    s.move()

                # find collision
                for s1 in lst_of_snakes:
                    if s1.is_dead:
                        continue
                    if s1.is_hop:
                        s1.outside()
                        continue
                    if s1.outside():
                        continue
                    s1.collision(history_game)

                # add to history
                for s1 in lst_of_snakes:
                    if s1.is_hop:
                        continue
                    history_game = s1.add(history_game)

                for s1 in lst_of_snakes:
                    if not s1.is_dead:
                        s1.survival_time += 1
                    else:
                        s1.survival_time -= 1

    for i in range(int(pop_size / 4)):
        group = []
        if len(genomes) <= i * 4 + 3:
            break
        for x in range(4):
            group.append(genomes[(i * 4) + x])
        play_game(group)


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
    winner = p.run(eval_genomes, 18)

    # show final stats
    # print('\nBest genome:\n{!s}'.format(winner))

    # save the module
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    pickle.dump(winner_net, open("best.pickle", "wb"))




# Determine path to configuration file. This path manipulation is
# here so that the script will run successfully regardless of the
# current working directory.
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config.txt')
run(config_path)
