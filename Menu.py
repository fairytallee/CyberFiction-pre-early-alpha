import pygame
from pygame import Surface
import pyautogui
WIN_WIDTH, WIN_HEIGHT = pyautogui.size()[0], pyautogui.size()[1]


def write(screen, text, pos_x, pos_y, color, size):
    font = pygame.font.SysFont('data/qhyts___.ttf', size)
    text = font.render(text, 1, color)
    text_y = pos_y - text.get_height() // 2
    screen.blit(text, (pos_x, text_y))
    return


def create_button(screen, size, color, pos):
    new_button = pygame.Rect(pos[0], pos[1], size[0], size[1])
    pygame.draw.rect(screen, color, new_button, 3)


def blurSurf(surface, amt):
    """
    Blur the given surface by the given 'amount'.  Only values 1 and greater
    are valid.  Value 1 = no blur.
    """
    if amt < 1.0:
        raise ValueError("Arg 'amt' must be greater than 1.0, passed in value is %s"%amt)
    scale = 1.0/float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf


def menu_pause(screen, screenshot):

    half_w = WIN_WIDTH // 2
    pause_text = ["Pause", "Continue", "Quit to menu"]

    blur_surf = Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
    blur_surf.blit(screenshot, (0, 0))
    new_serf = blurSurf(blur_surf, 20)
    screen.blit(new_serf, (0, 0))

    pygame.draw.line(screen, (78, 37, 245), [0, 110], [WIN_WIDTH, 110], 3)

    # image = pygame.image.load('data/pause_gradient.png').convert_alpha()
    # screen.blit(image, (0, 0))

    wasd = pygame.image.load('data/pause/wasd.png').convert_alpha()
    wasd = pygame.transform.scale(wasd, (100, 100))
    screen.blit(wasd, (WIN_WIDTH - 450, WIN_HEIGHT - 100))
    write(screen, '- move', WIN_WIDTH - 330, WIN_HEIGHT - 50, (255, 255, 255), 50)

    shoot = pygame.image.load('data/pause/лкм.png').convert_alpha()
    shoot = pygame.transform.scale(shoot, (110, 80))
    screen.blit(shoot, (WIN_WIDTH - 230, WIN_HEIGHT - 100))
    write(screen, '- shoot', WIN_WIDTH - 130, WIN_HEIGHT - 50, (255, 255, 255), 50)

    pos_x = 30

    create_button(screen, (250, 50), (78, 37, 245), (pos_x, 30))
    write(screen, pause_text[2], 43, 55, (255, 255, 255), 50)

    pos_x += 260

    create_button(screen, (200, 50), (78, 37, 245), (pos_x, 30))
    write(screen, pause_text[1], pos_x + 22, 55, (255, 255, 255), 50)


def main_menu(screen, bg):
    # blur_surf = Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
    # blur_surf.blit(bg, (0, 0))
    # new_serf = blurSurf(blur_surf, 200)
    # screen.blit(new_serf, (0, 0))

    main_serf_width = 500
    main_serf_height = 100

    menu_text = ['New game', 'Load', 'Quit', 'v1.36']

    pos_x = 200
    pos_y = 400
    create_button(screen, (300, 50), (78, 37, 245), (pos_x, pos_y))
    write(screen, menu_text[0], pos_x + 13, pos_y + 27, (78, 37, 245), 50)

    pos_y += 60
    create_button(screen, (300, 50), (78, 37, 245), (pos_x, pos_y))
    write(screen, menu_text[1], pos_x + 13, pos_y + 27, (78, 37, 245), 50)

    pos_y += 60
    create_button(screen, (300, 50), (78, 37, 245), (pos_x, pos_y))
    write(screen, menu_text[2], pos_x + 13, pos_y + 27, (78, 37, 245), 50)

    write(screen, menu_text[3], pos_x + 10, pos_y + 220, (78, 37, 245), 30)