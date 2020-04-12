import neat
import os
import random
from snake import *
import numpy
import pickle

def crete_list_angle() -> list:
    """ value = (move_x, move_y) """
    nums_of_angels = 8
    lst = []
    for i in range(nums_of_angels):
        angle = (360 / nums_of_angels) * i
        # move 4????
        num = RADUIS * 1
        if angle == 0:
            move_x = num
            move_y = 0
        elif angle == 90:
            move_x = 0
            move_y = num
        elif angle == 180:
            move_x = -num
            move_y = 0
        elif angle == 270:
            move_x = 0
            move_y = -num
        elif angle < 90:
            move_x = num
            move_y = num
        elif angle < 180:
            move_x = -num
            move_y = num
        elif angle < 270:
            move_x = -num
            move_y = -num
        else:
            move_x = num
            move_y = -num
        lst.append((move_x, move_y))
    return lst


lst_of_moves = crete_list_angle()


# def crete_input(snake: Snake, history_game) -> list:
#     """ find first well from 8 directs"""
#     nums_of_angels = 8
#     lst = []
#     for i in range(nums_of_angels):
#         # min_dis = None
#         angle = (360 / nums_of_angels) * i
#         x = snake.int_pos[0] + (RADUIS * lst_of_moves[i][0])
#         y = snake.int_pos[1] + (RADUIS * lst_of_moves[i][1])
#         run = True
#         while run:
#             for rx in range(2 * RADUIS):
#                 if rx > RADUIS:
#                     rx = RADUIS - rx
#                 for ry in range(RADUIS):
#                     if outside((x + rx, y + (ry * lst_of_moves[i][1]))):
#                         run = False
#                         break
#                     if run and history_game[x + rx][y + (ry * lst_of_moves[i][1])]:
#                         run = False
#                         break
#             if run:
#                 x += lst_of_moves[i][0]
#                 y += lst_of_moves[i][1]
#         temp_dis = math.sqrt(((snake.int_pos[0] - x) ** 2) + ((snake.int_pos[1] - y) ** 2))
#         #TODO if well is edge
#         lst.append(temp_dis)
#     lst.append(snake.direct)
#     return lst


def crete_input(snake: Snake, history_game, win=None) -> list:
    # win is a debugging tool
    x = snake.int_pos[0]
    y = snake.int_pos[1]
    lst = []
    num = 16
    for ry in range(2 * RADUIS + 1):
        if ry > RADUIS:
            ry = RADUIS - ry
        # add from left
        if outside((x + RADUIS + num, y + ry)):
            lst.append(1)
        else:
            lst.append(history_game[x + RADUIS + num][y + ry])
        # add from right
        if outside((x - RADUIS - num, y + ry)):
            lst.append(1)
        else:
            lst.append(history_game[x - RADUIS - num][y + ry])
        if win is not None:
            pygame.draw.circle(win, (0, 0, 255), (x + RADUIS + num, y + ry), 1)
            pygame.draw.circle(win, (0, 0, 255), (x - RADUIS - num, y + ry), 1)

    for rx in range(2 * RADUIS):
        if rx == RADUIS:
            continue
        if rx > RADUIS:
            rx = RADUIS - rx
        # add from top
        if outside((x + rx, y + RADUIS + num)):
            lst.append(1)
        else:
            lst.append(history_game[x + rx][y + RADUIS + num])
        # add from bottom
        if outside((x + rx, y - RADUIS - num)):
            lst.append(1)
        else:
            lst.append(history_game[x + rx][y - RADUIS- num])
        if win is not None:
            pygame.draw.circle(win, (0, 0, 255), (x + rx, y + RADUIS + num), 1)
            pygame.draw.circle(win, (0, 0, 255), (x + rx, y - RADUIS - num), 1)
    lst.append(snake.direct)
    return lst


def change_angle(snake: Snake, symbol: int) -> None:
    # symbol = 0/1/2
    if symbol == 2:
        pass
    elif symbol == 1:
        snake.direct += CHENGEANGEL
    else:
        snake.direct -= CHENGEANGEL


pop_size = 256

def eval_genomes(genomes, config):

    if len(genomes) != pop_size:
        print("shit")

    def play_game(group: list, rounds: int=1) -> None:
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
            history_game = [[0] * WIDTH for i in range(LENGTH)]
            cs1 = Snake(random.choice(range(10, 490)), random.choice(range(10, 490)), math.pi / 2, None)
            cs2 = Snake(random.choice(range(10, 490)), random.choice(range(10, 490)), math.pi / 2, None)
            cs3 = Snake(random.choice(range(10, 490)), random.choice(range(10, 490)), math.pi / 2, None)
            cs4 = Snake(random.choice(range(10, 490)), random.choice(range(10, 490)), math.pi / 2, None)
#             cs1 = Snake(100, 100, math.pi / 2, None)
#             cs2 = Snake(200, 200, math.pi / 2, None)
#             cs3 = Snake(300, 300, math.pi / 2, None)
#             cs4 = Snake(400, 400, math.pi / 2, None)

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
                        output = nets[i].activate(crete_input(snake, history_game))
                        change_angle(lst_of_snakes[1], output.index(max(output)))

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
    winner = p.run(eval_genomes, 15)

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
