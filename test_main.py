
import random
from snake import *
import numpy


# input[0..8] = first wall from this angle (0, 45, 90, 135, 180, 225, 270, 315)

def crete_input(snake: Snake, lst_of_snakes: list, nums_of_angels: int = 8) -> list:
    # define the 0,0 point
    x_0 = snake.int_pos[0]
    y_0 = snake.int_pos[0]

    min_dis_0 = 500 - y_0 - RADUIS
    min_dis_90 = 500 - x_0 - RADUIS
    min_dis_180 = y_0 - RADUIS
    min_dis_270 = x_0 - RADUIS

    min_dis_45 = min_dis_0 / math.cos(math.pi / 4)
    if y_0 < 500 - x_0:
        min_dis_45 = min_dis_45 - ((500 - x_0 - y_0) / math.cos(math.pi / 4))

    min_dis_135 = min_dis_180 / math.cos(math.pi / 4)
    if y_0 > x_0:
        min_dis_135 = min_dis_135 - ((y_0 - x_0) / math.cos(math.pi / 4))

    min_dis_225 = min_dis_180 / math.cos(math.pi / 4)
    if y_0 > 500 - x_0:
        min_dis_225 = min_dis_225 - ((y_0 - 500 + x_0) / math.cos(math.pi / 4))

    min_dis_315 = min_dis_0 / math.cos(math.pi / 4)
    if y_0 < x_0:
        min_dis_315 = min_dis_315 - ((x_0 - y_0) / math.cos(math.pi / 4))

    for s in lst_of_snakes:
        for x in s.history:
            y = s.history[x]
            dis = math.sqrt(((x - x_0) ** 2) + ((y - y_0) ** 2))

            # calculation for 0 degree
            if x_0 - 2 * RADUIS < x and x > x_0 + 2 * RADUIS and y > y_0 and min_dis_0 < dis:
                # we have a collision!!
                min_dis_0 = dis

            # calculation for 45 degree
            if x < x_0 and y_0 - 2 * RADUIS - x < y < y_0 + 2 * RADUIS - x and min_dis_45 < dis:
                # we have a collision!!
                min_dis_45 = dis

            # calculation for 90 degree
            if x < x_0 and y_0 - 2 * RADUIS < y < y_0 + 2 * RADUIS and min_dis_90 < dis:
                # we have a collision!!
                min_dis_90 = dis

            # calculation for 135 degree
            if x < x_0 and y_0 - 2 * RADUIS + x < y < y_0 + 2 * RADUIS + x and min_dis_135 < dis:
                # we have a collision!!
                min_dis_135 = dis

            # calculation for 180 degree
            if x_0 - 2 * RADUIS < x and x > x_0 + 2 * RADUIS and y < y_0 and min_dis_180 < dis:
                # we have a collision!!
                min_dis_180 = dis

            # calculation for 225 degree
            if x > x_0 and y_0 - 2 * RADUIS - x < y < y_0 + 2 * RADUIS - x and min_dis_225 < dis:
                # we have a collision!!
                min_dis_225 = dis

            # calculation for 270 degree
            if x > x_0 and y_0 - 2 * RADUIS < y < y_0 + 2 * RADUIS and min_dis_270 < dis:
                # we have a collision!!
                min_dis_270 = dis

            # calculation for 315 degree
            if x > x_0 and y_0 - 2 * RADUIS + x < y < y_0 + 2 * RADUIS + x and min_dis_315 < dis:
                # we have a collision!!
                min_dis_315 = dis

    return [min_dis_0, min_dis_45, min_dis_90, min_dis_135, min_dis_180, min_dis_225, min_dis_270, min_dis_315]


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
        # lst = crete_input(lst_of_snakes[0], lst_of_snakes, 1)
        lst = crete_input(lst_of_snakes[0], lst_of_snakes)
        print(lst)

        # make a dealy
        # num = 0
        # for i in range(10 ** 7):
        #     num += i


        pygame.display.update()



pygame.quit()
