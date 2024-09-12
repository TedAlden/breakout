import pathlib


# Window settings
WIN_WIDTH = 720
WIN_HEIGHT = 480
WIN_TITLE = "Breakout"
WIN_FPS = 120

FONT_PATH = pathlib.Path(pathlib.Path(__file__).parent.absolute(), "assets", "font.ttf")

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (224, 17, 24)
ORANGE = (229, 93, 12)
YELLOW = (255, 186, 17)
GREEN = (26, 175, 61)
BLUE = (33, 142, 192)
PURPLE = (160, 31, 146)

# Padding settings
PADDLE_SPEED = 3

# Ball settings
BALL_MISS_PENALTY = 100
BALL_SCORE = 10
BALL_SPEED = 3
BALL_SLIP = 20  
# Ball slip is how many degrees the movement of the paddle can change
# the direction of the ball by.

# Game settings
MAX_LIVES = 3
