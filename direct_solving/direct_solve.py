from multiprocessing import Lock, Process, Queue, Manager, current_process
import time
import queue # imported for using queue.Empty exception
import numpy as np
from numba import jit

from new_state import newState
from get_score import getScore
from get_actions import getActions
from create_random_state import createRandomInitialState
from hash_state import hashState


def do_job(states_to_run):
    try_again = 0
    last_printed = -999
    # Continue to pull new states from the queue until they are exhausted
    while True:
        # This will raise queue.Empty if the queue is empty
        try:
            state = states_to_run.get_nowait()
        # At the beginning there will only be one item in the queue, so I have a try again so that the 2-n processes
        # don't quit immediately
        except queue.Empty:
            if try_again < 1000:
                print('Process ended')
                break
            time.sleep(.1)
            try_again += 1
        # Otherwise do the task
        else:
            # Seems to be a delay in getting things into the queue
            try_again = 0
            obs, hands, seat, targetSeat, stateDict, randomSeats, childrenDict, parentDict = state
            s = len(parentDict.keys())
            if s - last_printed > 1000:
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
                parent = parentDict[h]
                p_obs, p_hands, p_seat, p_targetSeat, p_stateDict, p_randomSeats, p_childrenDict, p_parentDict = parent
                parentHash = hashState(p_obs, p_hands)
                if all(child in stateDict.keys() for child in childrenDict[parentHash]):
                    states_to_run.put(parent)
                continue

            # Find all the children and update the parent and children dicts
            actions = getActions(obs, hands, seat)
            nextStates = [newState(obs, hands, action, seat) for action in actions]
            children = [hashState(new_obs, new_hands) for (new_obs, new_hands, _) in nextStates]
            childrenDict[h] = children
            for child in children:
                parentDict[child] = state

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
                parent = parentDict[h]
                p_obs, p_hands, p_seat, p_targetSeat, p_stateDict, p_randomSeats, p_childrenDict, p_parentDict = parent
                parentHash = hashState(p_obs, p_hands)
                if all(child in stateDict.keys() for child in childrenDict[parentHash]):
                    states_to_run.put(parent)
                continue
            # Otherwise send the child states to the compute queue
            else:
                for new_obs, new_hands, new_seat in nextStates:
                    add_state = (new_obs, new_hands, new_seat, targetSeat, stateDict, randomSeats, childrenDict, parentDict)
                    states_to_run.put(add_state)
    return True


if __name__ == '__main__':
    number_of_processes = 12
    states_to_run = Queue()
    processes = []
    manager = Manager()

    obs, hands = createRandomInitialState(0)
    seat = 0
    targetSeat = 0
    randomSeats = [1, 3]
    h = hashState(obs, hands)
    stateDict = manager.dict()
    childrenDict = manager.dict()
    parentDict = manager.dict()
    states_to_run.put((obs, hands, seat, targetSeat, stateDict, randomSeats, childrenDict, parentDict))

    # creating processes
    for w in range(number_of_processes):
        p = Process(target=do_job, args=(states_to_run,))
        processes.append(p)
        p.start()

    # completing process
    for p in processes:
        p.join()
