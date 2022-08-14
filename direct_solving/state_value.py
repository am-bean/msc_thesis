from hash_state import hashState
from get_score import getScore
from get_actions import getActions
from new_state import newState

import numpy as np
from numba import jit


@jit
def stateValue(obs, hands, seat, targetSeat, stateDict, randomSeats):
    h = hashState(obs, hands)
    # Don't compute the same state twice
    if h in stateDict.keys():
        return stateDict[h]

    hand = hands[seat, :]
    round = 6 - len(np.nonzero(hand)[0])
    # If the game is over, compute the scores from the observation
    if round == 6:
        score = getScore(obs, hands, targetSeat)

    # Otherwise compute the scores by recursion
    else:
        actions = getActions(obs, hands, seat)
        nextStates = [newState(obs, hands, action, seat) for action in actions]
        # Values are computed with respect to the non-random seats
        # If it is a random turn we average since the random is uniform
        if seat in randomSeats:
            score = np.mean([stateValue(new_obs, new_hands, new_seat, targetSeat, stateDict, randomSeats) for
                             (new_obs, new_hands, new_seat) in nextStates])
        else:
            score = max([stateValue(new_obs, new_hands, new_seat, targetSeat, stateDict, randomSeats) for
                         (new_obs, new_hands, new_seat) in nextStates])

    # Save the learned value and then return it
    stateDict[h] = score
    return score
