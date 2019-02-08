import pygame
import os
import random

pygame.init()
running = True
image = pygame.image.load(os.path.join('data', 'background.png'))
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
        self.image = pygame.image.load(os.path.join('data', 'ground.png'))
        self.image = pygame.transform.scale(self.image, (480, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = height - 50
        self.mask = pygame.mask.from_surface(self.image)


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('data', 'platform.png'))
        self.image = pygame.transform.scale(self.image, (100, 25))
        self.rect = self.image.get_rect()
        self.rect.x = 90
        self.rect.y = 500
        print(self.rect)

    def update(self):
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_1 = pygame.image.load(os.path.join('data', 'doodle.png'))
        self.image_2 = pygame.image.load(os.path.join('data', 'doodle_pr.png'))
        self.image = pygame.image.load(os.path.join('data', 'doodle.png'))
        self.mask = pygame.mask.from_surface(self.image)
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.image_1 = pygame.transform.scale(self.image, (80, 80))
        self.image_2 = pygame.transform.scale(self.image_2, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = width // 2 - 40
        self.rect.y = height - 100
        self.direction = 0
        self.jump = False
        self.flag = False
        self.camera = 0
        self.k = 0

    def check(self):
        if not (pygame.sprite.spritecollideany(self, all_sprites)):
            self.k += 1
        else:
            self.k = 0
        if not (pygame.sprite.spritecollideany(self, all_sprites)) and self.k > 50:
            screen.fill(red)
            self.kill()

    def update(self):
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
            if pygame.sprite.spritecollideany(self, all_sprites) == platform \
                    and pygame.sprite.spritecollideany(self, all_sprites).rect.y < self.rect.y:
                self.camera = 100
            self.image = self.image_2
            self.jump = 1
        else:
            self.jump = 0
            self.image = self.image_1
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
platform = Platform()
all_sprites = pygame.sprite.Group()
player_g = pygame.sprite.Group()
all_sprites.add(ground)
all_sprites.add(platform)
player_g.add(player)
image_3 = pygame.image.load(os.path.join('data', 'gameover.png'))

while running:
    if player_g:
        screen.blit(image, (0, 0))
    else:
        screen.fill(black)
        screen.blit(image_3, (0, 190))
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
    player_g.draw(screen)
    all_sprites.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
