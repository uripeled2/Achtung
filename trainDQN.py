
import tensorflow as tf
from tensorflow import keras
import numpy as np
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense
# from tensorflow.keras.optimizers import Adam
from collections import deque
import random
from game import Game
from snake import *
import math
from tensorflow.keras.models import model_from_json
import pygame
import time
import datetime
import matplotlib.pyplot as plt


class DQNAgent:
    def __init__(self, state_size: tuple = (WIDTH, LENGTH), action_size: int = 3):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.frame_to_pass = 2 * RADUIS

    def reshape(self, lst, size: int):
        if len(self.state_size) == 2:
            return np.reshape(lst, (size, self.state_size[0], self.state_size[1]))
        elif len(self.state_size) == 1:
            return np.reshape(lst, (size, self.state_size[0]))
        else:
            raise Exception("Not vaild state_size")

    def _build_model(self):
        ##### MY MODEL #####
        model = keras.Sequential([
            keras.layers.Flatten(input_shape=self.state_size),  # (state_size,) ???
            keras.layers.Dense(256, activation='relu'),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(self.action_size, activation="softmax")
        ])

        model.compile(optimizer='adam',
                      loss='mse',
                      metrics=['accuracy'])
        ##### COPY MODEL ####
        # model = Sequential()
        # model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        # model.add(Dense(24, activation='relu'))
        # model.add(Dense(self.action_size, activation='linear'))
        # model.compile(loss='mse',
        #               optimizer=Adam(lr=self.learning_rate))
        #####################
        return model

    def act(self, state) -> int:
        """
        :param state:
        :return: action: 0 or 1 or 2
        """

        if np.random.random() <= self.epsilon:
            return random.randrange(self.action_size)
        return np.argmax(self.model.predict(state))

    def memorize(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size):
        x_batch, y_batch = [], []
        minibatch = random.sample(
            self.memory, min(len(self.memory), batch_size))
        for state, action, reward, next_state, done in minibatch:
            y_target = self.model.predict(state)
            y_target[0][action] = reward if done else reward + self.gamma * np.max(self.model.predict(next_state)[0])
            x_batch.append(state[0])
            y_batch.append(y_target[0])

        x_batch = self.reshape(x_batch, len(x_batch))
        y_batch = np.reshape(y_batch, [len(y_batch), 3])
        self.model.fit(x_batch, np.array(y_batch))
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


def avg(lst: list) -> float:
    return sum(lst) / len(lst)


if __name__ == "__main__":
    best = 0
    history_game = [[0] * WIDTH for i in range(LENGTH)]
    game = Game([Snake(100, 100, math.pi / 2, (0, 255, 0))], history_game)
    agent = DQNAgent()
    episodes = 300
    display_each = 20
    alert_before = 10
    times = []
    scores = []
    # Iterate the game
    for e in range(episodes):
        start = time.time()

        # reset state in the beginning of each game
        state = game.reset()
        state = agent.reshape(state, 1)

        # PyGame set win
        if e % display_each == 0:
            pygame.init()
            win = pygame.display.set_mode((WIDTH, LENGTH))
            pygame.display.set_caption(F"{e}")
        else:
            win = None
        if e + alert_before % display_each == 0:
            # TODO Set alert using noise
            pass
        game.win = win
        # time_t represents each frame of the game
        # the more time_t the more score
        for time_t in range(200):
            # render
            if win is not None:
                win.fill((0, 0, 0))
                pygame.time.delay(FRAME)
                game.draw()
                pygame.display.update()

            # Decide action
            if time_t % agent.frame_to_pass == 0:
                action = agent.act(state)

            # Advance the game to the next frame based on the action.
            game.lst_of_snakes[0].change_angle(action)
            done = game.all_dead()
            game.move()
            game.search_collision()
            game.add()
            game.fitness()
            next_state = game.history_game
            if not done:
                reward = 1
            else:
                reward = -200
            _ = None
            next_state = agent.reshape(next_state, 1)

            # memorize the previous state, action, reward, and done
            agent.memorize(state, action, reward, next_state, done)

            # make next_state the new current state for the next frame.
            state = next_state

            # done becomes True when the game ends
            if done:
                end = time.time()
                took = end - start
                times.append(took)
                scores.append(time_t)
                if time_t > best:
                    best = time_t
                # print the score and break out of the loop
                print(F"episode: {e}/{episodes} score: {time_t} best: {best} took: {round(took, 2)} "
                      F"average time: {round(avg(times), 2)}")
                break

        # close win
        pygame.quit()

        # train the agent with the experience of the episode
        agent.replay(64)

    print(F"total time: {sum(times)}")

    # serialize model to JSON
    model_json = agent.model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    agent.model.save_weights("model.h5")
    print("Saved model to disk")

    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")

    # plot
    plt.plot(scores)
    plt.ylabel('scores')
    plt.show()
