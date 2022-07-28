"""Simulates playing games in the cards environment with random partners and opponents

"""

import argparse
import json

from ray.rllib.env import PettingZooEnv
from ray.tune.registry import register_env
from ray.rllib.utils.framework import try_import_torch

import cards_env
import numpy as np

torch, nn = try_import_torch()

parser = argparse.ArgumentParser()

parser.add_argument("--num-games", type=int, default=35)
parser.add_argument("--num-samples", type=int, default=1000)
parser.add_argument("--filename", type=str, default='simulation.json')

if __name__ == "__main__":
    '''Tests random agents to generate a distribution for bootstrapping

    Args:
    num-iters: int, how many games to play for the test
    num-cpus: int, how many CPUs to request with Ray
    first-checkpoint: str, the first checkpoint for testing
    second-checkpoint: str, the second checkpoint for testing
    '''

    args = parser.parse_args()

    # Get obs- and action Spaces.
    def env_creator():
        env = cards_env.env()
        return env

    my_env = PettingZooEnv(env_creator())

    # Loop over games to collect results
    cum_rewards = {'player_0': 0, 'player_1': 0, 'player_2': 0, 'player_3': 0}
    rewards_list = []

    for j in range(args.num_samples):
        for i in range(args.num_games):
            done = False
            my_env.seed(j*args.num_games+i+1)
            np.random.seed(j*args.num_games+i+1)
            obs = my_env.reset()
            while not done:
                agent = list(obs.keys())[0]
                action = np.random.choice(np.nonzero(obs[agent]['action_mask'])[0])
                action_dict = {agent: action}
                obs, reward, dones, info = my_env.step(action_dict)
                done = dones['__all__']
            for player, reward in reward.items():
                cum_rewards[player] += reward
            if i == args.num_games - 1:
                if j%2 == 0:
                    rewards_list.append(cum_rewards['player_0'])
                else:
                    rewards_list.append(cum_rewards['player_1'])
        if j % (args.num_samples // 10) == 0:
            print(j)
        cum_rewards = {'player_0': 0, 'player_1': 0, 'player_2': 0, 'player_3': 0}
    with open(args.filename, 'w') as f:
        json.dump(rewards_list, f)
    f.close()

