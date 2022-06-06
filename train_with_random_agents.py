import os
from copy import deepcopy

import numpy as np
import ray
from ray import tune
from ray.rllib.agents.registry import get_agent_class
from ray.rllib.env import PettingZooEnv
from ray.rllib.models import ModelCatalog
from ray.rllib.utils.framework import try_import_torch
from ray.tune.registry import register_env

from mask_dqn_model import TorchMaskedActions, MaskedRandomPolicy, default_config

import cards_env

torch, nn = try_import_torch()

if __name__ == "__main__":

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
             stop={"timesteps_total": 150000},
             checkpoint_freq=1000,
             config=config,
             )

    print(f'Last checkpoint: {results.get_last_checkpoint(results.trials[0])}')

    ray.shutdown()