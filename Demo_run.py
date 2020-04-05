from snake import *

# TODO lst of colors, find from google


def crate_snake(color):
    return Snake(random.choice(range(10, 490)), random.choice(range(10, 490)), random.choice(range(4)), color)


def change_angle(snake, is_left):
    # maybe be more flexible if is_left = 0/1/2
    if is_left is None:
        pass
    elif is_left:
        snake.direct += CHENGEANGEL
    else:
        snake.direct -= CHENGEANGEL


def need_to_stop(lst_of_snakes):
    # stop if only one is alive
    count = 0
    for s in lst_of_snakes:
        if not s.is_dead:
            count += 1
    if count <= 1:
        return True
    return False

lst_of_snakes = []
run = True

while run:
    if need_to_stop(lst_of_snakes):
        run = False
        break
    
        




