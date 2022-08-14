from multiprocessing import current_process

from hash_state import hashState
from get_score import getScore
from get_actions import getActions
from new_state import newState

import time
import queue
import numpy as np
from numba import jit


def do_job(states_to_run):
    try_again = 0
    last_printed = -9999
    # Continue to pull new states from the queue until they are exhausted
    while True:
        # This will raise queue.Empty if the queue is empty
        try:
            state = states_to_run.get_nowait()
        # At the beginning there will only be one item in the queue, so I have a try again so that the 2-n processes
        # don't quit immediately
        except queue.Empty:
            if try_again > 20:
                print('Process ended')
                break
            time.sleep(.1*try_again)
            try_again += 1
        # Otherwise do the task
        else:
            # Seems to be a delay in getting things into the queue
            try_again = 0
            obs, hands, seat, targetSeat, stateDict, randomSeats, childrenDict, parentDict, stateDetailsDict = state
            s = len(parentDict.keys())
            if s - last_printed > 10000:
                print(current_process().name)
                print(s)
                last_printed = s
            h = hashState(obs, hands)

            # If the state has been solved before, don't do it again
            if h in stateDict.keys():
                continue

            hand = hands[seat, :]
            round = 6 - len(np.nonzero(hand)[0])

            # If the game is over, compute the scores from the observation
            if round == 6:
                score = getScore(obs, hands, targetSeat)
                # Save the learned value
                stateDict[h] = score
                # See if parent can be computed now, if so add back to queue
                if h in parentDict.keys():
                    parentHash = parentDict[h]
                    if all(child in stateDict.keys() for child in childrenDict[parentHash]):
                        states_to_run.put(stateDetailsDict[parentHash])
                continue

            # Find all the children and update the parent and children dicts
            actions = getActions(obs, hands, seat)
            nextStates = [newState(obs, hands, action, seat) for action in actions]
            children = [hashState(new_obs, new_hands) for (new_obs, new_hands, _) in nextStates]
            childrenDict[h] = children
            stateDetailsDict[h] = state
            for child in children:
                parentDict[child] = h

            # If the child states are already computed, use them
            if all(child in stateDict.keys() for child in children):
                # Values are computed with respect to the non-random seats
                # If it is a random turn we average since the random is uniform
                if seat in randomSeats:
                    score = np.mean([stateDict[child] for child in children])
                else:
                    score = np.max([stateDict[child] for child in children])
                stateDict[h] = score
                # See if parent can be computed now, if so add back to queue
                if h in parentDict.keys():
                    parentHash = parentDict[h]
                    if all(child in stateDict.keys() for child in childrenDict[parentHash]):
                        states_to_run.put(stateDetailsDict[parentHash])
                continue
            # Otherwise send the child states to the compute queue
            else:
                for new_obs, new_hands, new_seat in nextStates:
                    add_state = (new_obs, new_hands, new_seat, targetSeat, stateDict, randomSeats, childrenDict, parentDict, stateDetailsDict)
                    states_to_run.put(add_state)
    return True