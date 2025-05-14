WIDTH = 720  # Size of the board
HEIGHT = 720

SCREEN_WIDTH = 720  # Size of the screen
SCREEN_HEIGHT = 800
DIMENSION = 9  #
CELL_SIZE = 55  # = 64 #
GRID = (80, 105, 57.5)  # RGB color for the grid

MAX_FPS = 15
BUT_WIDTH = BUT_HEIGHT = 62.5  # Size of the button

# Button position
BACKWARD_X = WIDTH / 2 - 2 * BUT_HEIGHT  # Position of the backward button
BACKWARD_Y = SCREEN_HEIGHT - BUT_HEIGHT

NEXTSTEP_X = BACKWARD_X + BUT_WIDTH  # Position of the next step button
NEXTSTEP_Y = BACKWARD_Y

REPLAY_X = BACKWARD_X + 2 * BUT_WIDTH  # Position of the reverse button
REPLAY_Y = BACKWARD_Y

START_X = WIDTH / 2 - BUT_WIDTH / 2  # Position of the start button
START_Y = HEIGHT / 2 - BUT_HEIGHT / 2

REVERSE_X = BACKWARD_X + 3 * BUT_WIDTH  # Position of the replay button
REVERSE_Y = BACKWARD_Y

REPLAY_X = BACKWARD_X + 3 * BUT_WIDTH  # Position of the replay button
REPLAY_Y = BACKWARD_Y

BUT_TEXT = 300  # Size of the button text
BUTTEXT_X = SCREEN_WIDTH / 2 - BUT_TEXT / 2
BUTTEXT_Y = HEIGHT / 2 - 50

TITLE_WIDTH = 300
TITLE_WIDTH_X = SCREEN_WIDTH / 2
TITLE_HEIGHT_Y = 100
