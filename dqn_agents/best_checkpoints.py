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
