import os
from copy import deepcopy

import numpy as np
import ray
from ray import tune
from ray.rllib import TorchPolicy, Policy
from ray.rllib.agents.dqn import DQNTrainer
from ray.rllib.agents.dqn.dqn_torch_model import DQNTorchModel
from ray.rllib.examples.policy.random_policy import RandomPolicy
from ray.rllib.agents.registry import get_agent_class
from ray.rllib.env import PettingZooEnv
from ray.rllib.models import ModelCatalog
from ray.rllib.models.torch.fcnet import FullyConnectedNetwork as TorchFC
from ray.rllib.utils.framework import try_import_torch
from ray.rllib.utils.torch_utils import FLOAT_MAX
from ray.tune.registry import register_env
from ray.rllib.utils.annotations import override

from custom_model import TorchMaskedActions, MaskedRandomPolicy

import cards_env

torch, nn = try_import_torch()

if __name__ == "__main__":
    ray.shutdown()
    alg_name = "DQN"
    ModelCatalog.register_custom_model("pa_model", TorchMaskedActions)


    # function that outputs the environment you wish to register.
    def env_creator():
        env = cards_env.env()
        return env


    num_cpus = 2

    config = deepcopy(get_agent_class(alg_name)._default_config)

    register_env("cards", lambda config: PettingZooEnv(env_creator()))

    test_env = PettingZooEnv(env_creator())
    obs_space = test_env.observation_space
    act_space = test_env.action_space

    config["multiagent"] = {
        "policies": {
            "player_0": (None, obs_space, act_space, {"model": {"custom_model": "pa_model"}}),
            "player_1": (MaskedRandomPolicy, obs_space, act_space, {}),
            "player_2": (MaskedRandomPolicy, obs_space, act_space, {}),
            "player_3": (MaskedRandomPolicy, obs_space, act_space, {}),
        },
        "policy_mapping_fn": lambda agent_id: agent_id,
        "policies_to_train": ["player_0"],
    }

    config["v_min"] = -10.0
    config["v_max"] = 10.0
    config["lr"] = 0.001
    config["num_gpus"] = 1 if torch.cuda.is_available() else 0
    config["log_level"] = "DEBUG"
    config["num_workers"] = 1
    config["rollout_fragment_length"] = 30
    config["train_batch_size"] = 200
    config["horizon"] = 200
    config["no_done_at_end"] = False
    config["framework"] = "torch"

    config["n_step"] = 1

    config["exploration_config"] = {
        # The Exploration class to use.
        "type": "EpsilonGreedy",
        # Config for the Exploration class' constructor:
        "initial_epsilon": 0.1,
        "final_epsilon": 0.0,
        "epsilon_timesteps": 100000,  # Timesteps over which to anneal epsilon.
    }
    config["hiddens"] = []
    config["dueling"] = False
    config["env"] = "cards"

    ray.init(num_cpus=num_cpus)

    results = tune.run('DQN',
             stop={"timesteps_total": 1000000},
             checkpoint_freq=1000,
             config=config,
             )
