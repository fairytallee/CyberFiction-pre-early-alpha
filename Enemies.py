import pygame
from pygame import *
from Entities import Bullet
import math
import random
import pyautogui
import pyganim


# WIN_WIDTH, WIN_HEIGHT = 700, 700
# WIN_WIDTH, WIN_HEIGHT = 1920, 1080
WIN_WIDTH, WIN_HEIGHT = pyautogui.size()[0], pyautogui.size()[1]

JUMP_POWER = 10
GRAVITY = 0.35  # Сила, которая будет тянуть нас вниз

ENEMY_MOVE_SPEED = random.randrange(3, 7)
ENEMY_WIDTH = 80
ENEMY_HEIGHT = 80
ENEMY_HP = 70

COLOR = 'red'

BULLET_SIZE = 10
BULLET_SPEED = 17

ANIMATION_DELAY = 150 # скорость смены кадров
ANIMATION_RIGHT = ['data/animations/hero/run1.png', 'data/animations/hero/run2.png', 'data/animations/hero/run3.png',
                   'data/animations/hero/run4.png', 'data/animations/hero/run5.png', 'data/animations/hero/run6.png']

ANIMATION_LEFT = ['data/animations/hero/run_l1.png', 'data/animations/hero/run_l2.png',
                  'data/animations/hero/run_l3.png', 'data/animations/hero/run_l4.png',
                  'data/animations/hero/run_l5.png', 'data/animations/hero/run_l6.png']

ANIMATION_STAY = [('data/animations/hero/run1.png', 150)]


class EnemyBullet(Bullet):
    def __init__(self, x, y, speedx, speedy, hero):
        super().__init__(x, y, speedx, speedy)
        self.image.fill((255, 0, 0))
        self.hero = hero

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                self.kill()
        if sprite.collide_rect(self, self.hero):
            self.hero.heals_points -= 10
            self.kill()
            print(self.hero.heals_points)

    def update_bullet(self, platforms):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy

        self.collide(platforms)

        if self.rect.x - self.x0 > self.kill_distance or self.x0 - self.rect.x > self.kill_distance \
                or self.rect.y - self.y0 > self.kill_distance or self.y0 - self.rect.y > self.kill_distance:
            self.kill()


def find_enemy_speed(pos_mouse_x, pos_mouse_y, self_pos_x, self_pos_y):
    x = self_pos_x
    y = self_pos_y

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


class Check(sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((BULLET_SIZE, BULLET_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Enemy(sprite.Sprite):
    def __init__(self, x, y, move_speed, bullet_group, all_sprites, hero):
        sprite.Sprite.__init__(self)

        self.agr = False
        self.onGround = False  # На земле ли я?

        self.yvel = 0  # скорость вертикального перемещения
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте

        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y

        self.move_speed = move_speed

        self.image = Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
        self.image.set_colorkey('#888888')
        self.rect = Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.pos = (self.rect.x, self.rect.y)

        self.bullets_group = bullet_group
        self.all_sprites = all_sprites

        self.hero = hero

        self.heals_points = ENEMY_HP

        self.bullet_speed = BULLET_SPEED

        self.shoot_pass = True

        self.hero_near = False

        self.start_timer = 0

        self.left = False
        self.right = False
        self.up = False

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

    def update(self, platforms):

        if self.agr:
            if self.rect.centerx > self.hero.rect.centerx:
                self.left = True
                self.right = False
            elif self.rect.centerx < self.hero.rect.centerx:
                self.right = True
                self.left = False

        if self.heals_points <= 0:
            self.kill()

        if abs(self.rect.centerx - self.hero.rect.centerx) < 900\
                and abs(self.rect.centery - self.hero.rect.centery) < 900:

            if self.left == self.right:
                self.left = random.choice([True, False])
                self.right = random.choice([True, False])
                if self.left == self.right:
                    self.left = False
                    self.right = False

            self.hero_near = True
        else:
            self.left = False
            self.right = False

            self.hero_near = False

        if self.hero_near:
            self.intelligence(self.hero.rect.centerx, self.hero.rect.centery, platforms, self.hero)

        if self.right == self.left:
            self.right = False
            self.left = False
            self.image.fill('#888888')
            self.boltAnimStay.blit(self.image, (0, 0))

        if self.left:
            self.xvel = -self.move_speed # Лево = x- n
            self.image.fill('#888888')
            self.boltAnimLeft.blit(self.image, (0, 0))

        if self.right:
            self.xvel = self.move_speed  # Право = x + n
            self.image.fill('#888888')
            self.boltAnimRight.blit(self.image, (0, 0))

        if not (self.left or self.right):  # стоим, когда нет указаний идти
            self.xvel = 0
            self.image.fill('#888888')
            self.boltAnimStay.blit(self.image, (0, 0))

        if self.up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо
                    self.right = False
                    self.left = True

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево
                    self.left = False
                    self.right = True

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает

    def intelligence(self, hero_pos_x, hero_pos_y, platforms, hero):
        fall_left = True
        fall_right = True
        hero_left = False
        hero_right = False
        hero_here = False

        r = 500
        if (hero_pos_x - self.rect.centerx) ** 2 + (hero_pos_y - self.rect.centery) ** 2 <= r * r:
            self.agr = True
            if pygame.time.get_ticks() - self.start_timer > random.randrange(300, 1200):
                self.shoot(self.bullets_group, self.all_sprites, hero_pos_x, hero_pos_y)
                self.start_timer = pygame.time.get_ticks()
            if self.rect.centerx - hero_pos_x > 10:
                self.right = False
                self.left = True
                hero_left = True
                hero_right = False
            elif self.rect.centerx - hero_pos_x < -10:
                self.right = True
                self.left = False
                hero_right = True
                hero_left = False
            else:
                self.right = False
                self.left = False
                hero_here = True

        for p in platforms:
            checkpoint = Check(self.rect.right, self.rect.bottom + 10)

            if sprite.collide_rect(checkpoint, p):
                fall_right = False

            checkpoint.rect.x = self.rect.left

            if sprite.collide_rect(checkpoint, p):
                fall_left = False

            checkpoint.kill()
        if self.agr and fall_left and hero_left:
            self.right = False
            self.left = False
        elif self.agr and fall_right and hero_right:
            self.right = False
            self.left = False
        elif fall_right and self.agr is False:
            self.right = False
            self.left = True
        elif fall_left and self.agr is False:
            self.right = True
            self.left = False
        elif hero_here:
            self.left = False
            self.right = False
        self.agr = False

    def shoot(self, bullets_group, all_sprites, pos_mouse_x, pos_mouse_y):

        speed_x, speed_y = find_enemy_speed(pos_mouse_x, pos_mouse_y, self.rect.centerx, self.rect.centery)

        bullet = EnemyBullet(self.rect.centerx - (BULLET_SIZE // 2),
                             self.rect.centery - (BULLET_SIZE // 2), speed_x, speed_y, self.hero)
        bullets_group.add(bullet)
        all_sprites.add(bullet)
