import math
import pygame
import random

WIDTH = 500
LENGTH = 500
FRAME = 10
SPEED = 1
RADUIS = 4
# CHENGEANGEL = math.pi / (SPEED * 5)
CHENGEANGEL = SPEED * 2 * (math.pi / 180)
BACKGROUND = (0, 0, 0)
WIATUNTILHOP = (10 * FRAME, 15 * FRAME)
# HOPINGTIME = int(3.5 * 500 / (SPEED * FRAME))
HOPINGTIME = int(3.5 * FRAME / SPEED)


def collision_between_two_dots(pos1, pos2):
    x1 = pos1[0]
    x2 = pos2[0]
    y1 = pos1[1]
    y2 = pos2[1]

    if x1 == x2 or x1 < x2 < x1 + 2 * RADUIS or x1 - 2 * RADUIS < x2 < x1:
        if y1 == y2 or y1 < y2 < y1 + 2 * RADUIS or y1 - 2 * RADUIS < y2 < y1:
            return True
    return False


class Snake:
    def __init__(self, head_x, head_y, direct, color, is_dead=False):
        self.position = (head_x, head_y)
        self.int_pos = (int(head_x), int(head_y))
        self.last = self.int_pos
        self.color = color
        self.is_dead = is_dead
        self.history = {}
        self.history[self.int_pos[0]] = {}
        self.history[self.int_pos[0]][self.int_pos[1]] = True
        self.direct = direct
        self.is_hop = False
        self.when_to_hop = random.choice(WIATUNTILHOP)
        self.when_to_stop = HOPINGTIME
        self.survival_time = 0

    def move(self):
        v1 = self.position[0] + SPEED * math.cos(self.direct)
        v2 = self.position[1] + SPEED * math.sin(self.direct)
        tu = (v1, v2)
        self.position = tu
        # self.int_pos = (int(self.position[0]),  int(self.position[1]))
        self.int_pos = (round(self.position[0]), round(self.position[1]))

    def draw(self, win):
        pygame.draw.circle(win, self.color, self.int_pos, RADUIS)
        for key in self.history:
            for k in self.history[key]:
                pygame.draw.circle(win, self.color, (key, k), RADUIS)

    def collision(self, snake):

        for x in range(4 * RADUIS):
            if x >= 2 * RADUIS:
                x = 2 * RADUIS - x
            if snake.history.get(self.int_pos[0] + x) is not None:
                for y in range(4 * RADUIS):
                    if y >= 2 * RADUIS:
                        y = 2 * RADUIS - y
                    if snake.history.get(self.int_pos[0] + x).get(self.int_pos[1] + y):
                        if self == snake and snake.color is not None and collision_between_two_dots((self.int_pos[0] + x, self.int_pos[1] + y), self.last):
                            if snake.color is None:
                                print("uri")
                            # print(f"last: {self.last}")
                            # print(f"pos: {(self.int_pos[0] + x, self.int_pos[1] + y)}")
                            continue
                        else:
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


