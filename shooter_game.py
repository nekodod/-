from pygame import *
from time import time as time_count
from random import randint

init()
mixer.init()
window = display.set_mode((700, 600))
display.set_caption("SpaceShooter")
background = transform.scale(image.load("galaxy.jpg"), (700, 600))
mixer.music.load('space.ogg')
mixer.music.play(loops=-1) # loops=-1 забезпечує зациклення музики
clock = time.Clock()
font.init()  # ініціалізувати модуль шрифтів

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size, player_speed=0):
        super().__init__()
        self.image = transform.scale(image.load(player_image), size)
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def draw_sprite(self):
        window.blit(self.image, self.rect)

start_time = time_count()

class Player(GameSprite):
    def update(self, bullets):
        global start_time
        pressed_keys = key.get_pressed()
        if pressed_keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if pressed_keys[K_d] and self.rect.x < 640:
            self.rect.x += self.speed
        if pressed_keys[K_SPACE] and time_count() - start_time >= 1:
            bullets.add(Bullet('bullet.png', self.rect.x + 25, self.rect.y, (10, 20), 10))
            start_time = time_count()

class Bullet(GameSprite):
    def move(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Enemy(GameSprite):
    def update(self):
        global life, score
        self.rect.y += self.speed
        if self.rect.y > 600:
            life -= 1
            self.kill()
        if sprite.spritecollide(self, bullets, True):
            score += 1
            self.kill()

def draw_label():
    image = font.SysFont("Century Gothic", 20).render("Enemies killed: " + str(score), True, (255, 255, 255))
    window.blit(image, (20, 50))
    image = font.SysFont("Century Gothic", 20).render("Life: " + str(life), True, (255, 255, 255))
    window.blit(image, (20, 20))

rocket = Player('rocket.png', 250, 480, (60, 100), 5)

game = True

bullets = sprite.Group()
enemies_group = sprite.Group()

score = 0
life = 3

while game:
    if len(enemies_group) < 7:
        new_enemy = Enemy('ufo.png', randint(0, 640), -100, (80, 50), 1)
        if not sprite.spritecollide(new_enemy, enemies_group, False):
            enemies_group.add(new_enemy)

    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(background, (0, 0))

    for bullet in bullets:
        bullet.move()
        bullet.draw_sprite()

    rocket.update(bullets)
    rocket.draw_sprite()

    enemies_group.update()
    enemies_group.draw(window)

    draw_label()

    if life <= 0:
        game = False

    display.update()
    clock.tick(60)

quit