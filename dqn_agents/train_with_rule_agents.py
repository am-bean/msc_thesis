"""Loads a previously trained set of agents and then continues to train one of them.
"""
import os
import shutil
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
from best_checkpoints import best_checkpoints, update_best_checkpoints
from dqn_agents.rule_based_policy import RuleBasedPolicy
from train_with_random_agents import MaskedRandomPolicy
from train_with_random_agents import TorchMaskedActions
from mask_dqn_model import default_config


torch, nn = try_import_torch()

parser = argparse.ArgumentParser()

parser.add_argument("--stop-iters", type=int, default=40000)
parser.add_argument('--checkpoint_freq', type=int, default=10000)
parser.add_argument("--num-cpus", type=int, default=4)
parser.add_argument("--checkpoint", type=str, default='rb4_1')
parser.add_argument("--repetitions", type=int, default=3)
parser.add_argument('--cp-filepath', type=str, default='C:/Users/Administrator/ray_results/DQN/')
parser.add_argument('--local-folder', type=str, default="/tsclient/C/Users/Andre/ray_results/DQN/aws")
parser.add_argument('--checkpoint-name', type=str, default='/checkpoint_040000/checkpoint-40000')
parser.add_argument('--shutdown', type=bool, default=True)


if __name__ == "__main__":

    args = parser.parse_args()

    best_checkpoint = args.cp_filepath + best_checkpoints()[args.checkpoint]
    training_checkpoints = []

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
                "player_1": (RuleBasedPolicy, obs_space, act_space, {}),
                "player_2": (None, obs_space, act_space, {"model": {"custom_model": "masked_dqn"}}),
                "player_3": (RuleBasedPolicy, obs_space, act_space, {}),
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
            checkpoint_freq=args.checkpoint_freq,
            reuse_actors=True,
            verbose=0
        )

        cp = results.get_last_checkpoint(results.trials[0])

        ray.shutdown()

        old_cp = args.checkpoint
        new_cp = old_cp[:-1] + str(int(old_cp[-1]) + 1 + i)
        filepath = args.cp_filepath.replace('/', '\\')
        file = cp.local_path.replace(filepath, "")
        checkpoint_name = args.checkpoint_name
        folder = cp.local_path.replace(checkpoint_name.replace('/', '\\'), "")
        folder_only = folder.replace(filepath, "")
        update_best_checkpoints(file, new_cp)

        training_checkpoints.append(file)
        best_checkpoint = cp

        machine = platform.uname()[1]
        if machine != 'AndrewXPS15':
            src_folder = folder
            dst_folder = args.local_folder + '/' + folder_only
            dst_folder = dst_folder.replace('/', '\\')
            # Using try to protect against the connection to the remote server dropping
            try:
                shutil.copytree(src_folder, "\\" + dst_folder)
                print(f'Copied to {dst_folder}')
            except:
                pass
            unneeded_files = ['params.json', 'params.pkl', 'progress.csv', 'result.json']
            for f in unneeded_files:
                try:
                    os.remove(folder + '/' + f)
                finally:
                    pass

    if machine != 'AndrewXPS15':
        if args.shutdown:
            os.system("shutdown /s /t 30")
    else:
        print(training_checkpoints)
