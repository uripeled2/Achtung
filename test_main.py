
import random
from snake import *
import numpy


# input[0..8] = first wall from this angle (0, 45, 90, 135, 180, 225, 270, 315)
def crete_input(snake: Snake, lst_of_snakes: list, nums_of_angels: int = 8) -> list:
    lst = []
    for i in range(nums_of_angels):
        min_dis = None
        angle = ((2 * math.pi) / nums_of_angels) * i
        if angle == math.pi * 1.5 or math.pi / 2 == angle:
            # special because the x stays
            if angle == math.pi:
                num = -1
            else:
                num = 1
            move_x = 0
            move_y = num * 4

            temp_s = Snake(snake.int_pos[0] + move_x, snake.int_pos[1] + move_y, 0, None)
            bo = True
            while bo:
                # search collision
                if temp_s.outside():
                    min_dis = math.sqrt((move_x ** 2) + (move_y ** 2))
                    bo = False
                    break
                for s in lst_of_snakes:
                    if temp_s.collision(s):
                        if False and s == snake and collision_between_two_dots(temp_s.int_pos,
                                                                     s.int_pos):  # collision_between_two_dots((self.int_pos[0] + x, self.int_pos[1] + y), self.last)
                            continue
                        else:
                            min_dis = math.sqrt((move_x ** 2) + (move_y ** 2))
                            bo = False
                            break

                # move
                move_y += num
                temp_s.int_pos = (snake.int_pos[0] + move_x, snake.int_pos[1] + move_y)

            # TODO also add the second well
            lst.append(min_dis)

        else:
            if angle < math.pi / 2 or angle > math.pi * (270 / 180):  # angle < 90 angle or > 270
                num = 1
            else:
                num = -1
            move_x = num * 4
            a = move_x / math.cos(angle)
            move_y = round(a * math.sin(angle))
            # while move_y != int(move_y):
            #     move_x += num
            #     a = move_x / math.cos(angle)
            #     move_y = a * math.sin(angle)

            temp_s = Snake(snake.int_pos[0] + move_x, snake.int_pos[1] + move_y, 0, None)
            bo = True
            while bo:
                # search collision
                if temp_s.outside():
                    min_dis = math.sqrt((move_x ** 2) + (move_y ** 2))
                    break
                for s in lst_of_snakes:
                    if temp_s.collision(s):
                        # print("uri")
                        if s == snake and collision_between_two_dots(temp_s.int_pos,
                                                                     s.int_pos):  # collision_between_two_dots((self.int_pos[0] + x, self.int_pos[1] + y), self.last)
                            pass
                        else:
                            min_dis = math.sqrt((move_x ** 2) + (move_y ** 2))
                            bo = False
                            break

                # move
                move_x += num
                a = move_x / math.cos(angle)
                move_y = round(a * math.sin(angle))

                # while move_y != int(move_y):
                #     move_x += num
                #     a = move_x / math.cos(angle)
                #     move_y = a * math.sin(angle)
                temp_s.int_pos = (snake.int_pos[0] + move_x, snake.int_pos[1] + move_y)

            # TODO also add the second well
            print(move_x, move_y)
            lst.append(min_dis)

    return lst


# from new_snake import *
# import pygame
# import random

pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("First Game")

run = True

cs1 = Snake(random.choice(range(10, 490)), random.choice(range(10, 490)), math.pi / 4, (255, 0, 0))
cs2 = Snake(random.choice(range(10, 490)), random.choice(range(10, 490)), math.pi / 2, (0, 255, 0))
lst_of_snakes = [cs1, cs2]

# dict: key = pos_x; value = dict: key = pos_y; value = True;
count = 0
pause = False
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

        if keys[pygame.K_a]:
            lst_of_snakes[1].direct -= CHENGEANGEL
        if keys[pygame.K_s]:
            lst_of_snakes[1].direct += CHENGEANGEL

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
        for s in lst_of_snakes:
            s.draw(win)

        # find collision
        for s1 in lst_of_snakes:
            if s1.is_dead:
                continue
            if s1.is_hop:
                s1.outside()
                continue
            if s1.collision(s1):
                continue
            s1.outside()
            for s2 in lst_of_snakes:
                if s1.is_dead:
                    break
                if s1 == s2:
                    continue
                s1.collision(s2)

        for s1 in lst_of_snakes:
            if s1.is_hop:  # or s1.is_dead:
                continue
            elif s1.history.get(s1.int_pos[0]) is None:
                s1.history[s1.int_pos[0]] = {}

            s1.history[s1.int_pos[0]][s1.int_pos[1]] = True

        # debug colse well
        lst = crete_input(lst_of_snakes[0], lst_of_snakes, 1)
        # lst = crete_input(lst_of_snakes[0], lst_of_snakes)
        #print(lst)

        # make a dealy
        # num = 0
        # for i in range(10 ** 7):
        #     num += i


        pygame.display.update()



pygame.quit()
