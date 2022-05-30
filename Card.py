import pygame
from pygame_constants import *


# Define a card object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'card'
class Card(pygame.sprite.Sprite):
    def __init__(self, suit, rank, show_front=True):
        super(Card, self).__init__()

        self.surf = None
        self.show_front = None
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