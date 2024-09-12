import pygame


class Brick(pygame.sprite.Sprite):

    def __init__(self, game, x, y, colour, hp):
        self.colour = colour
        self.hp = hp
        pygame.sprite.Sprite.__init__(self, game.bricks)
        self.width, self.height = 76, 25
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collide(self):
        self.hp -= 1
        if self.hp == 0:
            self.kill()
        # darken the bricks when they are hit
        r = int(self.colour[0] // 2)
        g = int(self.colour[1] // 2)
        b = int(self.colour[2] // 2)
        self.colour = (r, g, b)
        self.image.fill(self.colour)
