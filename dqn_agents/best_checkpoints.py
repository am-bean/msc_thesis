import json


def best_checkpoints():

    with open('best_checkpoints.txt', 'r') as f:
        checkpoints = json.loads(f.read())

    return checkpoints


def update_best_checkpoints(file=None, key=None):
    checkpoints = best_checkpoints()

    if file and key:
        checkpoints[key] = file

    with open('best_checkpoints.txt', 'w') as f:
        f.write(json.dumps(checkpoints))


if __name__ == "__main__":
    update_best_checkpoints('DQN_cards_87808_00000_0_2022-07-01_11-47-05\checkpoint_040000\checkpoint-40000','l7_1')