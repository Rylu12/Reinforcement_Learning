import pickle
import value_iter as v
import q_sarsa as qs
import read_print_map



text_file = 'R-track.txt'
policy_file = 'R_policy_SARSA.pickle'
noWall = True

#Read and print ASCII race map
race_map = read_print_map.read_map(text_file)
read_print_map.print_map(race_map)

#For Q-Learning and SARSA
num_episodes = 50000

#Get policy from using q_learning
policy = qs.q_sarsa(map = race_map, gamma = 0.9, alpha = 0.25, q_learning = True, max_episodes = num_episodes)



#For value iteration
iterations = 10

#Get policy from using value iteration algorithm
#policy = v.value_iteration(map = race_map, gamma=0.8, iterations = iterations)

#Save policy for testing demo later as pickle file
with open(policy_file, 'wb') as handle:
    pickle.dump(policy, handle, protocol=pickle.HIGHEST_PROTOCOL)
