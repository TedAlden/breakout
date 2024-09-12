import pygame
import math
import random

from settings import *


class Ball(pygame.sprite.Sprite):

    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.width, self.height = 10, 10
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.new()

    def new(self):
        self.tick = WIN_FPS * 1  # Wait 1 second before moving ball
        self.rect.x, self.rect.y = WIN_WIDTH // 2, WIN_HEIGHT // 2
        self.direction = random.randint(135, 225)

    def __collide_screen(self):
        # Top edge of screen
        if self.rect.y <= 0:
            self.direction = (180 - self.direction) % 360
        # Bottom edge of screen
        if self.rect.y >= WIN_HEIGHT - self.height:
            self.new()
            self.game.score = max(self.game.score - BALL_MISS_PENALTY, 0)
            self.game.lives -= 1
        # Left edge of screen
        if self.rect.x <= 0:
            self.direction = (360 - self.direction) % 360
        # Right edge of screen
        if self.rect.x >= WIN_WIDTH - self.width:
            self.direction = (360 - self.direction) % 360

    def __collide_paddles(self):
        if self.rect.colliderect(self.game.paddle.rect):
            paddle = self.game.paddle
            if self.rect.x > paddle.rect.midleft[0] and self.rect.x < paddle.rect.midright[0]:
                # Top edge of paddle
                if self.rect.y <= paddle.rect.midtop[1]:
                    self.rect.y -= 5
                    self.direction = (180 - self.direction) % 360
                    vx = self.game.paddle.vel.x

                    if self.direction > 180:
                        if vx > 0:
                            self.direction = self.direction + BALL_SLIP
                        elif vx < 0:
                            self.direction = self.direction - BALL_SLIP

                    elif self.direction < 180:
                        if vx > 0:
                            self.direction = self.direction + BALL_SLIP
                        elif vx < 0:
                            self.direction = self.direction - BALL_SLIP
                # Bottom edge of paddle
                elif self.rect.y >= paddle.rect.midbottom[1]:
                    pass
            
            elif self.rect.y > paddle.rect.midtop[1] and self.rect.y < paddle.rect.midbottom[1]:
                # Left edge of paddle
                if self.rect.x >= paddle.rect.midleft[0]:
                    self.rect.x -= 5
                    self.rect.y -= 5
                    self.direction = (360 - self.direction) % 360
                # Right edge of paddle
                if self.rect.x <= paddle.rect.midright[0]:
                    self.rect.x += 5
                    self.rect.y -= 5
                    self.direction = (360 - self.direction) % 360

    def __collide_bricks(self):
        # FIXME: collisions with bricks sometimes register twice
        brick = pygame.sprite.spritecollideany(self, self.game.bricks)
        if brick:
            if self.rect.x > brick.rect.midleft[0] and self.rect.x < brick.rect.midright[0]:
                # Bottom edge of brick
                if self.rect.y <= brick.rect.midbottom[1]:
                    self.rect.y += 2
                    self.direction = (180 - self.direction) % 360
                # Top edge of brick
                elif self.rect.y >= brick.rect.midtop[1]:
                    self.rect.y -= 2
                    self.direction = (180 - self.direction) % 360

            elif self.rect.y > brick.rect.midtop[1] and self.rect.y < brick.rect.midbottom[1]:
                # Left edge of brick
                if self.rect.x >= brick.rect.midleft[0]:
                    self.rect.x -= 2
                    self.direction = (360 - self.direction) % 360
                # Right edge of brick
                elif self.rect.x <= brick.rect.midright[0]:
                    self.rect.x += 2
                    self.direction = (360 - self.direction) % 360
            brick.collide()  # Register collision with brick
            self.game.score += BALL_SCORE

    def update(self):
        if self.tick > 0:
            self.tick -= 1
            return
        # Calculate new x, y of ball based on it's speed and direction
        self.rect.x += BALL_SPEED * math.sin(math.radians(self.direction))
        self.rect.y -= BALL_SPEED * math.cos(math.radians(self.direction))
        # Check for collisions and adjust direction, x, y accordingly
        self.__collide_screen()
        self.__collide_paddles()
        self.__collide_bricks()    
        # Apply adjusted movement parameters to ball
        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
