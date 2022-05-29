"""Simple example of how to restore only one of n agents from a trained
multi-agent Trainer using Ray tune.

The trick/workaround is to use an intermediate trainer that loads the
trained checkpoint into all policies and then reverts those policies
that we don't want to restore, then saves a new checkpoint, from which
tune can pick up training.

Control the number of agents and policies via --num-agents and --num-policies.
"""

import argparse
import gym
import os
import random
from copy import deepcopy

import ray
from ray import tune
from ray.rllib.agents.dqn import DQNTrainer
from ray.rllib.env import PettingZooEnv
from ray.rllib.models import ModelCatalog
from ray.tune.registry import register_env
from ray.rllib.utils.framework import try_import_torch
from ray.rllib.agents.registry import get_agent_class

import cards_env
from custom_env_test import MaskedRandomPolicy
from custom_env_test import TorchMaskedActions
from ray.rllib.utils.framework import try_import_tf
from ray.rllib.utils.test_utils import check_learning_achieved

torch, nn = try_import_torch()

parser = argparse.ArgumentParser()

parser.add_argument("--num-agents", type=int, default=4)
parser.add_argument("--num-policies", type=int, default=2)
parser.add_argument("--pre-training-iters", type=int, default=5)
parser.add_argument("--stop-iters", type=int, default=200)
parser.add_argument("--stop-reward", type=float, default=150)
parser.add_argument("--stop-timesteps", type=int, default=150000)
parser.add_argument("--num-cpus", type=int, default=2)
parser.add_argument("--as-test", action="store_true")
parser.add_argument("--framework", choices=["tf2", "tf", "tfe", "torch"], default="torch")

if __name__ == "__main__":
    args = parser.parse_args()

    ray.init(num_cpus=args.num_cpus)

    # Get obs- and action Spaces.
    def env_creator():
        env = cards_env.env()
        return env

    ModelCatalog.register_custom_model("pa_model", TorchMaskedActions)
    register_env("cards", lambda config: PettingZooEnv(env_creator()))

    single_env = PettingZooEnv(env_creator())
    obs_space = single_env.observation_space
    act_space = single_env.action_space

    # Setup DQN with an ensemble of `num_policies` different policies.

    old_config = deepcopy(get_agent_class('DQN')._default_config)

    old_config["env"] = "cards"
    old_config["env_config"] = {"num_agents": args.num_agents}
    old_config["num_gpus"] = 1 if torch.cuda.is_available() else 0
    old_config["multiagent"] = {
        "policies": {
            "player_0": (None, obs_space, act_space, {"model": {"custom_model": "pa_model"}}),
            "player_1": (MaskedRandomPolicy, obs_space, act_space, {}),
            "player_2": (MaskedRandomPolicy, obs_space, act_space, {}),
            "player_3": (MaskedRandomPolicy, obs_space, act_space, {}),
        },
        "policy_mapping_fn": lambda agent_id: agent_id,
        "policies_to_train": ["player_0"],
        }
    old_config["framework"] = args.framework
    old_config["v_min"] = -10.0
    old_config["v_max"] = 10.0
    old_config["lr"] = 0.001
    old_config["num_gpus"] = 1 if torch.cuda.is_available() else 0
    old_config["log_level"] = "DEBUG"
    old_config["num_workers"] = 1
    old_config["rollout_fragment_length"] = 30
    old_config["train_batch_size"] = 200
    old_config["horizon"] = 200
    old_config["no_done_at_end"] = False
    old_config["framework"] = "torch"

    old_config["n_step"] = 1

    old_config["exploration_config"] = {
        # The Exploration class to use.
        "type": "EpsilonGreedy",
        # Config for the Exploration class' constructor:
        "initial_epsilon": 0.1,
        "final_epsilon": 0.0,
        "epsilon_timesteps": 100000,  # Timesteps over which to anneal epsilon.
    }
    old_config["hiddens"] = []
    old_config["dueling"] = False
    old_config["env"] = "cards"

    # Do some training and store the checkpoint.
    run_new_model = False
    if run_new_model:
        results = tune.run(
            "DQN",
            config=old_config,
            stop={"timesteps_total": 150000},
            verbose=1,
            checkpoint_freq=1000,
            checkpoint_at_end=True,
        )

    print("Pre-training done.")

    # Load previously trained best checkpoint
    if run_new_model:
        best_checkpoint = results.get_last_checkpoint(results.trials[0], mode="max")
    else:
        best_checkpoint = "C:/Users/Andre/ray_results/DQN" + "/DQN_cards_ab6b7_00000_0_2022-05-28_07-30-30/checkpoint_032000/checkpoint-32000"
    print(f".. best checkpoint was: {best_checkpoint}")

    new_config = deepcopy(old_config)
    new_config["multiagent"] = {
        "policies": {
            "player_0": (None, obs_space, act_space, {"model": {"custom_model": "pa_model"}}),
            "player_1": (None, obs_space, act_space, {"model": {"custom_model": "pa_model"}}),
            "player_2": (None, obs_space, act_space, {"model": {"custom_model": "pa_model"}}),
            "player_3": (None, obs_space, act_space, {"model": {"custom_model": "pa_model"}}),
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
    print(".. checkpoint to restore from (all policies loaded"
          f"): {new_checkpoint}")

    print("Starting new tune.run")

    # Start our actual experiment.
    stop = {
        "timesteps_total": args.stop_timesteps
    }

    # Make sure, the non-1st policies are not updated anymore.
    new_config["multiagent"]["policies_to_train"] = ["policy_0"]

    results = tune.run(
        "DQN",
        stop=stop,
        config=new_config,
        checkpoint_freq=1000,
        verbose=1
    )

    ray.shutdown()