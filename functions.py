import numpy as np
import random


start, finish, wall = 'S', 'F', '#'
max_velocity = 1
v_range = range(-max_velocity, max_velocity + 1)


def restart_position(world):
    """Restart agent to a 'S' position on the map"""
    starts = []
    for y, row in enumerate(world):
        for x, col in enumerate(row):
            if col == 'S':
                starts += [(y, x)]

    return starts[0]



def get_policy(cols, rows, v_range, Q, actions):
    """Gets the Q-values of all possible states and determines the best actions based on argmax.
    Returns best actions for each possible state as a policy dictionary"""

    pi_policy = {}
    for y in range(rows):
        for x in range(cols):
            for vy in v_range:
                for vx in v_range:
                    pi_policy[(y, x, vy, vx)] = actions[np.argmax(Q[y][x][vy][vx])]

    return (pi_policy)



def get_new_velocity(old_vel, accel, min_vel=-max_velocity, max_vel=max_velocity):
    """Gets the new velocity is acceleration is applied but need to set max and min limit of velocity"""

    new_vy = old_vel[0] + accel[0]
    new_vx = old_vel[1] + accel[1]
    #If greater than the velocity limit range, set as max/min values
    if new_vx < min_vel:
        new_vx = min_vel
    if new_vx > max_vel:
        new_vx = max_vel
    if new_vy < min_vel:
        new_vy = min_vel
    if new_vy > max_vel:
        new_vy = max_vel

    return new_vy, new_vx



def get_next_location(old_loc, vel):
    """Gets the next new location by adding the old location and velocity values"""
    y, x = old_loc[0], old_loc[1]
    vy, vx = vel[0], vel[1]

    return y + vy, x + vx



def crash_check(map, check_y, check_x):
    """Performs check to see if crash into wall '#' or fell outside of map"""

    rows = len(map)
    cols = len(map[0])

    #If fall outside of map
    if check_y >= rows or check_y <=0 or check_x >=cols or check_x<=0:
        new_y, new_x = restart_position(map)
        return new_y, new_x

    #If land on '#' walls
    elif map[check_y][check_x] == wall:
        new_y, new_x = restart_position(map)
        return new_y, new_x

    else:
        return check_y, check_x



def get_next_move(old_y, old_x, old_vy, old_vx, accel, map, deterministic=True):
    """Get the next states including x,y coordinate and all possible velocities.
    Also handles crash events"""

    epsilon = 0.2
    if deterministic == False:
        # Non-deterministic with 20% chance of failure (acceleration stays 0,0)
        if random.uniform(0,1) < epsilon:
            accel = (0, 0)

    new_vy, new_vx = get_new_velocity((old_vy, old_vx), accel)
    temp_y, temp_x = get_next_location((old_y, old_x), (new_vy, new_vx))
    new_y, new_x = crash_check(map, temp_y, temp_x)

    # If crash...reset velocity
    if map[new_y][new_x] == start:
        new_vy, new_vx = 0, 0

    return new_y, new_x, new_vy, new_vx
