import pygame, sys, math, random, os, pathlib

WIN_WIDTH = 720
WIN_HEIGHT = 480
WIN_TITLE = "Breakout"
WIN_FPS = 360

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

GREEN = (26, 175, 61)
YELLOW = (255, 186, 17)
ORANGE = (229, 93, 12)
RED = (224, 17, 24)
PURPLE = (160, 31, 146)
BLUE = (33, 142, 192)

PADDLE_SPEED = 1
BALL_SPEED = 1
BALL_SLIP = 20
# how many degrees the movement of the paddle will change the direction of the
# ball by
ENABLE_BALL_SLIP = True

BALL_MISS_PENALTY = 100
BALL_SCORE = 10

MAX_LIVES = 3

FONT_PATH = os.path.join(pathlib.Path(__file__).parent.absolute(), "assets", "font.ttf")

vec = pygame.math.Vector2

def clamp(num, min_value, max_value):
	return max(min(num, max_value), min_value)


class Game:

	def __init__(self):
		pygame.init()
		pygame.font.init()
		self.font = pygame.font.Font(FONT_PATH, 60)
		self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
		pygame.display.set_caption(WIN_TITLE)
		self.clock = pygame.time.Clock()

		self.all_sprites = pygame.sprite.Group()
		self.bricks = pygame.sprite.Group()
		self.balls = pygame.sprite.Group()
		self.paddles = pygame.sprite.Group()

		self.new()

	def new(self):
		self.paddle = Paddle(self)
		self.ball = Ball(self)
		self.score = 0
		self.lives = 3
		
		Brick(self, 2, 24, GREEN, 2)
		Brick(self, 82, 24, GREEN, 2)
		Brick(self, 162, 24, GREEN, 2)
		Brick(self, 242, 24, GREEN, 2)
		Brick(self, 322, 24, GREEN, 2)
		Brick(self, 402, 24, GREEN, 2)
		Brick(self, 482, 24, GREEN, 2)
		Brick(self, 562, 24, GREEN, 2)
		Brick(self, 642, 24, GREEN, 2)

		Brick(self, 2, 54, YELLOW, 2)
		Brick(self, 82, 54, YELLOW, 2)
		Brick(self, 162, 54, YELLOW, 2)
		Brick(self, 242, 54, YELLOW, 2)
		Brick(self, 322, 54, YELLOW, 2)
		Brick(self, 402, 54, YELLOW, 2)
		Brick(self, 482, 54, YELLOW, 2)
		Brick(self, 562, 54, YELLOW, 2)
		Brick(self, 642, 54, YELLOW, 2)

		Brick(self, 2, 84, ORANGE, 2)
		Brick(self, 82, 84, ORANGE, 2)
		Brick(self, 162, 84, ORANGE, 2)
		Brick(self, 242, 84, ORANGE, 2)
		Brick(self, 322, 84, ORANGE, 2)
		Brick(self, 402, 84, ORANGE, 2)
		Brick(self, 482, 84, ORANGE, 2)
		Brick(self, 562, 84, ORANGE, 2)
		Brick(self, 642, 84, ORANGE, 2)

		Brick(self, 2, 114, RED, 1)
		Brick(self, 82, 114, RED, 1)
		Brick(self, 162, 114, RED, 1)
		Brick(self, 242, 114, RED, 1)
		Brick(self, 322, 114, RED, 1)
		Brick(self, 402, 114, RED, 1)
		Brick(self, 482, 114, RED, 1)
		Brick(self, 562, 114, RED, 1)
		Brick(self, 642, 114, RED, 1)

		Brick(self, 2, 144, PURPLE, 1)
		Brick(self, 82, 144, PURPLE, 1)
		Brick(self, 162, 144, PURPLE, 1)
		Brick(self, 242, 144, PURPLE, 1)
		Brick(self, 322, 144, PURPLE, 1)
		Brick(self, 402, 144, PURPLE, 1)
		Brick(self, 482, 144, PURPLE, 1)
		Brick(self, 562, 144, PURPLE, 1)
		Brick(self, 642, 144, PURPLE, 1)

		Brick(self, 2, 174, BLUE, 1)
		Brick(self, 82, 174, BLUE, 1)
		Brick(self, 162, 174, BLUE, 1)
		Brick(self, 242, 174, BLUE, 1)
		Brick(self, 322, 174, BLUE, 1)
		Brick(self, 402, 174, BLUE, 1)
		Brick(self, 482, 174, BLUE, 1)
		Brick(self, 562, 174, BLUE, 1)
		Brick(self, 642, 174, BLUE, 1)

	def start(self):
		self.running = True
		while self.running:
			self.dt = self.clock.tick(WIN_FPS) / 1000
			self.events()
			self.update()
			self.draw()

		pygame.quit()
		sys.exit()

	def stop(self):
		self.running = False

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.stop()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.stop()

	def update(self):
		self.all_sprites.update()

		if len(self.bricks) <= 0 or self.lives <= 0:
			print("game over")

		print(self.score)

	def draw(self):
		self.screen.fill(BLACK)
		
		self.paddle.draw()
		self.ball.draw()
		for brick in self.bricks:
			brick.draw()

		score = self.font.render("SCORE: " + str(self.score), False, WHITE)
		self.screen.blit(score, (2, -8))

		lives = self.font.render("LIVES: " + str(self.lives), False, WHITE)
		self.screen.blit(lives, (WIN_WIDTH - lives.get_rect().width - 3, -8))

		pygame.display.flip()


class Paddle(pygame.sprite.Sprite):

	def __init__(self, game):
		self.game = game
		self.groups = game.all_sprites, game.paddles
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.width, self.height = 180, 10
		self.image = pygame.Surface((self.width, self.height))
		self.image.fill(WHITE)
		self.rect = self.image.get_rect()
		self.rect.midbottom = (WIN_WIDTH/2, WIN_HEIGHT - 20)

		self.vel = vec(0, 0)

	def draw(self):
		self.game.screen.blit(self.image, self.rect)

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


class Brick(pygame.sprite.Sprite):

	def __init__(self, game, x, y, colour, hp):
		self.game = game
		self.colour = colour
		self.hp = hp
		self.groups = game.all_sprites, game.bricks
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.width, self.height = 76, 25
		self.image = pygame.Surface((self.width, self.height))
		self.image.fill(self.colour)
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = x, y

	def draw(self):
		self.game.screen.blit(self.image, self.rect)

	def collide(self):
		self.hp -= 1
		if self.hp == 0:
			self.kill()
		print(len(self.game.bricks))

		# darken the bricks when they are hit
		r = int(self.colour[0] / 2)
		g = int(self.colour[1] / 2)
		b = int(self.colour[2] / 2)

		self.colour = (r, g, b)
		self.image.fill(self.colour)


class Ball(pygame.sprite.Sprite):

	def __init__(self, game):
		self.game = game
		self.groups = game.all_sprites, game.balls
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.width, self.height = 10, 10
		self.image = pygame.Surface((self.width, self.height))
		self.image.fill(WHITE)
		self.rect = self.image.get_rect()

		self.direction = 0
		self.speed = BALL_SPEED

		self.new()

	def new(self):
		self.x, self.y = WIN_WIDTH/2, WIN_HEIGHT/2
		self.rect.x, self.rect.y = self.x, self.y
		self.direction = random.randint(135, 225)

		self.tick = 0

	def update(self):
		# -------------------- move the ball -------------------- #
		self.tick += 1

		if self.tick < 360:
			return

		direction_radians = math.radians(self.direction)

		self.x += self.speed * math.sin(direction_radians)
		self.y -= self.speed * math.cos(direction_radians)
 	
		# -------------- collide with screen edges -------------- #

		if self.y <= 0: # top edge
			self.direction = (180 - self.direction) % 360
 
		if self.y >= WIN_HEIGHT - self.height: # bottom edge
			#self.direction = (180 - self.direction) % 360
			self.new()
			self.game.score = max(self.game.score - BALL_MISS_PENALTY, 0)
			self.game.lives -= 1
 
		if self.x <= 0: # left edge
			self.direction = (360 - self.direction) % 360
			 
		if self.x >= WIN_WIDTH - self.width: # right edge
			self.direction = (360 - self.direction) % 360

		# ----------------- collide with paddle ----------------- #

		if self.rect.colliderect(self.game.paddle.rect):

			hit = self.game.paddle

			if self.x > hit.rect.midleft[0] and self.x < hit.rect.midright[0]:
				
				if self.y <= hit.rect.midtop[1]: # top of paddle

					self.y -= 5
					self.direction = (180 - self.direction) % 360
					vx = self.game.paddle.vel.x

					if ENABLE_BALL_SLIP:
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

				elif self.y >= hit.rect.midbottom[1]: # bottom of paddle
					pass

			elif self.y > hit.rect.midtop[1] and self.y < hit.rect.midbottom[1]:
				
				if self.x <= hit.rect.midleft[0]: # left of paddle
					self.x -= 2
					self.direction = (360 - self.direction) % 360

				if self.x >= hit.rect.midright[0]: # right of paddle
					# FIX: Not recognising this collision for some reason
					self.x += 5
					self.direction = (360 - self.direction) % 360

		# ----------------- collide with bricks ----------------- #

		hit = pygame.sprite.spritecollideany(self, self.game.bricks)

		if hit:
			
			if self.x > hit.rect.midleft[0] and self.x < hit.rect.midright[0]:

				if self.y <= hit.rect.midbottom[1]: # bottom of brick
					self.y += 2
					self.direction = (180 - self.direction) % 360

				elif self.y >= hit.rect.midtop[1]: # top of brick
					self.y -= 2
					self.direction = (180 - self.direction) % 360

			elif self.y > hit.rect.midtop[1] and self.y < hit.rect.midbottom[1]:

				if self.x <= hit.rect.midleft[0]: # left of brick
					self.x -= 2
					self.direction = (360 - self.direction) % 360

				elif self.x >= hit.rect.midright[0]: # right of brick
					self.x += 2
					self.direction = (360 - self.direction) % 360

			hit.collide() # make the brick register the collision
			self.game.score += BALL_SCORE

		# ---------------- apply movement to ball --------------- #

		self.rect.x = round(self.x)
		self.rect.y = round(self.y)
		# the movement can be rounded to an integer, because it can only move an
		# integer amount of pixels, i.e. it cannot move 0.5 pixels

	def draw(self):
		self.game.screen.blit(self.image, self.rect)


Game().start()