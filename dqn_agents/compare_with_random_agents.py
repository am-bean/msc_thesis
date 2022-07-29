"""Loads a pre-trained agent to play a demo game
"""

import argparse
from copy import deepcopy

import ray
from ray import tune
from ray.rllib.agents.dqn import DQNTrainer
from ray.rllib.env import PettingZooEnv
from ray.rllib.models import ModelCatalog
from ray.tune.registry import register_env
from ray.rllib.utils.framework import try_import_torch

import cards_env
from best_checkpoints import best_checkpoints, update_best_checkpoints
from train_with_random_agents import MaskedRandomPolicy
from train_with_random_agents import TorchMaskedActions
from mask_dqn_model import default_config
import numpy as np
import pandas as pd

torch, nn = try_import_torch()

parser = argparse.ArgumentParser()

parser.add_argument("--num-iters", type=int, default=5000)
parser.add_argument("--num-cpus", type=int, default=4)
parser.add_argument("--checkpoint", type=str, default='l1_8')
parser.add_argument('--checkpoints-folder', type=str, default='../data/checkpoints/')


if __name__ == "__main__":
    '''Takes a pre-trained checkpoint and benchmarks the performance competing with random opponents and partner.
    
    Args:
    num-iters: int, how many games to play for the test
    num-cpus: int, how many CPUs to request with Ray
    checkpoint: str, the checkpoint for testing
    '''

    args = parser.parse_args()

    ray.init(num_cpus=args.num_cpus)

    # Get obs- and action Spaces.
    def env_creator():
        env = cards_env.env()
        return env

    ModelCatalog.register_custom_model("masked_dqn", TorchMaskedActions)
    register_env("cards", lambda config: PettingZooEnv(env_creator()))

    my_env = PettingZooEnv(env_creator())
    obs_space = my_env.observation_space
    act_space = my_env.action_space

    # Setup DQN with an ensemble of `num_policies` different policies.

    first_config = default_config()

    first_config["env"] = "cards"
    first_config["multiagent"] = {
        "policies": {
            "player_0": (None, obs_space, act_space, {"model": {"custom_model": "masked_dqn"}}),
            "player_1": (MaskedRandomPolicy, obs_space, act_space, {}),
            "player_2": (MaskedRandomPolicy, obs_space, act_space, {}),
            "player_3": (MaskedRandomPolicy, obs_space, act_space, {}),
        },
        "policy_mapping_fn": lambda agent_id: agent_id,
        "policies_to_train": ['policy_0'],
    }

    # Load the checkpoint.
    first_checkpoint = args.checkpoints_folder + best_checkpoints(args.checkpoints_folder)[args.checkpoint]

    # Create a dummy Trainer to load our checkpoint.
    first_dummy_trainer = DQNTrainer(config=first_config)
    new_trainer = DQNTrainer(config=first_config)
    # Restore all policies from checkpoint.
    first_dummy_trainer.restore(first_checkpoint)
    # Get trained weights
    first_trained_weights = first_dummy_trainer.get_weights()
    new_trainer.set_weights({'player_0': first_trained_weights['player_0']})

    # Loop over games to collect results
    cum_rewards = []
    for i in range(args.num_iters):
        done = False
        my_env.seed(i)
        obs = my_env.reset()
        while not done:
            agent = list(obs.keys())[0]
            if agent == 'player_0':
                action = new_trainer.compute_single_action(obs[agent], policy_id=agent, explore=False)
            else:
                action = np.random.choice(np.nonzero(obs[agent]['action_mask'])[0])
            action_dict = {agent: action}
            obs, reward, dones, info = my_env.step(action_dict)
            done = dones['__all__']
        if 'player_0' in reward.keys():
            cum_rewards.append(reward['player_0'])
        if i%(args.num_iters//5) == (args.num_iters//5)-1:
            print(np.mean(cum_rewards))
            print(np.std(cum_rewards))

    ray.shutdown()
