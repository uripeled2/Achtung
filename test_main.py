from snake import *
import pygame
import random


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
    around = 1
    x = snake.int_pos[0]
    y = snake.int_pos[1]
    lst = []
    num = 8
    for _ in range(around):
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


pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("First Game")

run = True
import pickle
winner_net = pickle.load(open("best.pickle", "rb"))
cs1 = Snake(random.choice(range(10, 490)), random.choice(range(10, 490)), math.pi / 4, (255, 0, 0))
cs2 = Snake(random.choice(range(10, 490)), random.choice(range(10, 490)), math.pi / 2, (0, 255, 0))

lst_of_snakes = [cs1, cs2]


def change_angle(snake: Snake, symbol: int) -> None:
    # symbol = 0/1/2
    if symbol == 0:
        pass
    elif symbol == 1:
        snake.direct += CHENGEANGEL
    else:
        snake.direct -= CHENGEANGEL

pause = False
history_game = [[0] * WIDTH for i in range(LENGTH)]
history_game = cs1.add(history_game)
history_game = cs2.add(history_game)

while run:
    win.fill((0, 0, 0))
    pygame.time.delay(FRAME)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        pause = not pause
    if not pause:
        if keys[pygame.K_LEFT]:
            lst_of_snakes[0].direct -= CHENGEANGEL
        if keys[pygame.K_RIGHT]:
            lst_of_snakes[0].direct += CHENGEANGEL

        # change angle
        if not lst_of_snakes[1].is_dead:
            inp = crete_input(lst_of_snakes[1], history_game, win)
            output = winner_net.activate(inp)
            change_angle(lst_of_snakes[1], output.index(max(output)))

        # stop if anyone is die
        # die = False
        # for s in lst_of_snakes:
        #     if s.is_dead:
        #         pygame.time.delay(1000)
        #         pygame.quit()

        # stop if evrey one are dead
        die = True
        for s in lst_of_snakes:
            if not s.is_dead:
                die = False
        if die:
            pygame.time.delay(1000)
            pygame.quit()


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


        # draw the snakes
        draw_all(win, lst_of_snakes, history_game)

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

        for s1 in lst_of_snakes:
            if s1.is_hop:
                continue
            history_game = s1.add(history_game)

        pygame.display.update()

pygame.quit()
