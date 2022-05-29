# Import the pygame module
import pygame

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

    # Define constants for the screen width and height
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 700

    CARD_WIDTH = SCREEN_WIDTH * .08
    CARD_RATIO = 1.455
    CARD_HEIGHT = CARD_WIDTH * CARD_RATIO
    BORDER_THICKNESS = .97

    BLUE = (0, 33, 71, 255)
    WHITE = (255, 255, 255, 0)
    BLACK = (0, 0, 0, 0)

    # Define a player to hold info about displaying each player
    class Player:
        def __init__(self, name, hand_x, hand_y, is_vertical=False):
            self.name = name
            self.hand_x = hand_x
            self.hand_y = hand_y
            self.hand_cards = []
            self.hand_sprites = pygame.sprite.Group()
            self.is_vertical = is_vertical


        def add_cards(self, sprites):
            for card in sprites:
                self.hand_sprites.add(card)

        def hide_cards(self):
            for card in self.hand_sprites:
                card.update_card(False)

    # Define a card object by extending pygame.sprite.Sprite
    # The surface drawn on the screen is now an attribute of 'card'
    class Card(pygame.sprite.Sprite):
        def __init__(self, suit, rank, show_front=True):
            super(Card, self).__init__()

            frontpath = "card_images/png/" + rank + "_of_" + suit +".png"
            front_img = pygame.image.load(frontpath).convert_alpha()
            front_img = pygame.transform.smoothscale(front_img, (CARD_WIDTH * BORDER_THICKNESS, CARD_HEIGHT * BORDER_THICKNESS))
            self.front = pygame.Surface((CARD_WIDTH * BORDER_THICKNESS, CARD_HEIGHT * BORDER_THICKNESS))
            self.front.fill(WHITE)
            self.front.blit(front_img, self.front.get_rect())

            backpath = "card_images/png/back.png"

            back_img = pygame.image.load(backpath).convert_alpha()
            pygame.transform.threshold(dest_surface=back_img, surface=back_img,
                                       search_color=(0, 0, 0, 0),
                                       threshold=(225, 225, 225, 0),
                                       set_color=BLUE)
            back_img = pygame.transform.smoothscale(back_img, (CARD_WIDTH * BORDER_THICKNESS, CARD_HEIGHT * BORDER_THICKNESS))
            self.back = pygame.Surface((CARD_WIDTH * BORDER_THICKNESS, CARD_HEIGHT * BORDER_THICKNESS))
            self.back.blit(back_img, self.back.get_rect())
            self.update_card(show_front)

        def update_card(self, show_front=True):
            self.show_front = show_front
            self.surf = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
            #self.surf.fill(BLACK)
            surf_rect = self.surf.get_rect()
            back_rect = self.back.get_rect()
            front_rect = self.front.get_rect()
            back_rect.center = surf_rect.center
            front_rect.center = surf_rect.center
            if self.show_front:
                self.surf.blit(self.front, front_rect)
            else:
                self.surf.blit(self.back, back_rect)
            self.rect = self.surf.get_rect()

    # Initialize pygame
    pygame.init()

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen_rect = screen.get_rect()

    players = {'north': Player('North', screen_rect.centerx, screen_rect.top + CARD_HEIGHT * .6),
               'east': Player('East', screen_rect.right - CARD_HEIGHT * .8, screen_rect.centery, True),
               'south': Player('South', screen_rect.centerx, screen_rect.bottom - CARD_HEIGHT * .6),
               'west': Player('West', screen_rect.left + CARD_HEIGHT * .5, screen_rect.centery, True)
               }

    # Instantiate a card
    players['south'].add_cards([Card('hearts', '6'), Card('hearts', '5')])
    players['north'].add_cards([Card('spades', '6'), Card('spades', '5'), Card('spades', '4')])
    players['east'].add_cards([Card('diamonds', '6'), Card('diamonds', '5')])
    players['west'].add_cards([Card('clubs', '6'), Card('clubs', '5'), Card('clubs', '4')])

    players['north'].hide_cards()
    players['east'].hide_cards()
    players['west'].hide_cards()

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

        # Fill the screen with green
        screen.fill((0, 51, 8))

        # Draw cards in hand
        for player in players.values():
            hand_size = len(player.hand_sprites.sprites())
            if hand_size < 3:
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

        # Update the display
        pygame.display.flip()
