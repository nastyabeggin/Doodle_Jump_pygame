import pygame
import os
import random

pygame.init()
pygame.mixer.init()
running = True
image = pygame.image.load(os.path.join('data', 'textures', 'background.png'))
width = image.get_rect()[2]
height = image.get_rect()[-1]
screen = pygame.display.set_mode((width, height))
x = 0
v = 350  # пикселей в секунду
fps = 100
clock = pygame.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)
red = (207, 37, 5)
green = (0, 106, 2)
yellow = (250, 213, 0)
orange = (255, 134, 0)

platforms = []
camera = 0


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('data', 'textures', 'ground.png'))
        self.image = pygame.transform.scale(self.image, (480, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = height - 50
        self.mask = pygame.mask.from_surface(self.image)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join('data', 'textures', 'platform.png'))
        self.image = pygame.transform.scale(self.image, (100, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # print(self.rect)

    def update(self):
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_1 = pygame.image.load(os.path.join('data', 'heroes', 'doodle.png')) # загружаем изображения
        self.image_2 = pygame.image.load(os.path.join('data', 'heroes', 'doodle_pr.png'))
        self.image = pygame.image.load(os.path.join('data', 'heroes', 'doodle.png'))
        self.mask = pygame.mask.from_surface(self.image)
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.image_1 = pygame.transform.scale(self.image, (80, 80))
        self.image_2 = pygame.transform.scale(self.image_2, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = width // 2 - 40
        self.rect.y = height - 100
        self.direction = 0 # направление дудла (если 1, то зеркально отоброжаем картинку)
        self.jump = False # в прыжке ли дудл
        self.flag = False # флаг, отвечающий за положение дудла по оси y
        self.camera = 0 # положение камеры
        self.k = 0 # число, которое показывает, сколько дудл не соприкасался с платформами
        self.n = 0 # переменная, отвечающая за плавное6 движение камеры
        self.flag_coll = False # флаг, покзывающий соприкасается ли дудл с платформой 

    def check(self):
        if not (pygame.sprite.spritecollideany(self, all_sprites)):
            self.k += 1
        else:
            self.k = 0
        if not (pygame.sprite.spritecollideany(self, all_sprites)) and self.k > 50:
            screen.fill(red)
            self.kill()

    def update(self):
        if not self.flag_coll:
            self.n = 0
            self.camera = 0
        if self.rect.y > height - 200 and not self.flag:
            self.rect.y -= v / fps
        else:
            if self.rect.y > height - 100:
                self.flag = False
            else:
                self.flag = True
                self.rect.y += v / fps
        if pygame.sprite.spritecollideany(self, all_sprites):
            if pygame.sprite.spritecollideany(self, all_sprites) in platforms \
                    and pygame.sprite.spritecollideany(self, all_sprites).rect.y < self.rect.y:
                self.n = 600 - pygame.sprite.spritecollideany(self, all_sprites).rect.y
                self.flag_coll = True
            self.image = self.image_2
            self.jump = 1
        else:
            self.jump = 0
            self.image = self.image_1
        if self.flag_coll:
            self.camera = 10
            self.n -= 10
        if self.n <= 0:
            self.flag_coll = False
        if self.rect.y - self.camera <= 200:
            self.camera -= 10
        if self.direction and self.jump:
            self.image = pygame.transform.flip(self.image_2, 1, 0)
        elif self.direction and not self.jump:
            self.image = pygame.transform.flip(self.image, 1, 0)
        elif not self.direction and not self.jump:
            self.image = self.image
        elif not self.direction and self.jump:
            self.image = self.image_2
        for i in all_sprites:
            i.rect.y += self.camera
        self.check()

    def set_coords(self, x):
        self.rect.x -= x
        if x < 0:
            self.direction = 1
        else:
            self.direction = 0


player = Player()
ground = Ground()
x_pos = 0
y_pos = 500
all_sprites = pygame.sprite.Group()
for x in range(100):
    platforms.append(Platform(x_pos, y_pos))
    x_pos = random.randint(0, 300)
    y_pos -= random.randint(100, 150)

all_sprites.add(platforms)
player_g = pygame.sprite.Group()
all_sprites.add(ground)
player_g.add(player)
image_3 = pygame.image.load(os.path.join('data', 'textures', 'gameover.png'))
pygame.mixer.music.load("data/music/Windows_XP_Shutdown.mp3")
pygame.mixer.music.set_volume(0.4)
f = True

while running:
    if player_g:
        screen.blit(image, (0, 0))
    else:
        screen.fill(black)
        screen.blit(image_3, (0, 190))
        if f:
            pygame.mixer.music.play(1)
            f = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            pass
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_RIGHT]:
        player.set_coords(-10)
    elif pressed[pygame.K_LEFT]:
        player.set_coords(10)
    all_sprites.update()
    player_g.update()
    all_sprites.draw(screen)
    player_g.draw(screen)
    if not player_g:
        screen.blit(image_3, (0, 190))
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
