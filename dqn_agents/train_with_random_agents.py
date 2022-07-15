"""Trains a new DQN agent in the cards environment with random partners and opponents"""

import os
import re
import shutil

import ray
import argparse
from ray import tune
from ray.rllib.env import PettingZooEnv
from ray.rllib.models import ModelCatalog
from ray.rllib.utils.framework import try_import_torch
from ray.tune.registry import register_env

from dqn_agents.best_checkpoints import update_best_checkpoints
from dqn_agents.mask_dqn_model import TorchMaskedActions, MaskedRandomPolicy, default_config

from dqn_agents import cards_env

torch, nn = try_import_torch()

parser = argparse.ArgumentParser()

parser.add_argument("--stop-iters", type=int, default=1)
parser.add_argument("--checkpoint-freq", type=int, default=1)
parser.add_argument("--checkpoint", type=str, default='0_0')
parser.add_argument('--checkpoints-folder', type=str, default='C:/Users/Andre/ray_results/DQN/')
parser.add_argument('--local-folder', type=str, default="/tsclient/C/Users/Andre/ray_results/DQN/aws")
parser.add_argument('--checkpoint-name', type=str, default='/checkpoint_000001/checkpoint-1')
parser.add_argument('--copy_to_local', type=bool, default=False)
parser.add_argument('--shutdown', type=bool, default=True)

if __name__ == "__main__":

    args = parser.parse_args()

    ray.shutdown()
    alg_name = "DQN"
    ModelCatalog.register_custom_model("masked_dqn", TorchMaskedActions)

    # function that outputs the environment you wish to register.
    def env_creator():
        env = cards_env.env()
        return env


    num_cpus = 2

    config = default_config()

    register_env("cards", lambda config: PettingZooEnv(env_creator()))

    test_env = PettingZooEnv(env_creator())
    obs_space = test_env.observation_space
    act_space = test_env.action_space

    config["multiagent"] = {
        "policies": {
            "player_0": (None, obs_space, act_space, {"model": {"custom_model": "masked_dqn"}}),
            "player_1": (MaskedRandomPolicy, obs_space, act_space, {}),
            "player_2": (MaskedRandomPolicy, obs_space, act_space, {}),
            "player_3": (MaskedRandomPolicy, obs_space, act_space, {}),
        },
        "policy_mapping_fn": lambda agent_id: agent_id,
        "policies_to_train": ["player_0"],
    }
    config['env'] = 'cards'

    ray.init(num_cpus=num_cpus)

    results = tune.run('DQN',
             stop={"training_iteration": args.stop_iters},
             checkpoint_freq=args.checkpoint_freq,
             config=config,
             verbose=0
             )

    ray.shutdown()

    cp = results.get_last_checkpoint(results.trials[0])
    filepath = args.checkpoints_folder.replace('/', '\\')
    file = cp.local_path.replace(filepath, "")
    folder = re.sub(r"checkpoint.*$", "", cp.local_path)
    folder_only = folder.replace(filepath, "")
    update_best_checkpoints(file, args.checkpoint)

    if args.copy_to_local:
        src_folder = folder
        dst_folder = args.local_folder + '/' + folder_only
        dst_folder = dst_folder.replace('/', '\\')
        shutil.copytree(src_folder, "\\" + dst_folder)

        # TODO: remove this and set the correct ENV variable to make it obsolete
        unneeded_files = ['params.json', 'params.pkl', 'progress.csv', 'result.json']
        for f in unneeded_files:
            os.remove(folder + '/' + f)

        if args.shutdown:
            os.system("shutdown /s /t 30")
