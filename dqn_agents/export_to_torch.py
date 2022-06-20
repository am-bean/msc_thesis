from card_game_files.load_pretrained_player import load_pretrained_player

if __name__ == '__main__':
    e, t = load_pretrained_player("C:/Users/Andre/ray_results/DQN/" + 'DQN_cards_4c2f7_00000_0_2022-06-06_17-54-15/checkpoint_009000/checkpoint-9000')
    export_dir = 'C:/Users/Andre/OneDrive/Documents/GitHub/msc_thesis/dqn_agents/'
    print(t.get_weights())
    p = t.get_policy(policy_id='player_0')
    print(p.observation_space)
    print(p.model)
    print(p.get_weights())