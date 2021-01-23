import pygame


def write(screen, text, pos_x, pos_y, color, size):
    font = pygame.font.SysFont('data/qhyts___.ttf', size)
    text = font.render(text, 1, color)
    text_y = pos_y - text.get_height() // 2
    screen.blit(text, (pos_x, text_y))
    return


def create_button(screen, size, color, pos):
    new_button = pygame.Surface((size[0], size[1]))
    new_button.fill((color))
    screen.blit(new_button, (pos[0], pos[1]))


def menu_pause(screen):

    image = pygame.image.load('data/pause_gradient.png').convert_alpha()
    screen.blit(image, (700, 200))

    pause_text = ["Pause", "Continue", "Quit"]
    write(screen, pause_text[0], 860, 260, (249, 209, 72), 100)
    create_button(screen, (200, 100), (249, 209, 42), (860, 600))
    write(screen, pause_text[1], 880, 650, (0, 0, 0), 50)
    create_button(screen, (100, 50), (206,48,39), (910, 725))
    write(screen, pause_text[2], 940, 750, (0, 0, 0), 25)