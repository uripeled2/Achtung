
import random
from snake import *
import numpy


# input[0..8] = first wall from this angle (0, 45, 90, 135, 180, 225, 270, 315)
def crete_input(snake: Snake, lst_of_snakes: list, nums_of_angels: int = 8) -> list:
    lst = []
    for i in range(nums_of_angels):
        min_dis = None
        angle = ((2 * math.pi) / nums_of_angels) * i

        is_normal = True
        if angle == math.pi * 1.5 or math.pi / 2 == angle:
            is_normal = False

        # define limts
        if angle > math.pi * 1.5 or math.pi / 2 > angle:
            min_x = snake.int_pos[0]
            max_x = WIDTH - RADUIS
        elif angle == math.pi * 1.5 or math.pi / 2 == angle:
            min_x = snake.int_pos[0] - RADUIS
            max_x = snake.int_pos[0] + RADUIS # raduis /2 ???
        else:
            min_x = RADUIS
            max_x = snake.int_pos[0]

        if angle <= math.pi:
            min_y = snake.int_pos[1]
            # max_y = LENGTH - RADUIS
            if not is_normal:
                max_y = LENGTH - RADUIS
            else:
                hypotenuse = max_x / math.cos(angle)
                max_y = round(hypotenuse * math.sin(angle))

        else:
            max_y = snake.int_pos[1]
            if not is_normal:
                min_y = RADUIS
            else:
                hypotenuse = min_x / math.cos(angle)
                min_y = round(hypotenuse * math.sin(angle))



        # loop
        for s in lst_of_snakes:
            for key_x in s.history:
                if key_x < min_x or key_x > max_x:
                    continue
                if not is_normal:
                    hypotenuse = False
                else:
                    hypotenuse = key_x / math.cos(angle)
                    taregt_y = round(hypotenuse * math.sin(angle))
                for key_y in s.history[key_x]:
                    if min_y <= key_y <= max_y:
                        bo = True
                        if hypotenuse:
                            bo = False
                            if collision_between_two_dots((key_x, key_y), (key_x, taregt_y)):
                                bo = True
                        if bo:
                            # print("uri")
                            temp_dis = math.sqrt(((snake.int_pos[0] - key_x) ** 2) + ((snake.int_pos[1] - key_y) ** 2))
                            if min_dis is None or temp_dis < min_dis:
                                min_dis = temp_dis
                            # break # becuse the rest of the y dont buderr me anymore??
                            # only break if the angle is not 90 or 270

        temp_dis = math.sqrt(((max_x - snake.int_pos[0]) ** 2) + ((max_y - snake.int_pos[1]) ** 2))
        if min_dis is None or temp_dis < min_dis:
            # well is edge
            min_dis = temp_dis

        # TODO also add second well
        lst.append(min_dis)
    return lst


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
