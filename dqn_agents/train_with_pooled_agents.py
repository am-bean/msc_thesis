"""Loads a previously trained set of agents and then continues to train one of them.
"""

import re
import argparse
import os
import platform
import shutil
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
from best_checkpoints import best_checkpoints, update_best_checkpoints
from train_with_random_agents import MaskedRandomPolicy
from train_with_random_agents import TorchMaskedActions
from mask_dqn_model import default_config

torch, nn = try_import_torch()

parser = argparse.ArgumentParser()

parser.add_argument("--stop-iters", type=int, default=5000)
parser.add_argument('--checkpoint_freq', type=int, default=5000)
parser.add_argument("--num-cpus", type=int, default=4)
parser.add_argument("--repetitions", type=int, default=32)
parser.add_argument("--checkpoint", type=str, default='l3_4')
parser.add_argument('--cp-filepath', type=str, default='C:/Users/Administrator/ray_results/DQN/')
parser.add_argument('--local-folder', type=str, default="/tsclient/C/Users/Andre/ray_results/DQN/aws")
parser.add_argument('--shutdown', type=bool, default=True)
parser.add_argument('--copy_to_local', type=bool, default=False)
parser.add_argument('--use-checkpoints', type=bool, default=False)

if __name__ == "__main__":

    args = parser.parse_args()

    checkpoints_pool = ['l1_4', 'l2_4', 'l3_4', 'l4_4']
    checkpoints_pool.append(args.checkpoint)
    checkpoints_pool = list(set(checkpoints_pool))
    raw_checkpoints_pool = checkpoints_pool.copy()

    subs = {'a': '\checkpoint_010000\checkpoint-10000',
            'b': '\checkpoint_020000\checkpoint-20000',
            'c': '\checkpoint_030000\checkpoint-30000'}

    if args.use_checkpoints:
        for checkpoint in raw_checkpoints_pool:
            for sub in subs.keys():
                checkpoints_pool.append(checkpoint + sub)

    for i in range(args.repetitions):

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

        weights_list = {}
        for checkpoint in checkpoints_pool:
            # Restore all policies from checkpoint.
            if checkpoint[-1] in subs.keys():
                long_checkpoint = best_checkpoints()[checkpoint[:-1]].replace('\checkpoint_040000\checkpoint-40000', subs[checkpoint[-1]])
            else:
                long_checkpoint = best_checkpoints()[checkpoint]
            dummy_trainer.restore(args.cp_filepath + long_checkpoint)
            # Get trained weights
            trained_weights = dummy_trainer.get_weights()
            # Set all the weights to the trained agent weights
            weights_list[checkpoint] = trained_weights['player_0']

        weights_dict = {}
        shuffle(checkpoints_pool)
        for j, pid in enumerate(untrained_weights.keys()):
            if pid == 'player_0':
                weights_dict[pid] = weights_list[args.checkpoint]
            else:
                weights_dict[pid] = weights_list[checkpoints_pool[j]]
        new_trainer.set_weights(weights_dict)
        # Create the checkpoint from which tune can pick up the
        # experiment.
        new_checkpoint = new_trainer.save()

        results = tune.run(
            "DQN",
            stop={"training_iteration": args.stop_iters},
            config=new_config,
            checkpoint_freq=args.checkpoint_freq,
            reuse_actors=True,
            # max_concurrent_trials=1000,
            verbose=1
        )

        cp = results.get_last_checkpoint(results.trials[0])

        ray.shutdown()

        filepath = args.cp_filepath.replace('/', '\\')
        file = cp.local_path.replace(filepath, "")
        folder = re.sub(r"checkpoint.*$", "", cp.local_path)
        folder_only = folder.replace(filepath, "")

        if args.copy_to_local:
            src_folder = folder
            dst_folder = args.local_folder + '/' + folder_only
            dst_folder = dst_folder.replace('/', '\\')
            # Using try to protect against the connection to the remote server dropping
            try:
                shutil.copytree(src_folder, "\\" + dst_folder)
                print(f'Copied to {dst_folder}')
            except:
                pass

        trained_weights = new_trainer.get_weights()
        for j, pid in enumerate(trained_weights.keys()):
            weights_list[checkpoints_pool[j]] = trained_weights[pid]

        ray.shutdown()
