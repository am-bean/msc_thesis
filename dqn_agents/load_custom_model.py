"""Simple example of how to restore only one of n agents from a trained
multi-agent Trainer using Ray tune.

The trick/workaround is to use an intermediate trainer that loads the
trained checkpoint into all policies and then reverts those policies
that we don't want to restore, then saves a new checkpoint, from which
tune can pick up training.

Control the number of agents and policies via --num-agents and --num-policies.
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
from best_checkpoints import best_checkpoints
from train_with_random_agents import MaskedRandomPolicy
from train_with_random_agents import TorchMaskedActions
from mask_dqn_model import default_config

torch, nn = try_import_torch()

parser = argparse.ArgumentParser()

parser.add_argument("--stop-timesteps", type=int, default=1)
parser.add_argument("--num-cpus", type=int, default=4)
parser.add_argument("--checkpoint", type=str, default='0_0')
parser.add_argument('--cp-filepath', type=str, default='C:/Users/Andre/ray_results/DQN/')

if __name__ == "__main__":
    run_new_model = False
    args = parser.parse_args()

    ray.init(num_cpus=args.num_cpus)

    # Get obs- and action Spaces.
    def env_creator():
        env = cards_env.env()
        return env


    ModelCatalog.register_custom_model("masked_dqn", TorchMaskedActions)
    register_env("cards", lambda config: PettingZooEnv(env_creator()))

    single_env = PettingZooEnv(env_creator())
    obs_space = single_env.observation_space
    act_space = single_env.action_space

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

    # Do some training and store the checkpoint.
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

        best_checkpoint = results.get_last_checkpoint(results.trials[0])
    else:
        best_checkpoint = args.cp_filepath + best_checkpoints()[args.checkpoint]
    print(f".. best checkpoint was: {best_checkpoint}")

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
    print(".. checkpoint to restore from (all policies loaded"
          f"): {new_checkpoint}")

    results = tune.run(
        "DQN",
        stop={"timesteps_total": args.stop_timesteps},
        config=new_config,
        checkpoint_freq=1,
        verbose=1
    )



    ray.shutdown()
