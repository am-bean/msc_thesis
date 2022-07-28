from card_game_files.load_pretrained_player import load_pretrained_player
from best_checkpoints import best_checkpoints
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("--checkpoints-folder", type=str, default='../data/checkpoints/')
parser.add_argument('--checkpoint', type=str, default='0_0')
parser.add_argument('--out-folder', type=str, default='../data/models')

if __name__ == '__main__':
    """Exports the policy from the trained agent specified by the args as an ONNX file in the desired folder"""

    args = parser.parse_args()

    e, t = load_pretrained_player(args.checkpoints_folder + best_checkpoints(args.checkpoints_folder)[args.checkpoint])
    p = t.get_policy(policy_id='player_0')
    p.export_model(export_dir=args.out_folder, onnx=12)