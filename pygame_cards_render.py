# Import the pygame module
import pygame
from pygame_render_helpers import show_title, show_scores, show_curec
from pygame_constants import *
from Card import Card

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


if __name__ == '__main__':


    # Define a player to hold info about displaying each player
    class Player:
        def __init__(self, name, hand_x, hand_y, played_x, played_y, is_vertical=False):
            self.name = name
            self.hand_x = hand_x
            self.hand_y = hand_y
            self.played_x = played_x
            self.played_y = played_y
            self.hand_cards = []
            self.hand_sprites = pygame.sprite.Group()
            self.is_vertical = is_vertical
            self.played_sprites = pygame.sprite.Group()


        def add_cards(self, sprites):
            for card in sprites:
                self.hand_sprites.add(card)

        def hide_cards(self):
            for card in self.hand_sprites:
                card.update_card(False)

        def show_cards(self):
            for card in self.hand_sprites:
                card.update_card(True)

        def play_card(self, card):
            self.played_sprites.add(card)
            self.hand_sprites.remove(card)
            card.update_card(True)




    # Initialize pygame
    pygame.init()

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

    # Instantiate a card
    players['south'].hand_cards = [Card('spades', 'ace'), Card('hearts', 'jack'), Card('spades', 'king')]
    players['north'].hand_cards = [Card('spades', '10'), Card('spades', '5'), Card('spades', '4')]
    players['east'].hand_cards = [Card('spades', '9'), Card('diamonds', '5'), Card('diamonds', '10')]
    players['west'].hand_cards = [Card('spades', 'queen'), Card('clubs', '5'), Card('clubs', '4')]

    for key, player in players.items():
        player.add_cards(player.hand_cards)
        if key != 'south':
            player.hide_cards()
            player.play_card(player.hand_cards[0])

    # Variable to keep the main loop running
    running = True

    # Main loop
    while running:
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

        scores = {'E/W': 1, 'N/S': 1}

        # Fill the screen with green
        screen.fill((0, 51, 8))

        show_curec(screen, screen_rect)
        show_title(screen, screen_rect)
        show_scores(screen, screen_rect, scores)

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

        # Update the display
        pygame.display.flip()
