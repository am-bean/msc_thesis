import gc
import json


def best_checkpoints():

    with open('best_checkpoints.txt', 'r') as f:
        checkpoints = json.loads(f.read())
    f.close()

    return checkpoints


def update_best_checkpoints(file=None, key=None):
    checkpoints = best_checkpoints()

    if file and key:
        checkpoints[key] = file

    with open('best_checkpoints.txt', 'w') as f:
        f.write(json.dumps(checkpoints))


if __name__ == "__main__":
    update_best_checkpoints('DQN_cards_d32cf_00000_0_2022-07-07_10-30-30\checkpoint_070000\checkpoint-70000','l3_7')

