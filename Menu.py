import pygame
from pygame import Surface
import pyautogui
width, height = pyautogui.size()[0], pyautogui.size()[1]


def write(screen, text, pos_x, pos_y, color, size):
    font = pygame.font.SysFont('data/qhyts___.ttf', size)
    text = font.render(text, 1, color)
    text_y = pos_y - text.get_height() // 2
    screen.blit(text, (pos_x, text_y))
    return


def create_button(screen, size, color, pos):
    new_button = pygame.Rect(pos[0], pos[1], size[0], size[1])
    pygame.draw.rect(screen, color, new_button, 3, 0, 20, 0, 0, 20)


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
    global width, height

    half_w = width // 2
    pause_text = ["Pause", "Continue", "Quit"]

    blur_surf = Surface((width, height - 110), pygame.SRCALPHA)
    blur_surf.blit(screenshot, (0, -110))
    new_serf = blurSurf(blur_surf, 20)
    screen.blit(new_serf, (0, 110))

    pygame.draw.line(screen, (206, 48, 39), [0, 110], [width, 110], 3)

    # image = pygame.image.load('data/pause_gradient.png').convert_alpha()
    # screen.blit(image, (0, 0))

    wasd = pygame.image.load('data/wasd.png').convert_alpha()
    wasd = pygame.transform.scale(wasd, (100, 100))
    screen.blit(wasd, (width - 450, height - 100))
    write(screen, '- move', width - 330, height - 50, (255, 255, 255), 50)

    shoot = pygame.image.load('data/лкм.png').convert_alpha()
    shoot = pygame.transform.scale(shoot, (110, 80))
    screen.blit(shoot, (width - 230, height - 100))
    write(screen, '- shoot', width - 130, height - 50, (255, 255, 255), 50)

    write(screen, pause_text[0], width // 2 - 100, 55, (255, 255, 255), 100)

    create_button(screen, (200, 50), (206, 48, 39), (160, 30))
    write(screen, pause_text[1], 182, 55, (255, 255, 255), 50)

    create_button(screen, (100, 50), (206, 48, 39), (30, 30))
    write(screen, pause_text[2], 43, 55, (255, 255, 255), 50)