from gym.spaces import MultiBinary, Discrete, Dict
import numpy as np
import functools
from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector
from pettingzoo.utils import wrappers

N_CARDS = 24
N_AGENTS = 4
N_ITERS = N_CARDS // N_AGENTS

TRUMP = 'S'
SUITS = ['S', 'C', 'D', 'H']
RANKS = ['9', '10', 'J', 'Q', 'K', 'A']
NONE = np.zeros([1, N_CARDS])

SUIT_LOOKUP = {}
SUIT_REVERSE = {}
for i, suit in enumerate(SUITS):
    SUIT_LOOKUP[suit] = i
    SUIT_REVERSE[i] = suit

RANK_LOOKUP = {}
RANK_REVERSE = {}
for i, rank in enumerate(RANKS):
    RANK_LOOKUP[rank] = i
    RANK_REVERSE[i] = rank


def env():
    """
    The env function often wraps the environment in wrappers by default.
    You can find full documentation for these methods
    elsewhere in the developer documentation.
    """
    env = raw_env()
    # This wrapper is only for environments which write results to the terminal
    env = wrappers.CaptureStdoutWrapper(env)
    # Provides a wide vareity of helpful user errors
    # Strongly recommended
    env = wrappers.OrderEnforcingWrapper(env)
    return env


class raw_env(AECEnv):
    """
    The metadata holds environment constants. From gym, we inherit the "render_modes",
    metadata which specifies which modes can be put into the render() method.
    At least human mode should be supported.
    The "name" metadata allows the environment to be pretty printed.
    """

    metadata = {"render_modes": ["human"], "name": "cards"}

    def __init__(self):
        """
        The init method takes in environment arguments and
         should define the following attributes:
        - possible_agents
        - action_spaces
        - observation_spaces

        These attributes should not be changed after initialization.
        """
        self.state_seed = None
        self.possible_agents = ["player_" + str(r) for r in range(N_AGENTS)]
        self.partners = {"player_" + str(int(r + N_AGENTS / 2) % N_AGENTS): "player_" + str(r) for r in range(N_AGENTS)}
        self.agent_name_mapping = dict(
            zip(self.possible_agents, list(range(len(self.possible_agents))))
        )

        # Gym spaces are defined and documented here: https://gym.openai.com/docs/#spaces
        self._action_spaces = {agent: Discrete(N_CARDS) for agent in self.possible_agents}
        self._observation_spaces = {
            agent: Dict(
                {"observation": MultiBinary([N_CARDS + 1, N_CARDS]),
                 "action_mask": Discrete(N_CARDS),
                 }
            ) for agent in self.possible_agents
        }

    # this cache ensures that same space object is returned for the same agent
    # allows action space seeding to work as expected
    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        # Gym spaces are defined and documented here: https://gym.openai.com/docs/#spaces
        return Discrete(N_CARDS)

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        return Dict(
            {"observation": MultiBinary([N_CARDS + 1, N_CARDS]),
             "action_mask": MultiBinary(N_CARDS),
             }
        )

    def render(self, mode="human"):
        """
        Renders the environment. In human mode, it can write to terminal, open
        up a graphical window, or open up some other display that a human can see and understand.
        """
        if all(self.dones.values()):
            print("Game over")
        else:
            print(f"Current round: {self.current_round}")
            print(f"Tricks taken: {self.tricks_taken}")
            print(f"Current play: {self.cards_played}")
            print(f"Current hand: {self.hands[self.agent_selection]}")

    def observe(self, agent):
        """
        Observe should return the observation of the specified agent. This function
        should return a sane observation (though not necessarily the most up to date possible)
        at any time after reset() is called.
        """
        # observation of one agent is the previous state of the other
        return self.observations[agent]

    def close(self):
        """
        Close should release any graphical displays, subprocesses, network connections
        or any other environment data which should not be kept around after the
        user is no longer using the environment.
        """
        pass

    def seed(self, state_seed):
        self.state_seed = state_seed

    def reset(self, state_seed=None):
        """
        Reset needs to initialize the following attributes
        - agents
        - rewards
        - _cumulative_rewards
        - dones
        - infos
        - agent_selection
        And must set up the environment so that render(), step(), and observe()
        can be called without issues.

        Here it sets up the state dictionary which is used by step() and the observations dictionary which is used by step() and observe()
        """
        # Use the same seed for sets of four seats, but rotate who goes first
        if state_seed:
            self.state_seed = state_seed
            np.random.seed(self.state_seed - self.state_seed % 4)
            first_index = self.state_seed % 4
        elif self.state_seed:
            np.random.seed(self.state_seed - self.state_seed % 4)
            first_index = self.state_seed % 4
        else:
            first_index = np.random.choice([0, 1, 2, 3], 1)[0]
        self.agents = self.possible_agents[first_index:]
        self.agents.extend(self.possible_agents[:first_index])
        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.dones = {agent: False for agent in self.agents}
        self.illegal_move = False

        self.hands = {agent: {} for agent in self.agents}
        self.private_info = {agent: [] for agent in self.agents}
        self.private_observations = {agent: NONE.copy() for agent in self.agents}
        self.__deal_cards()
        self.public_info = []
        self.public_observation = np.zeros([N_CARDS, N_CARDS])

        self.action_masks = {agent: self.private_observations[agent].flatten() for agent in self.agents}
        self.infos = {agent: {'public': self.public_info, 'private': self.private_info[agent]} for agent in self.agents}
        self.state = {agent: NONE.copy() for agent in self.agents}

        self.observations = {
            agent: {'observation': np.append(self.private_observations[agent], self.public_observation, axis=0),
                    'action_mask': self.action_masks[agent]}
            for agent in self.agents}
        self.current_round = 0
        self.tricks_taken = {agent: 0 for agent in self.agents}

        self.cards_played = {agent: '' for agent in self.agents}
        self.has_lead = self.agents[0]
        """
        Our agent_selector utility allows easy cyclic stepping through the agents list.
        """
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.next()

        # Ensure relevant information is updated
        for i in self.agents:
            self.__update_action_mask(i)
            self.__update_observation(i)
            # obs = self.observe(i)
        # tensorboardprint('finished reset')

    def step(self, action):
        """
        step(action) takes in an action for the current agent (specified by
        agent_selection) and needs to update
        - rewards
        - _cumulative_rewards (accumulating the rewards)
        - dones
        - infos
        - agent_selection (to the next agent)
        And any internal state used by observe() or render()
        """

        one_hot_action = NONE.copy()
        one_hot_action[0, action] = 1
        agent = self.agent_selection
        this_round = self.current_round

        if self.dones[self.agent_selection]:
            # handles stepping an agent which is already done
            # accepts a None action for the one agent, and moves the agent_selection to
            # the next done agent,  or if there are no more done agents, to the next live agent
            # Updates the results of the trick
            if self._agent_selector.is_last() and not self.illegal_move:
                winning_agent = self.__choose_winner()
                # Increments the winner's tricks taken
                self.tricks_taken[winning_agent] += 1
                self.tricks_taken[self.partners[winning_agent]] += 1
                self._accumulate_rewards()
            return self._was_done_step(None)

        # Check for valid moves
        if (sum(self.action_masks[agent]) == 0) and not self.dones[agent]:
            print('No legal moves')
            self.dones = {agent: True for agent in self.agents}
            for i in self.agents:
                self.rewards[i] = 0
            self.rewards[agent] = 0
            self._accumulate_rewards()
            return

        if self.action_masks[agent][action] == 0:
            self.dones = {agent: True for agent in self.agents}
            for i in self.agents:
                self.rewards[i] = self.tricks_taken[i] + self.current_round / 10
            self.rewards[agent] = -10 + self.current_round
            self._accumulate_rewards()
            self.illegal_move = True
            return

            # the agent which stepped last had its _cumulative_rewards accounted for
        # (because it was returned by last()), so the _cumulative_rewards for this
        # agent should start again at 0
        # NOT SURE WHAT THIS STEP IS FOR
        # self._cumulative_rewards[agent] = 0

        # stores action of current agent
        self.state[self.agent_selection] = one_hot_action
        self.cards_played[agent] = self.__decode_card(action)
        self.hands[agent].remove(self.__decode_card(action))

        # collect reward if it is the last agent to act per cycle
        if self._agent_selector.is_last():
            # Updates the results of the trick
            winning_agent = self.__choose_winner()
            # Increments the winner's tricks taken
            self.tricks_taken[winning_agent] += 1
            self.tricks_taken[self.partners[winning_agent]] += 1
            # Sets the lead to the winner
            winning_index = self.possible_agents.index(winning_agent)
            self.has_lead = winning_agent
            self.agents = self.possible_agents[winning_index:]
            self.agents.extend(self.possible_agents[:winning_index])
            self._agent_selector.reinit(self.agents)
            # Resets the cards played
            self.cards_played = {i: '' for i in self.agents}

            self.current_round += 1
            # rewards for all agents are placed in the .rewards dictionary if in the final round
            if self.current_round == N_ITERS:
                for i in self.agents:
                    self.rewards[i] = self.tricks_taken[i]

                    # The dones dictionary must be updated for all players.
            self.dones = {i: self.current_round >= N_ITERS for i in self.agents}

        # observe the current state
        self.public_info.append(self.cards_played)
        observation_index = self.agent_name_mapping[agent] * N_ITERS + this_round
        self.public_observation[observation_index, action] = 1
        self.private_observations[agent][0, action] = 0
        for i in self.agents:
            self.__update_observation(i)

        for i in self.agents:
            self.__update_action_mask(i)

        # selects the next agent.
        self.agent_selection = self._agent_selector.next()
        # Adds .rewards to ._cumulative_rewards
        self._accumulate_rewards()

    def __encode_card(self, card):
        rank = RANK_LOOKUP[card[:-1]]
        suit = SUIT_LOOKUP[card[-1]] * N_ITERS
        return rank + suit

    def __decode_card(self, code):
        rank = RANK_REVERSE[code % N_ITERS]
        suit = SUIT_REVERSE[code // N_ITERS]
        return rank + suit

    def __deal_cards(self):
        deck = [str(rank) + suit for rank in RANKS for suit in SUITS]
        deck = np.random.permutation(deck)
        for i, agent in enumerate(self.agents):
            hand = list(deck[N_ITERS * i:N_ITERS * (i + 1)])
            self.hands[agent] = hand
            for card in hand:
                self.private_info[agent].append(card)
                self.private_observations[agent][0, self.__encode_card(card)] = 1
        return

    def __update_info(self, agent):
        self.infos[agent] = {'public': self.public_info, 'private': self.private_info[agent]}
        return

    def __update_observation(self, agent):
        self.observations[agent] = {
            'observation': np.append(self.private_observations[agent], self.public_observation, axis=0),
            'action_mask': self.action_masks[agent]}
        return

    def __update_action_mask(self, agent):
        self.action_masks[agent] = self.private_observations[agent].flatten()
        lead = self.cards_played[self.has_lead]
        if lead != '':
            lead_suit = lead[-1]
            hand = self.hands[agent]
            suits = [card[-1] for card in hand]
            if lead_suit in suits:
                for card in hand:
                    if card[-1] != lead_suit:
                        self.action_masks[agent][self.__encode_card(card)] = 0
        self.__update_observation(agent)
        return

    def __choose_winner(self):
        winning_card = self.cards_played[self.has_lead]
        winning_player = self.has_lead
        for player, card in self.cards_played.items():
            if self.__higher_card(winning_card, card):
                winning_card = card
                winning_player = player

        return winning_player

    def __higher_card(self, winning_card, card):
        suit = winning_card[-1]
        rank = RANK_LOOKUP[winning_card[:-1]]
        new_suit = card[-1]
        new_rank = RANK_LOOKUP[card[:-1]]
        if new_suit == suit:
            if new_rank > rank:
                return True
            else:
                return False
        elif new_suit == TRUMP:
            return True
        return False
