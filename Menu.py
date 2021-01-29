import pygame
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


def menu_pause(screen):
    global width, height
    image = pygame.image.load('data/pause_gradient.png').convert_alpha()
    screen.blit(image, (0, 0))

    pause_text = ["Pause", "Continue", "Quit"]
    write(screen, pause_text[0], 760, 260, (255, 255, 255), 200)
    create_button(screen, (200, 50), (206, 48, 39), (width - 320, height - 60))
    write(screen, pause_text[1], width - 300, height - 35, (255, 255, 255), 50)
    create_button(screen, (100, 50), (206, 48, 39), (width - 110, height - 60))
    write(screen, pause_text[2], width - 90, height - 35, (255, 255, 255), 35)