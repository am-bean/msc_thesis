from card_game_files.load_pretrained_player import load_pretrained_player
from best_checkpoints import best_checkpoints

if __name__ == '__main__':
    e, t = load_pretrained_player('C:/Users/Andre/ray_results/DQN/aws/' + best_checkpoints()['fcp'])
    export_dir = 'C:/Users/Andre/OneDrive/Documents/GitHub/msc_thesis/dqn_agents/final_models'
    p = t.get_policy(policy_id='player_0')
    print(p.observation_space)
    p.export_model(export_dir=export_dir, onnx=12)