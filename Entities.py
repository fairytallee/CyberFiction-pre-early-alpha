import pygame
from pygame import *
import math
from Animations import AnimatedSprite
import pyautogui
import os
import pyganim


# WIN_WIDTH, WIN_HEIGHT = 700, 700
# WIN_WIDTH, WIN_HEIGHT = 1920, 1080
WIN_WIDTH, WIN_HEIGHT = pyautogui.size()[0], pyautogui.size()[1]

JUMP_POWER = 10
GRAVITY = 0.35  # Сила, которая будет тянуть нас вниз

HERO_MOVE_SPEED = 7
HERO_WIDTH = 80
HERO_HEIGHT = 80
HERO_HP = 100

BULLET_SIZE = 10
BULLET_SPEED = 20
BULLET_DAMAGE = 10

COLOR = "white"

ANIMATION_DELAY = 100 # скорость смены кадров
ANIMATION_RIGHT = ['data/animations/hero/run1.png', 'data/animations/hero/run2.png', 'data/animations/hero/run3.png',
                   'data/animations/hero/run4.png', 'data/animations/hero/run5.png', 'data/animations/hero/run6.png']

ANIMATION_LEFT = ['data/animations/hero/run_l1.png', 'data/animations/hero/run_l2.png',
                  'data/animations/hero/run_l3.png', 'data/animations/hero/run_l4.png',
                  'data/animations/hero/run_l5.png', 'data/animations/hero/run_l6.png']

ANIMATION_JUMP_LEFT = [('data/animations/hero/run_l2.png', 100)]
ANIMATION_JUMP_RIGHT = [('data/animations/hero/run2.png', 100)]
ANIMATION_JUMP = [('data/animations/hero/run2.png', 100)]
ANIMATION_STAY = [('data/animations/hero/run1.png', 100)]


class Bullet(sprite.Sprite):
    def __init__(self, x, y, speedx, speedy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((BULLET_SIZE, BULLET_SIZE))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.x0 = x
        self.y0 = y
        self.rect.x = x
        self.rect.y = y
        self.speedx = speedx
        self.speedy = speedy
        self.damage = BULLET_DAMAGE

        self.kill_distance = 2000

    def collide(self, platforms, enemies_group):
        for p in platforms:
            if sprite.collide_rect(self, p):
                self.kill()
        for en in enemies_group:
            if sprite.collide_rect(self, en):
                en.heals_points -= self.damage
                en.agr = True
                self.kill()

    def update_bullet(self, platforms, enemies_group):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy

        self.collide(platforms, enemies_group)

        if self.rect.x - self.x0 > self.kill_distance or self.x0 - self.rect.x > self.kill_distance \
                or self.rect.y - self.y0 > self.kill_distance or self.y0 - self.rect.y > self.kill_distance:
            self.kill()


def find_speed(pos_mouse_x, pos_mouse_y):

    x = WIN_WIDTH // 2
    y = WIN_HEIGHT // 2 + 20

    angel = math.radians(abs(math.degrees(math.atan2(abs(pos_mouse_x - x), abs(y - pos_mouse_y))) - 90))

    print(f"hero x: {x} y: {y}")
    print(f'angel: {math.degrees(angel)} degrees')
    print(f"mouse: x: {pos_mouse_x} y: {pos_mouse_y}")
    print()

    speed_x, speed_y = 0, 0

    if x < pos_mouse_x and y > pos_mouse_y:
        speed_x = math.cos(angel) * BULLET_SPEED
        speed_y = -(math.sin(angel)) * BULLET_SPEED
    elif x > pos_mouse_x and y > pos_mouse_y:
        speed_x = -(math.cos(angel) * BULLET_SPEED)
        speed_y = -(math.sin(angel) * BULLET_SPEED)
    elif x > pos_mouse_x and y < pos_mouse_y:
        speed_x = -(math.cos(angel) * BULLET_SPEED)
        speed_y = math.sin(angel) * BULLET_SPEED
    elif x < pos_mouse_x and y < pos_mouse_y:
        speed_x = math.cos(angel) * BULLET_SPEED
        speed_y = math.sin(angel) * BULLET_SPEED
    elif x == pos_mouse_x:
        speed_x = 0
        if y > pos_mouse_y:
            speed_y = -BULLET_SPEED
        elif y < pos_mouse_y:
            speed_y = BULLET_SPEED
        else:
            speed_y = BULLET_SPEED
    elif y == pos_mouse_y:
        speed_y = 0
        if x > pos_mouse_x:
            speed_x = -BULLET_SPEED
        elif x < pos_mouse_x:
            speed_x = BULLET_SPEED
        else:
            speed_x = 0
            speed_y = BULLET_SPEED

    return speed_x, speed_y


def load_image(name, colorkey=None):
    fullname = os.path.join('data/', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удается загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


class Player(sprite.Sprite):
    def __init__(self, x, y, all_sprites):
        sprite.Sprite.__init__(self)

        self.onGround = False  # На земле ли я?

        self.heals_points = HERO_HP

        self.yvel = 0  # скорость вертикального перемещения
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте

        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y

        self.image = Surface((HERO_WIDTH, HERO_HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, HERO_WIDTH, HERO_HEIGHT)
        self.pos = (self.rect.x, self.rect.y)

        self.bullet_speed = BULLET_SPEED

        self.image.set_colorkey('#888888')  # делаем фон прозрачным
        #        Анимация движения вправо
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        #        Анимация движения влево
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))

        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))  # По-умолчанию, стоим

        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()

    def update(self, left, right, up, platforms, screen, extra_speed=0):
        hp_width = 600
        hp_height = 15

        hp_y = -5

        green = (36, 255, 72)
        yellow = (255, 227, 46)
        orange = (255, 122, 20)
        red = (255, 64, 64)
        cur_color = None

        cur_width = self.heals_points / 100 * hp_width
        percent = cur_width / hp_width * 100
        if percent >= 75.0:
            cur_color = green
        elif 45.0 <= percent < 75.0:
            cur_color = yellow
        elif 20.0 <= percent < 45.0:
            cur_color = orange
        elif percent < 20.0:
            cur_color = red

        hp = pygame.Rect(WIN_WIDTH // 2 - hp_width // 2, hp_y, cur_width, hp_height)
        pygame.draw.rect(screen, cur_color, hp)

        # hp_line = pygame.Rect(WIN_WIDTH // 2 - hp_width // 2, hp_y, hp_width, hp_height)
        # pygame.draw.rect(screen, cur_color, hp_line, 1, 0, 0, 0, 0, 0)

        if left:
            start = pygame.time.Clock()
            if pygame.time.get_ticks() - start.get_time() < 5000:
                self.xvel = -HERO_MOVE_SPEED - extra_speed  # Лево = x- n
            else:
                self.xvel = -HERO_MOVE_SPEED
            self.image.fill('#888888')
            if up:  # для прыжка влево есть отдельная анимация
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))

        if right:
            start = pygame.time.Clock()
            if pygame.time.get_ticks() - start.get_time() < 5000:
                self.xvel = HERO_MOVE_SPEED + extra_speed  # Лево = x- n
            else:
                self.xvel = HERO_MOVE_SPEED
            self.image.fill('#888888')
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
            if not up:
                self.image.fill('#888888')
                self.boltAnimStay.blit(self.image, (0, 0))

        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

        if self.heals_points <= 0:
            pass
            # return False

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает

    def shoot(self, bullets_group, all_sprites, pos_mouse_x, pos_mouse_y):

        speed_x, speed_y = find_speed(pos_mouse_x, pos_mouse_y)

        bullet = Bullet(self.rect.centerx - (BULLET_SIZE // 2),
                        self.rect.centery - (BULLET_SIZE // 2), speed_x, speed_y)
        bullets_group.add(bullet)
        all_sprites.add(bullet)