"""Loads a previously trained set of agents and then continues to train one of them.
"""

import argparse
from copy import deepcopy
from random import shuffle

import ray
from ray import tune
from ray.rllib.agents.dqn import DQNTrainer
from ray.rllib.env import PettingZooEnv
from ray.rllib.models import ModelCatalog
from ray.tune.registry import register_env
from ray.rllib.utils.framework import try_import_torch

import cards_env
from best_checkpoints import best_checkpoints
from train_with_random_agents import MaskedRandomPolicy
from train_with_random_agents import TorchMaskedActions
from mask_dqn_model import default_config

torch, nn = try_import_torch()

parser = argparse.ArgumentParser()

parser.add_argument("--num-iters", type=int, default=5000)
parser.add_argument("--num-cpus", type=int, default=2)
parser.add_argument('--cp-filepath', type=str, default='C:/Users/Andre/ray_results/DQN/')

if __name__ == "__main__":

    checkpoints_list = ['4_8', '5_8', '6_8', '7_8']

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

    old_config = default_config()

    old_config["env"] = "cards"
    old_config["multiagent"] = {
        "policies": {
            "player_0": (None, obs_space, act_space, {"model": {"custom_model": "masked_dqn"}}),
            "player_1": (MaskedRandomPolicy, obs_space, act_space, {}),
            "player_2": (MaskedRandomPolicy, obs_space, act_space, {}),
            "player_3": (MaskedRandomPolicy, obs_space, act_space, {}),
        },
        "policy_mapping_fn": lambda agent_id: agent_id,
        "policies_to_train": ["player_0"],
    }

    new_config = deepcopy(old_config)
    new_config["multiagent"] = {
        "policies": {
            "player_0": (None, obs_space, act_space, {"model": {"custom_model": "masked_dqn"}}),
            "player_1": (None, obs_space, act_space, {"model": {"custom_model": "masked_dqn"}}),
            "player_2": (None, obs_space, act_space, {"model": {"custom_model": "masked_dqn"}}),
            "player_3": (None, obs_space, act_space, {"model": {"custom_model": "masked_dqn"}}),
        },
        "policy_mapping_fn": lambda agent_id: agent_id,
        "policies_to_train": ["player_0", "player_1", "player_2", "player_3"],
    }

    # Create a dummy Trainer to load our checkpoint.
    dummy_trainer = DQNTrainer(config=old_config)
    new_trainer = DQNTrainer(config=new_config)
    # Get untrained weights for all policies.
    untrained_weights = new_trainer.get_weights()

    weights_list = {}
    for checkpoint in checkpoints_list:
        # Restore all policies from checkpoint.
        dummy_trainer.restore(best_checkpoints(args.cp_filepath)[checkpoint])
        # Get trained weights
        trained_weights = dummy_trainer.get_weights()
        # Set all the weights to the trained agent weights
        weights_list[checkpoint] = trained_weights['player_0']

    for i in range(args.num_iters):
        weights_dict = {}
        shuffle(checkpoints_list)
        for j, pid in enumerate(untrained_weights.keys()):
            weights_dict[pid] = weights_list[checkpoints_list[j]]
        new_trainer.set_weights(weights_dict)
        # Create the checkpoint from which tune can pick up the
        # experiment.
        new_checkpoint = new_trainer.save()

        results = tune.run(
            "DQN",
            stop={"training_iteration": 10},
            config=new_config,
            checkpoint_freq=1000,
            reuse_actors=True,
            # max_concurrent_trials=1000,
            verbose=1
        )

        print(f'Last checkpoint: {results.get_last_checkpoint(results.trials[0])}')

        trained_weights = new_trainer.get_weights()
        for j, pid in enumerate(trained_weights.keys()):
            weights_list[checkpoints_list[j]] = trained_weights[pid]


    ray.shutdown()