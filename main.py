from game import Game
from snake import *

import pygame
import random


pygame.init()

win = pygame.display.set_mode((WIDTH, LENGTH))
pygame.display.set_caption("First Game")

run = True

cs1 = Snake(random.randrange(10, 490), random.randrange(10, 490), math.pi / random.randrange(1, 5), (255, 0, 0))
cs2 = Snake(random.randrange(10, 490), random.randrange(10, 490), math.pi / random.randrange(1, 5), (0, 255, 0))
lst_of_snakes = [cs1, cs2]
pause = False
history_game = [[0] * WIDTH for i in range(LENGTH)]
history_game = cs1.add(history_game)
history_game = cs2.add(history_game)

game = Game(lst_of_snakes, history_game, win)

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
        # change angles
        if keys[pygame.K_LEFT]:
            lst_of_snakes[0].direct -= CHENGEANGEL
        if keys[pygame.K_RIGHT]:
            lst_of_snakes[0].direct += CHENGEANGEL
        if keys[pygame.K_a]:
            lst_of_snakes[1].direct -= CHENGEANGEL
        if keys[pygame.K_s]:
            lst_of_snakes[1].direct += CHENGEANGEL

        if not game.update():
            run = False
            break

        pygame.display.update()

pygame.quit()

