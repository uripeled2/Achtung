
from snake import *


class Game:
    def __init__(self, lst_of_snakes, history_game, win=None, train=False):
        self.lst_of_snakes = lst_of_snakes
        self.history_game = history_game
        self.win = win
        self.train = train

    def update(self, to_draw: bool = True) -> bool:
        """
        Update the game
        :param to_draw:
        :return: if the game end or not
        """

        def move(self):
            """ moves the snakes"""
            for s in self.lst_of_snakes:
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

        def draw(self):
            """ draw the snakes"""
            draw_all(self.win, self.lst_of_snakes, self.history_game)

        def search_collision(self):
            """  search for every snake if it is collided"""
            for s1 in self.lst_of_snakes:
                if s1.is_dead:
                    continue
                if s1.outside():
                    continue
                if not s1.is_hop:
                    s1.collision(self.history_game)

        def add(self):
            """ update the history_game, necessary for the game to keep runing"""
            for s1 in self.lst_of_snakes:
                if s1.is_hop:
                    continue
                self.history_game = s1.add(self.history_game)

        def fintess(self):
            pass

        def to_stop(self) -> bool:
            """

            :param self:
            :return: if the game reach to end
            """
            temp = 0
            for s in self.lst_of_snakes:
                if not s.is_dead:
                    temp += 1
            if temp <= 1:
                return True
            return False

        # execute the functions above in the right order
        if not to_stop(self):
            move(self)
            if self.win is not None and to_draw:
                draw(self)
            search_collision(self)
            add(self)
            return True
        else:
            return False


