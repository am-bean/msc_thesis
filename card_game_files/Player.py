import pygame


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