
import tensorflow as tf
from tensorflow import keras
import numpy as np
from collections import deque
import random
from game import Game
from snake import *
import math
from tensorflow.keras.models import model_from_json
import pygame


class DQNAgent:
    def __init__(self, state_size=(WIDTH, LENGTH), action_size=3):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        model = keras.Sequential([
            keras.layers.Flatten(input_shape=(WIDTH, LENGTH)),
            keras.layers.Dense(256, activation='relu'),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(self.action_size, activation="softmax")
        ])
        model.compile(optimizer='adam',
                      loss='mse',
                      metrics=['accuracy'])
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

        # self.model.fit(np.array(x_batch), np.array(y_batch), batch_size=len(x_batch), verbose=0)
        x_batch = np.reshape(x_batch, [len(x_batch), WIDTH, LENGTH])
        y_batch = np.reshape(y_batch, [len(y_batch), 3])
        self.model.fit(x_batch, np.array(y_batch))
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


if __name__ == "__main__":
    best = 0
    history_game = [[0] * WIDTH for i in range(LENGTH)]
    game = Game([Snake(100, 100, math.pi / 2, (0, 255, 0))], history_game)
    agent = DQNAgent(game)
    episodes = 25_000
    display_each = 3000
    # Iterate the game
    for e in range(episodes):
        # print("start e: ")
        # reset state in the beginning of each game
        state = game.reset()
        state = np.reshape(state, [1, WIDTH, LENGTH])

        # PyGame set win
        if e % display_each == 0:
            pygame.init()
            win = pygame.display.set_mode((WIDTH, LENGTH))
            pygame.display.set_caption(F"{e}")
        else:
            win = None
        game.win = win
        
        # time_t represents each frame of the game
        # Our goal is to keep the pole upright as long as possible until score of 500
        # the more time_t the more score
        for time_t in range(500):
            # render
            if win is not None:
                win.fill((0, 0, 0))
                pygame.time.delay(FRAME)
                game.draw()
                pygame.display.update()

            # Decide action
            action = agent.act(state)

            # Advance the game to the next frame based on the action.
            game.lst_of_snakes[0].change_angle(action)
            done = game.all_dead()
            game.move()
            game.search_collision()
            game.add()
            game.fitness()
            next_state = game.history_game
            reward = 1
            _ = None
            next_state = np.reshape(next_state, [1, WIDTH, LENGTH])

            # memorize the previous state, action, reward, and done
            agent.memorize(state, action, reward, next_state, done)

            # make next_state the new current state for the next frame.
            state = next_state

            # done becomes True when the game ends
            # ex) The agent drops the pole
            if done:
                if time_t > best:
                    best = time_t
                # print the score and break out of the loop
                print(F"episode: {e}/{episodes} score: {time_t} best: {best}")
                break

        # close win
        pygame.quit()

        # train the agent with the experience of the episode
        agent.replay(32)

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



