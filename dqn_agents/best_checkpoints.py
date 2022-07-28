import gc
import json


def best_checkpoints(filepath=''):

    with open(filepath + 'best_checkpoints.txt', 'r') as f:
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
    update_best_checkpoints('DQN_cards_b2121_00000_0_2022-07-08_20-29-41\checkpoint_040000\checkpoint-40000','rb4_4')

