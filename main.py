from snake import *
import pygame
import random

pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("First Game")

run = True

cs1 = Snake(250, 250, math.pi / 4, (255, 0, 0))
cs2 = Snake(400, 200, math.pi / 2, (0, 255, 0))
lst_of_snakes = [cs1, cs2]

# dict: key = pos_x; value = dict: key = pos_y; value = True;
count = 0

while run:
    win.fill((0, 0, 0))
    pygame.time.delay(FRAME)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

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
        if s1.is_hop or s1.is_dead:
            continue
        elif s1.history.get(s1.int_pos[0]) is None:
            s1.history[s1.int_pos[0]] = {}

        s1.history[s1.int_pos[0]][s1.int_pos[1]] = True

    pygame.display.update()

pygame.quit()
