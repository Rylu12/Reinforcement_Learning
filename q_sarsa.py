import time
import numpy as np
from functions import *
import random

start, finish, wall = 'S', 'F', '#'

max_velocity = 1
v_range = range(-max_velocity, max_velocity + 1)

# All possible default actions
actions_acc = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]


def q_sarsa(map, reward=0, gamma=0.9, alpha=0.25, q_learning = True, max_episodes=500000):
    """Uses the Q-learning or SARSA algorithm to search the state space and generate a policy"""

    episode_steps = 1000

    rows = len(map)
    cols = len(map[0])
    row_range = range(rows)
    col_range = range(cols)

    # initialize Q
    Q = [[[[[0 for a in actions_acc] for vy in v_range] for vx in v_range] for col in row] for row in map]


    for episode in range(max_episodes):

        if episode % 2000 == 0:
            print("Episode:", episode)

        # reset all goal states to reward value
        for y in range(rows):
            for x in range(cols):
                if map[y][x] == finish:
                    Q[y][x] = [[[reward for a in actions_acc] for vy in v_range] for vx in v_range]


        # Choose random initial state
        y = np.random.choice(row_range)
        x = np.random.choice(col_range)
        vy = np.random.choice(v_range)
        vx = np.random.choice(v_range)

        # Reward as a cost function
        r = -1

        # Set percent want to explore
        epsilon = 0.2

        #Q-learning algorithm
        if q_learning == True:

            for step in range(episode_steps):
                if map[y][x] == finish:
                    break
                if map[y][x] == wall:
                    break

                #Random exploration 20% chance
                if random.uniform(0,1) < epsilon:
                    a = random.choice(np.arange(0,9))
                 #   print('Random action: ', a)
                else:
                    a = np.argmax(Q[y][x][vy][vx])
                  #  print('Not random action: ', a)

                new_y, new_x, new_vy, new_vx = get_next_move(y, x, vy, vx, actions_acc[a], map,
                                                             deterministic=False)

                new_value = alpha * (r + gamma * max(Q[new_y][new_x][new_vy][new_vx]))

                # Temporal Difference
                Q[y][x][vy][vx][a] = ((1 - alpha) * Q[y][x][vy][vx][a] + new_value)

                y, x, vy, vx = new_y, new_x, new_vy, new_vx


        #SARSA algorithm
        else:

            a = np.argmax(Q[y][x][vy][vx])

            for step in range(episode_steps):
                if map[y][x] == finish:
                    break
                if map[y][x] == wall:
                    break

                #Random exploration 20% chance
                if random.uniform(0,1) < epsilon:
                    a = random.choice(np.arange(0,9))

                new_y, new_x, new_vy, new_vx = get_next_move(y, x, vy, vx, actions_acc[a], map,
                                                             deterministic=False)

                new_a = np.argmax(Q[new_y][new_x][new_vy][new_vx])

                new_value = alpha * (r + gamma * Q[new_y][new_x][new_vy][new_vx][new_a])

                # Temporal Difference
                Q[y][x][vy][vx][a] = ((1 - alpha) * Q[y][x][vy][vx][a] + new_value)

                y, x, vy, vx = new_y, new_x, new_vy, new_vx
                a = new_a

    policy = (get_policy(cols, rows, v_range, Q, actions_acc))
    return policy