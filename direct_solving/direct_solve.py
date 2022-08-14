from multiprocessing import Lock, Process, Queue, Manager, current_process
import time
import queue # imported for using queue.Empty exception
import numpy as np
from numba import jit
import argparse

from create_nearly_solved_initial_state import customInitialState
from state_value import do_job
from create_random_state import createRandomInitialState
from hash_state import hashState

parser = argparse.ArgumentParser()

parser.add_argument("--num-procs", type=int, default=1)

if __name__ == '__main__':

    args = parser.parse_args()

    number_of_processes = args.num_procs

    states_to_run = Queue()
    processes = []
    manager = Manager()

    obs, hands = createRandomInitialState(0)
    seat = 0
    targetSeat = 0
    randomSeats = [1, 3]
    h = hashState(obs, hands)
    stateDict = manager.dict()
    stateDetailsDict = manager.dict()
    childrenDict = manager.dict()
    parentDict = manager.dict()
    states_to_run.put((obs, hands, seat, targetSeat, stateDict, randomSeats, childrenDict, parentDict, stateDetailsDict))

    # creating processes
    for w in range(number_of_processes):
        p = Process(target=do_job, args=(states_to_run,))
        processes.append(p)
        p.start()

    # completing process
    for p in processes:
        p.join()

    print(stateDict[h])
    print(len(stateDict.keys()))
