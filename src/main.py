import pygame

from paddle import Paddle
from brick import Brick
from ball import Ball
from settings import *


def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)


class Game:

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font(FONT_PATH, 60)
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.bricks = pygame.sprite.Group()
        pygame.display.set_caption(WIN_TITLE)

    def new(self):
        self.running = True
        self.paddle = Paddle(self)
        self.ball = Ball(self)
        self.score = 0
        self.lives = MAX_LIVES
        # Colour and HP of each row of bricks
        colours = (GREEN, YELLOW, ORANGE, RED, PURPLE, BLUE)
        healths = (2, 2, 2, 1, 1, 1)
        # Create bricks using above layout
        for row, y in enumerate((24, 54, 84, 114, 144, 174)):
            for x in (2, 82, 162, 242, 322, 402, 482, 562, 642):
                Brick(self, x, y, colours[row], healths[row])

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        self.dt = self.clock.tick(WIN_FPS) / 1000
        self.paddle.update()
        self.ball.update()
        # If player wins (breaks all bricks) or loses (out of lives)
        if len(self.bricks) <= 0 or self.lives <= 0:
            self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        # Draw sprites
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.bricks.draw(self.screen)
        # Draw text
        score = self.font.render("SCORE: " + str(self.score), False, WHITE)
        lives = self.font.render("LIVES: " + str(self.lives), False, WHITE)
        self.screen.blit(score, (2, -8))
        self.screen.blit(lives, (WIN_WIDTH - lives.get_rect().width - 3, -8))
        # Flip screen
        pygame.display.flip()


if __name__ == "__main__":
    g = Game()
    g.new()
    while g.running:
        g.events()
        g.update()
        g.draw()
