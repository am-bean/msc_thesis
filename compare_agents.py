"""Loads a pre-trained agent to play a demo game
"""

from copy import deepcopy

import ray
from ray import tune
from ray.rllib.agents.dqn import DQNTrainer
from ray.rllib.env import PettingZooEnv
from ray.rllib.models import ModelCatalog
from ray.tune.registry import register_env
from ray.rllib.utils.framework import try_import_torch

import cards_env
from best_checkpoints import best_checkpoints
from custom_env_test import MaskedRandomPolicy
from custom_env_test import TorchMaskedActions
from mask_dqn_model import default_config

torch, nn = try_import_torch()

if __name__ == "__main__":

    ray.init(num_cpus=4)

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
        "policies_to_train": ["player_0"],
    }

    # Load the checkpoint.
    first_checkpoint = best_checkpoints()['first_round']
    second_checkpoint = best_checkpoints()['untrained']

    second_config = deepcopy(first_config)
    second_config["multiagent"] = {
        "policies": {
            "player_0": (None, obs_space, act_space, {"model": {"custom_model": "masked_dqn"}}),
            "player_1": (None, obs_space, act_space, {"model": {"custom_model": "masked_dqn"}}),
            "player_2": (None, obs_space, act_space, {"model": {"custom_model": "masked_dqn"}}),
            "player_3": (None, obs_space, act_space, {"model": {"custom_model": "masked_dqn"}}),
        },
        "policy_mapping_fn": lambda agent_id: agent_id,
        "policies_to_train": ["player_0"],
    }

    # Create a dummy Trainer to load our checkpoint.
    first_dummy_trainer = DQNTrainer(config=first_config)
    second_dummy_trainer = DQNTrainer(config=first_config)
    new_trainer = DQNTrainer(config=second_config)
    # Restore all policies from checkpoint.
    first_dummy_trainer.restore(first_checkpoint)
    second_dummy_trainer.restore(second_checkpoint)
    # Get trained weights
    first_trained_weights = first_dummy_trainer.get_weights()
    second_trained_weights = first_dummy_trainer.get_weights()
    # Set all the weights to the trained agent weights
    use_first_trained = ['player_0', 'player_2']
    use_second_trained = ['player_1', 'player_3']
    new_trainer.set_weights({pid: first_trained_weights['player_0'] for pid in use_first_trained})
    new_trainer.set_weights({pid: second_trained_weights['player_0'] for pid in use_second_trained})

    cum_rewards = {'player_0': 0, 'player_1': 0, 'player_2': 0, 'player_3': 0}
    for i in range(200):
        # run until episode ends
        done = False
        my_env.seed(i)
        obs = my_env.reset()
        while not done:
            agent = list(obs.keys())[0]
            action = new_trainer.compute_single_action(obs[agent], policy_id=agent, explore=False)
            action_dict = {agent: action}
            obs, reward, dones, info = my_env.step(action_dict)
            done = dones['__all__']
        for player, reward in reward.items():
            cum_rewards[player] += reward
        print(cum_rewards)

    ray.shutdown()
