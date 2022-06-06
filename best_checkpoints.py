

def best_checkpoints():
    filepath = "C:/Users/Andre/ray_results/DQN/"
    checkpoints = {
        'first_round': filepath + "DQN_cards_ab6b7_00000_0_2022-05-28_07-30-30/checkpoint_033000/checkpoint-33000",
        'untrained': filepath + "DQN_cards_ab6b7_00000_0_2022-05-28_07-30-30/checkpoint_001000/checkpoint-1000",
        'second_round': filepath + 'DQN_cards_4acab_00000_0_2022-05-31_18-29-57/checkpoint_005000/checkpoint-5000',
        'third_round': filepath + 'DQN_cards_4a305_00000_0_2022-05-31_21-14-35/checkpoint_024000/checkpoint-24000',
        '2_1': filepath + 'DQN_cards_4ce35_00000_0_2022-06-06_09-04-33/checkpoint_004000/checkpoint-4000'}

    return checkpoints
