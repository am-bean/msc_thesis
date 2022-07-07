import numpy as np

from ray.rllib.examples.policy.random_policy import RandomPolicy
from ray.rllib.utils.annotations import override

from dqn_agents import cards_env


class RuleBasedPolicy(RandomPolicy):
    """Hand-coded policy that returns rule-based actions."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        (obs_space, action_space, _) = args

        self.obs_space = obs_space

        self.action_shape = action_space.n

    @override(RandomPolicy)
    def compute_actions(
            self,
            obs_batch,
            state_batches=None,
            prev_action_batch=None,
            prev_reward_batch=None,
            **kwargs
    ):

        def trick_winner(played_this_trick):
            played = list(np.array([np.sign(o.size) for o in played_this_trick]).nonzero()[0])
            lead = played.copy()
            while len(lead) > 1:
                temp = lead.pop(0)
                if ((temp + 3) % 4) not in played:
                    lead.append(temp)
            lead = lead[0]
            winner = lead
            winning_card = played_this_trick[lead][0]
            for i, card in enumerate(played_this_trick):
                if not card.size > 0:
                    continue
                # Same suit
                if (card[0] // 6) == (winning_card // 6):
                    if card[0] > winning_card:
                        winning_card = card[0]
                        winner = i
                # Or spades
                elif (card[0] // 6) == 0:
                    winning_card = card[0]
                    winner = i
            return winner, winning_card

        def identify_current_player(player_obs):
            max_rows = np.array([o.sum(axis=1).nonzero()[0].max(initial=-1) for o in player_obs])
            current_round = max_rows.max()
            possible_current_players = list(
                np.array([1 if m == current_round - 1 else 0 for m in max_rows]).nonzero()[0])
            if len(possible_current_players) > 0:
                current_player = possible_current_players.copy()
                while len(current_player) > 1:
                    temp = current_player.pop(0)
                    if ((temp + 3) % 4) not in possible_current_players:
                        current_player.append(temp)
                current_player = current_player[0]
            else:
                current_player = None
                current_round += 1
            return current_player, current_round

        def identify_lead_player(player_obs):
            max_rows = np.array([o.sum(axis=1).nonzero()[0].max(initial=-1) for o in player_obs])
            current_round = max_rows.max()
            possible_lead_players = list(np.array([1 if m == current_round else 0 for m in max_rows]).nonzero()[0])
            if len(possible_lead_players) < 4:
                lead_player = possible_lead_players.copy()
                while len(lead_player) > 1:
                    temp = lead_player.pop(0)
                    if ((temp + 1) % 4) not in possible_lead_players:
                        lead_player.append(temp)
                lead_player = lead_player[0]
            else:
                lead_player = None
            return lead_player

        def choose_single_action(obs):

            obs = np.reshape(obs, (-1, 24))
            # RLLib appends action mask to observation array
            if obs.shape == (26, 24):
                action_mask = obs[0, :]
                obs = obs[1:, :]
            legal_actions = action_mask.nonzero()[0] #obs[0, :].nonzero()[0]
            played_cards = obs[1:, :].sum(axis=0).nonzero()[0]
            player_obs = [obs[1:7, :], obs[7:13, :], obs[13:19, :], obs[19:, :]]
            current_player, current_round = identify_current_player(player_obs)
            lead_player = identify_lead_player(player_obs)

            # If there is only one legal move, make it and stop checking rules
            if len(legal_actions) == 1:
                return legal_actions[0]

            # Lead will not be returned if the agent itself has the lead
            if not lead_player:
                # If holding any aces
                if any((legal_actions % 6) == 5):
                    aces = legal_actions[(legal_actions % 6 == 5)]
                    same_suits = [((legal_actions // 6) == (suit // 6)).sum() for suit in aces]
                    # Choose the ace with the least cards beneath it to reduce chance of getting trumped
                    return aces[np.argmin(same_suits)]
                # If no aces, play the non-trump card with the most cards in play under it
                else:
                    undermined_cards = np.array([len(
                        played_cards[np.all([(played_cards < card), ((played_cards // 6) == (card // 6))], axis=0)]) for
                                                 card in legal_actions])
                    self_undermined_cards = np.array([len(
                        legal_actions[np.all([(legal_actions < card), ((legal_actions // 6) == (card // 6))], axis=0)])
                                                      for card in legal_actions])
                    undermined_cards += self_undermined_cards
                    card_values = np.array([card % 6 for card in legal_actions])
                    cards_beneath = card_values - undermined_cards
                    return legal_actions[cards_beneath.argmax()]
            else:
                played_this_trick = [o[current_round, :].nonzero()[0] for o in player_obs]
                winning, winning_card = trick_winner(played_this_trick)
                n_played = sum([o.size > 0 for o in played_this_trick])

            # If all the playable cards are the same suit
            if len(set(legal_actions // 6)) == 1:
                # If that suit is spades
                if (legal_actions // 6)[0] == 0:
                    # If going last play the lowest winning card
                    if n_played == 3:
                        if winning_card // 6 == 0:
                            if len(legal_actions[legal_actions > winning_card]) > 0:
                                return legal_actions[legal_actions > winning_card].min()
                            else:
                                return legal_actions.min()
                        else:
                            return legal_actions.min()
                    # If not last, play the lowest winning card
                    elif winning_card // 6 == 0:
                        if len(legal_actions[legal_actions > winning_card]) > 0:
                            return legal_actions[legal_actions > winning_card].min()
                        else:
                            return legal_actions.min()
                    else:
                        return legal_actions.min()
                else:
                    # If it is possible to win the trick, do so
                    if all((legal_actions // 6) == (winning // 6)):
                        if len(legal_actions[legal_actions > winning_card]) > 0:
                            # If agent is going last, play lowest winning card
                            if n_played == 3:
                                return legal_actions[legal_actions > winning_card].min()
                            # Otherwise play the highest winning card
                            else:
                                return legal_actions.max()
                        # If winning is not possible, play the lowest possible card
                        else:
                            return legal_actions.min()
                    # If following suit is not possible, play the lowest card
                    else:
                        return legal_actions.min()
            # Otherwise, if a trump can be played
            elif 0 in set(legal_actions // 6):
                trumps = legal_actions[legal_actions // 6 == 0]
                # Play the lowest winning trump
                if winning_card // 6 == 0:
                    if len(trumps[trumps > winning_card]) > 0:
                        return trumps[trumps > winning_card].min()
                    else:
                        return legal_actions.min()
                else:
                    return trumps.min()
            # Otherwise play the lowest card that won't win
            else:
                return legal_actions.min()

            # Otherwise no rules apply, so choose at random
            return np.random.choice(legal_actions)

        return np.array([choose_single_action(obs) for obs in obs_batch]), [], {}
