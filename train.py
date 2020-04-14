import neat
import os
from snake import *
from game import Game
import pickle
import pygame


def eval_genomes(genomes, config):

    for player_id, player in genomes:
        player.fitness = 0

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
            # pygame.init()
            # win = pygame.display.set_mode((WIDTH, LENGTH))
            win = None
            # pygame.display.set_caption("First Game")
            history_game = [[0] * WIDTH for _ in range(LENGTH)]

            def crete_snakes(history_game):
                lst_of_snakes = []
                for _ in range(len(group)):
                    s = Snake(random.randrange(10, 490), random.randrange(10, 490), math.pi / random.randrange(1, 5), (255, 0, 0))
                    while s.collision(history_game):
                        s.int_pos = (random.randrange(10, 490), random.randrange(10, 490))
                    history_game = s.add(history_game)
                    lst_of_snakes.append(s)
                return lst_of_snakes, history_game

            lst_of_snakes, history_game = crete_snakes(history_game)

            num += 1
            # run round
            run = True
            game = Game(lst_of_snakes, history_game, win)
            while run:
                # win.fill((0, 0, 0))
                # pygame.time.delay(FRAME)

                # change angle
                for i, snake in enumerate(lst_of_snakes):
                    if not snake.is_dead:
                        output = nets[i].activate(snake.crete_input_nearest_well(history_game))
                        snake.change_angle(output.index(max(output)))

                if not game.update(to_draw=False):
                    run = False
                    break

                # pygame.display.update()

            # pygame.quit()

            # set score
            for i, s in enumerate(lst_of_snakes):
                if s.place is None:
                    s.place = game.last_place
                    game.last_place += 1
                ge[i].fitness += s.place

    play_game(genomes, 5)



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


