from snake import *
import pygame
import random
import pickle

pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("First Game")

run = True

winner_net = pickle.load(open("best.pickle", "rb"))
cs1 = Snake(random.randrange(10, 490), random.randrange(10, 490), math.pi / random.randrange(1, 5), (255, 0, 0))
cs2 = Snake(random.randrange(10, 490), random.randrange(10, 490), math.pi / random.randrange(1, 5), (0, 255, 0))
lst_of_snakes = [cs1, cs2]
pause = False
history_game = [[0] * WIDTH for i in range(LENGTH)]
history_game = cs1.add(history_game)
history_game = cs2.add(history_game)

# run game
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
            inp = lst_of_snakes[1].crete_input_nearest_well(history_game)
            print(inp)
            output = winner_net.activate(inp)
            lst_of_snakes[1].change_angle(output.index(max(output)))

        # if keys[pygame.K_a]:
        #     lst_of_snakes[1].direct -= CHENGEANGEL
        # if keys[pygame.K_s]:
        #     lst_of_snakes[1].direct += CHENGEANGEL

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
