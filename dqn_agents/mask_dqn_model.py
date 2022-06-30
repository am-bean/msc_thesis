import numpy as np

from copy import deepcopy
import multiprocessing

from ray.rllib.agents.dqn.dqn_torch_model import DQNTorchModel
from ray.rllib.agents.registry import get_trainer_class
from ray.rllib.examples.policy.random_policy import RandomPolicy
from ray.rllib.models.torch.fcnet import FullyConnectedNetwork as TorchFC
from ray.rllib.utils.framework import try_import_torch
from ray.rllib.utils.torch_utils import FLOAT_MAX
from ray.rllib.utils.annotations import override


from dqn_agents import cards_env

torch, nn = try_import_torch()

class TorchMaskedActions(DQNTorchModel):
    """PyTorch version of above ParametricActionsModel."""

    def __init__(self, obs_space, action_space, num_outputs, model_config, name, **kw):
        DQNTorchModel.__init__(
            self, obs_space, action_space, action_space.n, model_config, name, **kw
        )

        self.action_embed_model = TorchFC(
            obs_space,  # obs_space: gym.spaces.space.Space
            action_space,  # action_space: gym.spaces.space.Space
            action_space.n,  # num_outputs: int
            model_config,  # model_config: dict
            name + "_action_embed",
        )
        self.obs_space = obs_space

        self.action_shape = action_space.n

    @override(DQNTorchModel)
    def forward(self, input_dict, state, seq_lens):
        # Extract the available actions tensor from the observation.
        action_mask = input_dict["obs"]["action_mask"]
        obs = input_dict["obs"]["observation"]

        obs = torch.reshape(obs, (-1, 600))

        combined_obs = torch.cat([action_mask, obs], dim=1)

        # Compute the predicted action embedding
        action_logits, _ = self.action_embed_model(
            {"obs": combined_obs}
        )

        # turns probit action mask into logit action mask
        inf_mask = torch.clamp(torch.log(action_mask), -1e10, FLOAT_MAX)
        masked_actions = action_logits + inf_mask
        return masked_actions, state

    def value_function(self):
        return self.action_embed_model.value_function()


class MaskedRandomPolicy(RandomPolicy):
    """Hand-coded policy that returns random actions within the action mask."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @override(RandomPolicy)
    def compute_actions(
            self,
            obs_batch,
            state_batches=None,
            prev_action_batch=None,
            prev_reward_batch=None,
            **kwargs
    ):
        # Alternatively, a numpy array would work here as well.
        # e.g.: np.array([random.choice([0, 1])] * len(obs_batch))

        return [np.random.choice(obs[:cards_env.N_CARDS].nonzero()[0]) for obs in obs_batch], [], {}


def default_config():
    config = deepcopy(get_trainer_class('DQN')._default_config)

    config["v_min"] = -10.0
    config["v_max"] = 10.0
    config["lr"] = 0.001
    config["num_gpus"] = 1 if torch.cuda.is_available() else 0

    config["num_workers"] = 1
    config["rollout_fragment_length"] = 30
    config["train_batch_size"] = 200
    config["horizon"] = 200
    config["no_done_at_end"] = False
    config["framework"] = "torch"
    config["log_level"] = "WARN"

    config["n_step"] = 1

    config["exploration_config"] = {
        # The Exploration class to use.
        "type": "StochasticSampling", #EpsilonGreedy
        # Config for the Exploration class' constructor:
        #"initial_epsilon": 0.1,
        #"final_epsilon": 0.0,
        #"epsilon_timesteps": 100000,  # Timesteps over which to anneal epsilon.
    }
    config["hiddens"] = []
    config["dueling"] = False

    return config
