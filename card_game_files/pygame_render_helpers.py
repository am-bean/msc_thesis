import pygame
from pygame_constants import *


def show_scores(screen, screen_rect, scores):
    # Show the current score
    f_medium = pygame.font.Font(pygame.font.get_default_font(), 16)
    score_title = f_medium.render('Current scores', True, WHITE)
    score_title_rect = score_title.get_rect()
    score_title_rect.top = screen_rect.top + CARD_WIDTH * .5
    score_title_rect.left = screen_rect.left + CARD_WIDTH * .1
    ns_score = f_medium.render(f'N/S: {scores["N/S"]}', True, WHITE)
    ns_score_rect = ns_score.get_rect()
    ns_score_rect.topleft = score_title_rect.bottomleft
    ew_score = f_medium.render(f'E/W: {scores["E/W"]}', True, WHITE)
    ew_score_rect = ew_score.get_rect()
    ew_score_rect.topleft = ns_score_rect.bottomleft
    screen.blit(score_title, score_title_rect)
    screen.blit(ns_score, ns_score_rect)
    screen.blit(ew_score, ew_score_rect)


def show_curec(screen, screen_rect):
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
    logo = pygame.image.load('../card_images/oxford_logo.png').convert_alpha()
    logo = pygame.transform.smoothscale(logo, (CARD_WIDTH, CARD_WIDTH))
    logo_rect = logo.get_rect()
    logo_rect.bottom = r_ethics_rect.top - CARD_WIDTH * .1
    logo_rect.left = r_ethics_rect.left
    screen.blit(r_ethics, r_ethics_rect)
    screen.blit(curec, curec_rect)
    screen.blit(logo, logo_rect)


def show_title(screen, screen_rect):
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


def draw_arrow(screen, screen_rect, direction):
    if direction == 'south':
        tri_base_left = (screen_rect.centerx - CARD_WIDTH / 4, screen_rect.centery - CARD_WIDTH / (4 * 1.7))
        tri_base_right = (screen_rect.centerx + CARD_WIDTH / 4, screen_rect.centery - CARD_WIDTH / (4 * 1.7))
        tri_point = (screen_rect.centerx, screen_rect.centery + CARD_WIDTH / 4)
    elif direction == 'north':
        tri_base_left = (screen_rect.centerx - CARD_WIDTH / 4, screen_rect.centery + CARD_WIDTH / (4 * 1.7))
        tri_base_right = (screen_rect.centerx + CARD_WIDTH / 4, screen_rect.centery + CARD_WIDTH / (4 * 1.7))
        tri_point = (screen_rect.centerx, screen_rect.centery - CARD_WIDTH / 4)
    elif direction == 'east':
        tri_base_left = (screen_rect.centerx - CARD_WIDTH / (4 * 1.7), screen_rect.centery + CARD_WIDTH / 4)
        tri_base_right = (screen_rect.centerx - CARD_WIDTH / (4 * 1.7), screen_rect.centery - CARD_WIDTH / 4)
        tri_point = (screen_rect.centerx + CARD_WIDTH / 4, screen_rect.centery)
    else:
        tri_base_left = (screen_rect.centerx + CARD_WIDTH / (4 * 1.7), screen_rect.centery + CARD_WIDTH / 4)
        tri_base_right = (screen_rect.centerx + CARD_WIDTH / (4 * 1.7), screen_rect.centery - CARD_WIDTH / 4)
        tri_point = (screen_rect.centerx - CARD_WIDTH / 4, screen_rect.centery)
    pygame.draw.polygon(surface=screen, color=BLUE, points=[tri_base_left, tri_base_right, tri_point])
