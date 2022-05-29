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

        # Fill the screen with green
        screen.fill((0, 51, 8))

        # Place the logo and CUREC in the corner
        f = pygame.font.Font(pygame.font.get_default_font(), 12)
        curec = f.render('SSH_OII_CIA_22_054', True, WHITE)
        curec_rect = curec.get_rect()
        curec_rect.right = screen_rect.right - CARD_WIDTH * .1
        curec_rect.bottom = screen_rect.bottom - CARD_WIDTH * .1
        r_ethics = f.render('Ethics Approval:', True, WHITE)
        r_ethics_rect = r_ethics.get_rect()
        r_ethics_rect.left = curec_rect.left
        r_ethics_rect.bottom = curec_rect.top
        logo = pygame.image.load('card_images/oxford_logo.png').convert_alpha()
        logo = pygame.transform.smoothscale(logo, (CARD_WIDTH, CARD_WIDTH))
        logo_rect = logo.get_rect()
        logo_rect.bottom = r_ethics_rect.top - CARD_WIDTH * .1
        logo_rect.left = r_ethics_rect.left
        screen.blit(r_ethics, r_ethics_rect)
        screen.blit(curec, curec_rect)
        screen.blit(logo, logo_rect)

        # Add the title
        f_large = pygame.font.Font(pygame.font.get_default_font(), 24)
        f_medium = pygame.font.Font(pygame.font.get_default_font(), 16)
        title = f_large.render('AI Easy-Spades', True, WHITE)
        title_rect = title.get_rect()
        title_rect.left = screen_rect.left + CARD_WIDTH * .1
        title_rect.top = screen_rect.top + CARD_WIDTH * .1
        instruc3 = f_medium.render('Spades are trump and beat other suits', True, WHITE)
        instruc3_rect = instruc3.get_rect()
        instruc3_rect.bottom = screen_rect.bottom - CARD_WIDTH * .1
        instruc3_rect.left = screen_rect.left + CARD_WIDTH * .1
        instruc2 = f_medium.render('You must follow suit if you can', True, WHITE)
        instruc2_rect = instruc2.get_rect()
        instruc2_rect.bottomleft = instruc3_rect.topleft
        instruc = f_medium.render('Win as many tricks as you can with your partner', True, WHITE)
        instruc_rect = instruc.get_rect()
        instruc_rect.bottomleft = instruc2_rect.topleft
        screen.blit(title, title_rect)
        screen.blit(instruc, instruc_rect)
        screen.blit(instruc2, instruc2_rect)
        screen.blit(instruc3, instruc3_rect)

        # Show the current score
        score_title = f_medium.render('Current scores', True, WHITE)
        score_title_rect = score_title.get_rect()
        score_title_rect.top = title_rect.bottom + CARD_WIDTH * .2
        score_title_rect.left = title_rect.left
        ns_score = f_medium.render(f'N/S: {1}', True, WHITE)
        ns_score_rect = ns_score.get_rect()
        ns_score_rect.topleft = score_title_rect.bottomleft
        ew_score = f_medium.render(f'E/W: {1}', True, WHITE)
        ew_score_rect = ew_score.get_rect()
        ew_score_rect.topleft = ns_score_rect.bottomleft
        screen.blit(score_title, score_title_rect)
        screen.blit(ns_score, ns_score_rect)
        screen.blit(ew_score, ew_score_rect)


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
