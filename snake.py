import math
import pygame
import random

WIDTH = 500
LENGTH = 500
FRAME = 20
SPEED = 3
RADUIS = 4
CHENGEANGEL = SPEED * 2 * (math.pi / 180)
BACKGROUND = (0, 0, 0)
WIATUNTILHOP = (10 * FRAME, 15 * FRAME)
HOPINGTIME = int(3.5 * FRAME / SPEED)


# history_game = [[0] * WIDTH for i in range(LENGTH)]

# id != 0 or 1 !!!!
from_color_to_id = {(255, 0, 0): 2, (0, 255, 0): 3, None: 4, (0, 0, 255): 5, (255, 255, 255): 6}
from_id_to_color = {2: (255, 0, 0), 3: (0, 255, 0), 4: (0, 0, 0), 5: (0, 0, 255), 6: (255, 255, 255)}


def draw_all(win, lst_of_snakes, history_game):
    for s in lst_of_snakes:
        pygame.draw.circle(win, s.color, s.int_pos, RADUIS)
    for x, row in enumerate(history_game):
        for y, p in enumerate(row):
            if p != 0 and p != 1:
                pygame.draw.circle(win, from_id_to_color[p], (x, y), RADUIS)


def outside(int_pos: tuple) -> bool:
    if int_pos[0] < RADUIS or int_pos[0] + RADUIS > 500:
        # self.is_dead = True
        return True

    if int_pos[1] < RADUIS or int_pos[1] + RADUIS > 500:
        # self.is_dead = True
        return True
    return False


def collision_between_two_dots(pos1, pos2):
    x1 = pos1[0]
    x2 = pos2[0]
    y1 = pos1[1]
    y2 = pos2[1]

    if x1 == x2 or x1 < x2 <= x1 + 1 + RADUIS or x1 - 1 - RADUIS <= x2 < x1:
        if y1 == y2 or y1 < y2 <= y1 + 1 + RADUIS or y1 - 1 - RADUIS <= y2 < y1:
            return True
    return False


class Snake:
    def __init__(self, head_x, head_y, direct, color, is_dead=False):
        self.position = (head_x, head_y)
        self.int_pos = (int(head_x), int(head_y))
        self.last = self.int_pos
        self.color = color
        self.is_dead = is_dead
        self.direct = direct
        self.is_hop = False
        self.when_to_hop = random.choice(WIATUNTILHOP)
        self.when_to_stop = HOPINGTIME
        self.survival_time = 0
        self.id = from_color_to_id[color]
        # self.add(history_game)

    def move(self):
        v1 = self.position[0] + SPEED * math.cos(self.direct)
        v2 = self.position[1] + SPEED * math.sin(self.direct)
        tu = (v1, v2)
        self.position = tu
        # self.position = self.position + Vector2(1, 0).rotate(self.direct) * SPEED
        # self.int_pos = (int(self.position[0]),  int(self.position[1]))
        self.int_pos = (round(self.position[0]), round(self.position[1]))
        # add(self.int_pos[0], self.int_pos[1])

    def add(self, history_game):
        x = self.int_pos[0]
        y = self.int_pos[1]
        history_game[x][y] = self.id
        for rx in range(2 * RADUIS):
            if rx == RADUIS:
                continue
            if rx > RADUIS:
                rx = RADUIS - rx
            for ry in range(2 * RADUIS):
                if ry == RADUIS:
                    continue
                if ry > RADUIS:
                    ry = RADUIS - ry
                if rx == 0 and ry == 0:
                    continue
                # if not outside((x + rx, y + ry)):
                if 0 <= self.int_pos[0] + rx < 500 and 0 <= self.int_pos[1] + ry < 500:
                    if history_game[x + rx][y + ry] == 0:  # or history_game[x + rx][y + ry] == 1:
                        history_game[x + rx][y + ry] = 1
        return history_game

    def collision(self, history_game):
        for rx in range(2 * RADUIS):
            if rx > RADUIS:
                rx = RADUIS - rx
            for ry in range(2 * RADUIS):
                if ry > RADUIS:
                    ry = RADUIS - ry
                # if outside((self.int_pos[0] + rx, self.int_pos[1] + ry)):
                #     self.is_dead = True
                #     return True
                if 0 <= self.int_pos[0] + rx < 500 and 0 <= self.int_pos[1] + ry < 500:
                    if history_game[self.int_pos[0] + rx][self.int_pos[1] + ry]:
                        if not collision_between_two_dots((self.int_pos[0] + rx, self.int_pos[1] + ry), self.last):
                            self.is_dead = True
                            return True
        return False

    def outside(self):
        if self.int_pos[0] < RADUIS or self.int_pos[0] + RADUIS > 500:
            self.is_dead = True
            return True

        if self.int_pos[1] < RADUIS or self.int_pos[1] + RADUIS > 500:
            self.is_dead = True
            return True

        return False

    def crete_input_pixel_around(self, history_game, win=None) -> list:
        """

        :param history_game:
        :param win: a debugging tool
        :return:
        """
        around = 1
        snake = self
        x = snake.int_pos[0]
        y = snake.int_pos[1]
        lst = []
        num = 16
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
                    lst.append(history_game[x + rx][y - RADUIS - num])
                if win is not None:
                    pygame.draw.circle(win, (0, 0, 255), (x + rx, y + RADUIS + num), 1)
                    pygame.draw.circle(win, (0, 0, 255), (x + rx, y - RADUIS - num), 1)
        lst.append(snake.direct)
        return lst

    def crete_input_nearest_well(self, history_game, win=None) -> list:
        """
        find first well from 8 directs
        :param history_game:
        :param win: a debugging tool
        :return:
        """
        nums_of_angels = 8
        lst = []
        snake = self
        for i in range(nums_of_angels):
            angle = (360 / nums_of_angels) * i
            x = snake.int_pos[0] + (RADUIS * lst_of_moves[i][0])
            y = snake.int_pos[1] + (RADUIS * lst_of_moves[i][1])
            times = 0
            run = True
            while run and times < 5:
                times += 1
                for rx in range(2 * RADUIS):
                    if rx > RADUIS:
                        rx = RADUIS - rx
                    for ry in range(RADUIS):
                        if outside((x + rx, y + (ry * lst_of_moves[i][1]))):
                            run = False
                            break
                        if run and history_game[x + rx][y + (ry * lst_of_moves[i][1])]:
                            run = False
                            break
                if run:
                    x += lst_of_moves[i][0]
                    y += lst_of_moves[i][1]
            temp_dis = math.sqrt(((snake.int_pos[0] + lst_of_moves[i][0] - x) ** 2) +
            ((snake.int_pos[1] + lst_of_moves[i][1] - y) ** 2))
            if win is not None:
                pygame.draw.circle(win, (255, 255, 255), (x - lst_of_moves[i][0], y - lst_of_moves[i][1]), 2)
            lst.append(temp_dis)
        lst.append(snake.direct)
        return lst

    def change_angle(self, symbol: int) -> None:
        # symbol = 0/1/2
        if symbol == 2:
            pass
        elif symbol == 1:
            self.direct += CHENGEANGEL
        else:
            self.direct -= CHENGEANGEL


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




