# Import the pygame module
from time import sleep

import pygame
import argparse

import ray
import dqn_agents.best_checkpoints as best_checkpoints
from card_game_files.load_pretrained_player import load_pretrained_player
from pygame_render_helpers import show_title, show_scores, show_curec, draw_arrow
from pygame_constants import *
from Card import Card, parse_string_to_card, decode_card
from Player import Player

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

parser = argparse.ArgumentParser()

parser.add_argument("--checkpoint", type=str, default='0_0')
parser.add_argument("--checkpoints-folder", type=str, default='../data/checkpoints/')


if __name__ == '__main__':
    """This file runs a game with pre-trained agents using Pygame.
    
    args:
    
    checkpoint: str, the identifier of the desired agent in the checkpoints file
    checkpoints-folder: str, the path to the checkpoints folder, if not the expected one"""

    args = parser.parse_args()

    # Initialize pygame
    pygame.init()

    # Initialize pretrained model
    checkpoint = args.checkpoints_folder + best_checkpoints.best_checkpoints(args.checkpoints_folder)[args.checkpoint]
    my_env, trainer = load_pretrained_player(checkpoint)
    obs = my_env.reset()

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen_rect = screen.get_rect()

    players = {'north': Player('North', screen_rect.centerx, screen_rect.top + CARD_HEIGHT * .6,
                               screen_rect.centerx, screen_rect.centery - CARD_HEIGHT * .8),
               'east': Player('East', screen_rect.right - CARD_HEIGHT * .8, screen_rect.centery,
                              screen_rect.centerx + CARD_WIDTH * 1.2, screen_rect.centery, True),
               'south': Player('South', screen_rect.centerx, screen_rect.bottom - CARD_HEIGHT * .6,
                               screen_rect.centerx, screen_rect.centery + CARD_HEIGHT * .8),
               'west': Player('West', screen_rect.left + CARD_HEIGHT * .5, screen_rect.centery,
                              screen_rect.centerx - CARD_WIDTH * 1.2, screen_rect.centery, True)
               }

    hands = my_env.get_sub_environments.hands
    player_agent_mapping = {'player_0': 'south', 'player_1': 'west', 'player_2': 'north', 'player_3': 'east'}
    # Create hands from observations
    for agent, player in player_agent_mapping.items():
        players[player].hand_cards = [parse_string_to_card(string, True) for string in hands[agent]]
        players[player].hand_cards.sort(key=lambda card: card.card_to_index())

    for key, player in players.items():
        player.add_cards(player.hand_cards)
        if key != 'south':
            player.hide_cards()

    tricks = my_env.get_sub_environments.tricks_taken
    scores = {'E/W': tricks['player_1'], 'N/S': tricks['player_0']}

    # Variable to keep the main loop running
    running = True
    action_ready = False
    clear_table = False

    # Main loop
    while running:

        current_agent = list(obs.keys())[0]
        current_player = player_agent_mapping[current_agent]

        # Fill the screen with green
        screen.fill((0, 51, 8))

        if current_player != 'south' and not action_ready:
            sleep(1)
            action = trainer.compute_single_action(obs[current_agent], policy_id='player_0', explore=False)
            r, s = decode_card(action)
            selected_card = [card for card in players[current_player].hand_cards if card.suit == s and card.rank == r][0]
            action_ready = True

        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    running = False
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked_sprites = [s for s in players['south'].hand_sprites if s.rect.collidepoint(pos)]
                # The cards are rendered left to right, so the last one in the list will be on top
                if clicked_sprites:
                    # Need to deal with illegal actions
                    action_mask = obs[current_agent]['action_mask']
                    selected_card = clicked_sprites[-1]
                    action = selected_card.card_to_index()
                    if action_mask[action] == 1:
                        action_ready = True

        if clear_table:
            sleep(2)
            clear_table = False
            for player in players.values():
                player.played_sprites.empty()

        if action_ready:
            action_ready = False
            action_dict = {current_agent: action}
            players[current_player].play_card(selected_card)
            obs, reward, dones, info = my_env.step(action_dict)
            running = not dones['__all__']
            tricks = my_env.get_sub_environments.tricks_taken
            scores = {'E/W': tricks['player_1'], 'N/S': tricks['player_0']}
            table = my_env.get_sub_environments.cards_played
            if table == {'player_0': '', 'player_1': '', 'player_2': '', 'player_3': ''}:
                clear_table = True


        for player in players.values():
            # Draw cards in hand

            hand_size = len(player.hand_sprites.sprites())
            if hand_size < 3:
                # Don't overlap the cards if you can avoid it
                overlap_scaling = 1.1
            else:
                overlap_scaling = .5
            if hand_size > 0:
                for i, card in enumerate(player.hand_sprites):
                    if not player.is_vertical:
                        card.rect.centerx = player.hand_x + (i - (hand_size-1)/2) * CARD_WIDTH * overlap_scaling
                        card.rect.centery = player.hand_y
                    else:
                        if card.surf.get_height() > card.surf.get_width():
                            card.surf = pygame.transform.rotate(card.surf, 90)
                        card.rect.centerx = player.hand_x
                        card.rect.centery = player.hand_y + (i - (hand_size-1)/2) * CARD_WIDTH * overlap_scaling
                    screen.blit(card.surf, card.rect)

            # Draw the cards in play
            if len(player.played_sprites) > 0:
                for card in player.played_sprites:
                    card.rect.centerx = player.played_x
                    card.rect.centery = player.played_y
                    screen.blit(card.surf, card.rect)


        current_agent = list(obs.keys())[0]
        current_player = player_agent_mapping[current_agent]

        show_curec(screen, screen_rect)
        show_title(screen, screen_rect)
        show_scores(screen, screen_rect, scores)
        draw_arrow(screen, screen_rect, current_player)

        # Update the display
        pygame.display.flip()

    # Clean up once the game is over
    ray.shutdown()
