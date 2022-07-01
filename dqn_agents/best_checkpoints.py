


def best_checkpoints(filepath):

    checkpoints = {
        '0_0': filepath + "DQN_cards_ab6b7_00000_0_2022-05-28_07-30-30/checkpoint_001000/checkpoint-1000",
        '4_8': filepath + 'DQN_cards_eb25a_00000_0_2022-06-22_23-09-00\checkpoint_005000\checkpoint-5000',
        '5_8': filepath + 'DQN_cards_c6582_00000_0_2022-06-23_15-50-08\checkpoint_005000\checkpoint-5000',
        '6_8': filepath + 'DQN_cards_660c8_00000_0_2022-06-23_17-56-17\checkpoint_005000\checkpoint-5000',
        '7_8': filepath + 'DQN_cards_d1ddc_00000_0_2022-06-23_21-48-22\checkpoint_005000\checkpoint-5000',
        'l1_0': filepath + 'DQN_cards_d7d8d_00000_0_2022-06-24_19-31-20\checkpoint_040000\checkpoint-40000',
        'l2_0': filepath + 'DQN_cards_4d039_00000_0_2022-06-25_16-34-28\checkpoint_040000\checkpoint-40000',
        'l2_1': filepath + 'DQN_cards_42c48_00000_0_2022-06-25_19-18-49\checkpoint_040000\checkpoint-40000',
        'l2_2': filepath + 'DQN_cards_f2869_00000_0_2022-06-25_21-03-57\checkpoint_040000\checkpoint-40000',
        'l2_3': filepath + 'DQN_cards_3d870_00000_0_2022-06-26_05-55-46\checkpoint_040000\checkpoint-40000',
        'l3_0': filepath + 'DQN_cards_0df60_00000_0_2022-06-26_15-27-06\checkpoint_040000\checkpoint-40000',
        'l3_1': filepath + 'DQN_cards_25fc2_00000_0_2022-06-26_18-48-12\checkpoint_040000\checkpoint-40000',
        'l3_2': filepath + 'DQN_cards_f118d_00000_0_2022-06-26_20-34-06\checkpoint_040000\checkpoint-40000',
        'l3_3': filepath + 'DQN_cards_031c8_00000_0_2022-06-26_22-21-58\checkpoint_040000\checkpoint-40000',
        'l3_4': filepath + 'DQN_cards_67cc8_00000_0_2022-06-27_00-12-10\checkpoint_040000\checkpoint-40000',
        'l4_0': filepath + 'DQN_cards_5aacb_00000_0_2022-06-26_11-45-15\checkpoint_040000\checkpoint-40000',
        'l5_0': filepath + 'DQN_cards_c3fa9_00000_0_2022-06-27_05-36-52\checkpoint_040000\checkpoint-40000',
        'l5_1': filepath + 'DQN_cards_deadc_00000_0_2022-07-01_08-36-15\checkpoint_040000\checkpoint-40000',
        'l6_0': filepath + 'DQN_cards_413d8_00000_0_2022-06-29_19-18-28\checkpoint_040000\checkpoint-40000',
        'l6_1': filepath + 'DQN_cards_94ca4_00000_0_2022-06-30_10-15-35\checkpoint_040000\checkpoint-40000',
        'l7_0': filepath + 'DQN_cards_9ebd9_00000_0_2022-06-26_22-24-14\checkpoint_040000\checkpoint-40000',
        'l8_0': filepath + 'DQN_cards_f2086_00000_0_2022-06-27_04-38-48\checkpoint_040000\checkpoint-40000',

    }

    old_checkpoints = {
        '0_0': filepath + "DQN_cards_ab6b7_00000_0_2022-05-28_07-30-30/checkpoint_001000/checkpoint-1000",
        '1_1': filepath + "DQN_cards_ab6b7_00000_0_2022-05-28_07-30-30/checkpoint_033000/checkpoint-33000",
        '1_2': filepath + 'DQN_cards_4acab_00000_0_2022-05-31_18-29-57/checkpoint_005000/checkpoint-5000',
        '1_3': filepath + 'DQN_cards_4a305_00000_0_2022-05-31_21-14-35/checkpoint_024000/checkpoint-24000',
        '2_1': filepath + 'DQN_cards_4ce35_00000_0_2022-06-06_09-04-33/checkpoint_004000/checkpoint-4000',
        '2_2': filepath + 'DQN_cards_113e1_00000_0_2022-06-06_13-13-26/checkpoint_009000/checkpoint-9000',
        '2_3': filepath + 'DQN_cards_6a527_00000_0_2022-06-06_13-51-42/checkpoint_009000/checkpoint-9000',
        '3_1': filepath + 'DQN_cards_b8c46_00000_0_2022-06-06_17-14-20/checkpoint_004000/checkpoint-4000',
        '3_2': filepath + 'DQN_cards_4c2f7_00000_0_2022-06-06_17-54-15/checkpoint_009000/checkpoint-9000',
        '4_1': filepath + 'DQN_cards_5ed71_00000_0_2022-06-22_18-47-23/checkpoint_004000/checkpoint-4000',
        '4_2': filepath + 'DQN_cards_2b0c0_00000_0_2022-06-22_19-21-43\checkpoint_005000\checkpoint-5000',
        '4_3': filepath + 'DQN_cards_a4d3f_00000_0_2022-06-22_19-46-36\checkpoint_005000\checkpoint-5000',
        '4_4': filepath + 'DQN_cards_a196e_00000_0_2022-06-22_20-07-59\checkpoint_005000\checkpoint-5000',
        '4_5': filepath + 'DQN_cards_e0bf8_00000_0_2022-06-22_20-38-23\checkpoint_005000\checkpoint-5000',
        '4_6': filepath + 'DQN_cards_1106b_00000_0_2022-06-22_20-54-03\checkpoint_005000\checkpoint-5000',
        '4_7': filepath + 'DQN_cards_18304_00000_0_2022-06-22_21-58-40\checkpoint_005000\checkpoint-5000',
        '4_8': filepath + 'DQN_cards_eb25a_00000_0_2022-06-22_23-09-00\checkpoint_005000\checkpoint-5000',
        '5_1': filepath + 'DQN_cards_95c18_00000_0_2022-06-23_14-01-24\checkpoint_005000\checkpoint-5000',
        '5_2': filepath + 'DQN_cards_0407d_00000_0_2022-06-23_14-18-48\checkpoint_005000\checkpoint-5000',
        '5_3': filepath + 'DQN_cards_26771_00000_0_2022-06-23_14-34-04\checkpoint_005000\checkpoint-5000',
        '5_4': filepath + 'DQN_cards_2e54e_00000_0_2022-06-23_14-48-37\checkpoint_005000\checkpoint-5000',
        '5_5': filepath + 'DQN_cards_2daef_00000_0_2022-06-23_15-02-54\checkpoint_005000\checkpoint-5000',
        '5_6': filepath + 'DQN_cards_b49bf_00000_0_2022-06-23_15-21-00\checkpoint_005000\checkpoint-5000',
        '5_7': filepath + 'DQN_cards_c3c20_00000_0_2022-06-23_15-35-44\checkpoint_005000\checkpoint-5000',
        '5_8': filepath + 'DQN_cards_c6582_00000_0_2022-06-23_15-50-08\checkpoint_005000\checkpoint-5000',
        '6_1': filepath + 'DQN_cards_fba8f_00000_0_2022-06-23_16-05-56\checkpoint_005000\checkpoint-5000',
        '6_2': filepath + 'DQN_cards_3e28e_00000_0_2022-06-23_16-22-07\checkpoint_005000\checkpoint-5000',
        '6_3': filepath + 'DQN_cards_406d6_00000_0_2022-06-23_16-36-29\checkpoint_005000\checkpoint-5000',
        '6_4': filepath + 'DQN_cards_59f39_00000_0_2022-06-23_16-51-31\checkpoint_005000\checkpoint-5000',
        '6_5': filepath + 'DQN_cards_c2f53_00000_0_2022-06-23_17-08-46\checkpoint_005000\checkpoint-5000',
        '6_6': filepath + 'DQN_cards_3df0c_00000_0_2022-06-23_17-26-32\checkpoint_005000\checkpoint-5000',
        '6_7': filepath + 'DQN_cards_6dab2_00000_0_2022-06-23_17-42-11\checkpoint_005000\checkpoint-5000',
        '6_8': filepath + 'DQN_cards_660c8_00000_0_2022-06-23_17-56-17\checkpoint_005000\checkpoint-5000',
        '7_1': filepath + 'DQN_cards_8de30_00000_0_2022-06-23_20-06-15\checkpoint_005000\checkpoint-5000',
        '7_2': filepath + 'DQN_cards_58ad2_00000_0_2022-06-23_20-19-04\checkpoint_005000\checkpoint-5000',
        '7_3': filepath + 'DQN_cards_5a589_00000_0_2022-06-23_20-33-26\checkpoint_005000\checkpoint-5000',
        '7_4': filepath + 'DQN_cards_8d536_00000_0_2022-06-23_20-49-11\checkpoint_005000\checkpoint-5000',
        '7_5': filepath + 'DQN_cards_b149a_00000_0_2022-06-23_21-04-30\checkpoint_005000\checkpoint-5000',
        '7_6': filepath + 'DQN_cards_adcf5_00000_0_2022-06-23_21-18-43\checkpoint_005000\checkpoint-5000',
        '7_7': filepath + 'DQN_cards_b46d2_00000_0_2022-06-23_21-33-13\checkpoint_005000\checkpoint-5000',
        '7_8': filepath + 'DQN_cards_d1ddc_00000_0_2022-06-23_21-48-22\checkpoint_005000\checkpoint-5000',
        '8_1': filepath + 'DQN_cards_711e8_00000_0_2022-06-23_22-07-08\checkpoint_005000\checkpoint-5000',
        '8_2': filepath + 'DQN_cards_190cf_00000_0_2022-06-23_22-26-09\checkpoint_005000\checkpoint-5000',
        '8_3': filepath + 'DQN_cards_119e6_00000_0_2022-06-23_22-40-15\checkpoint_005000\checkpoint-5000',
        '8_4': filepath + 'DQN_cards_0f26a_00000_0_2022-06-23_22-54-30\checkpoint_005000\checkpoint-5000',
        '8_5': filepath + 'DQN_cards_810f9_00000_0_2022-06-24_00-16-26\checkpoint_005000\checkpoint-5000',
        'pool_1': filepath + 'DQN_cards_1fe21_00000_0_2022-06-24_17-10-11\checkpoint_001000\checkpoint-1000',
    }
    return checkpoints
