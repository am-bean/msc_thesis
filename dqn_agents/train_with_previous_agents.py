"""Loads a previously trained set of agents and then continues to train one of them.
"""
import os
import platform
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
from best_checkpoints import best_checkpoints
from train_with_random_agents import MaskedRandomPolicy
from train_with_random_agents import TorchMaskedActions
from mask_dqn_model import default_config


torch, nn = try_import_torch()

parser = argparse.ArgumentParser()

parser.add_argument("--stop-iters", type=int, default=40000)
parser.add_argument("--num-cpus", type=int, default=4)
parser.add_argument("--checkpoint", type=str, default='l8_1')
parser.add_argument("--repetitions", type=int, default=1)
parser.add_argument('--cp-filepath', type=str, default='C:/Users/Administrator/ray_results/DQN/')

if __name__ == "__main__":

    args = parser.parse_args()

    best_checkpoint = best_checkpoints(args.cp_filepath)[args.checkpoint]
    training_checkpoints = []

    for _ in range(args.repetitions):
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
            "policies_to_train": ["player_0"],
        }

        # Create a dummy Trainer to load our checkpoint.
        dummy_trainer = DQNTrainer(config=old_config)
        new_trainer = DQNTrainer(config=new_config)
        # Get untrained weights for all policies.
        untrained_weights = new_trainer.get_weights()
        # Restore all policies from checkpoint.
        dummy_trainer.restore(best_checkpoint)
        # Get trained weights
        trained_weights = dummy_trainer.get_weights()
        # Set all the weights to the trained agent weights
        new_trainer.set_weights({pid: trained_weights['player_0'] for pid, _ in untrained_weights.items()})
        # Create the checkpoint from which tune can pick up the
        # experiment.
        new_checkpoint = new_trainer.save()

        results = tune.run(
            "DQN",
            stop={"training_iteration": args.stop_iters},
            config=new_config,
            checkpoint_freq=1000,
            reuse_actors=True,
            verbose=1
        )

        cp = results.get_last_checkpoint(results.trials[0])
        print(f'The checkpoint string below needs to be added to the best_checkpoints file')
        print(f'Then update the variable at the top of this file to the next number e.g. 5_2 and run it again')
        print(f'Last checkpoint: {cp}')

        ray.shutdown()

        training_checkpoints.append(cp)
        best_checkpoint = cp

    print(training_checkpoints)
    machine = platform.uname()[1]

    if machine != 'AndrewXPS15':
        os.system("shutdown /s /t 30")
