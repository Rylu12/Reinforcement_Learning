import copy
import read_print_map
import time
import functions
import pickle
import random



def demo_simulate(map, policy, pause_time=0.1, animate=False):
    """ Function simulate the number of steps required for agent to reach finish goal using
    policy from value iteration or pretrained from Q-learning/SARSA"""


    starting_coord = functions.restart_position(map)
    y, x = starting_coord
    vy, vx = 0, 0
    stuck_count = 0

    map_display = copy.deepcopy(map)

    for i in range(1000):
        #Snowman unicode
        map_display[y][x] = u'\u2603'

        if animate == True:
            read_print_map.print_map(map_display)
            time.sleep(pause_time)


        map_display[y][x] = '.'
        actions = policy[(y, x, vy, vx)]

        if map[y][x] == 'F':
            return i

        y, x, vy, vx = functions.get_next_move(y, x, vy, vx, actions, map, deterministic=False)

        #Check if agent stuck, if so, needs more iteration/training
        if vy == 0 and vx == 0:
            stuck_count += 1
        else:
            stuck_count = 0

        if stuck_count == 10:
            print("Agent stuck at position %d,%d, terminate demo simulation." % (y, x))
            return i

    print("1000 steps allowed only...ending simulation")
    return 1000

###########################################################
#Program starts here and uses demo function above

map_txt = 'R-track.txt'
policy_file = 'R_policy_SARSA.pickle'
random.seed(1)

# Read in race track map
world = read_print_map.read_map(map_txt)

with open(policy_file, 'rb') as handle:
    policy = pickle.load(handle)

num_races = 100
total_steps = 0

for num in range(num_races):
    total_steps += demo_simulate(world, policy, animate=True)

avg_race_steps = total_steps/num_races

print("Race now completed! ", avg_race_steps, " is the avg step count.")