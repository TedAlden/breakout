import pygame

from settings import *


class Paddle(pygame.sprite.Sprite):

    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.width, self.height = 180, 10
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (WIN_WIDTH/2, WIN_HEIGHT - 20)
        self.vel = pygame.math.Vector2(0, 0)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pressed = pygame.key.get_pressed()
        self.vel.x = 0

        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            if self.rect.midleft[0] > 0:
                self.vel.x = -PADDLE_SPEED

        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            if self.rect.midright[0] < WIN_WIDTH:
                self.vel.x = PADDLE_SPEED

        self.rect.x += self.vel.x
