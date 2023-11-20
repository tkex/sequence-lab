
import pygame
import sys
import random

# Initialize
pygame.init()

# Define pygame window props
width, height = 300, 300
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sequence lab!")

# Define colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Game control vars
game_has_started = False

# Var to control if player is guessing the fields
wait_for_input = False

# Var for position of the specific highlighted field
colour_field = None

# Size for each memory field
blockSizeForField = 100

# Highlight duration (of a colour field) in milliseconds
highlight_dur = 1000

def grid():
    # Go through the grid in horizontal (x) and vertical (y) axis
    for x in range(0, width, blockSizeForField):
        for y in range(0, height, blockSizeForField):
            # Create rectangle at position x, y (with size blockSize * blockSize)
            rectangle = pygame.Rect(x, y, blockSizeForField, blockSizeForField)
            if (x, y) == colour_field:
                # Highlight the selected field
                pygame.draw.rect(window, RED, rectangle)
            else:
                pygame.draw.rect(window, WHITE, rectangle, 1)

def game_start():
    # Retrieve global defined vars (above)
    global game_has_started, colour_field, wait_for_input

    # Set the game as started
    game_has_started = True
    print(f"The sequence game has started!")

    # False since the user is not in input state if game starts
    wait_for_input = False

    # Select a random field
    # First generate a random number (0 to 2) since it's 3x3 and mult by block size of a field
    # to get a rand coordinate x and y in (!) the grid
    x = random.randint(0, 2) * blockSizeForField
    y = random.randint(0, 2) * blockSizeForField

    # Store the coordinates of the highlighted field
    colour_field = (x, y)

    pygame.time.set_timer(pygame.USEREVENT, highlight_dur)


def check_for_input(pos):
        global wait_for_input, colour_field
        if colour_field[0] <= pos[0] <= colour_field[0] + blockSizeForField and \
            colour_field[1] <= pos[1] <= colour_field[1] + blockSizeForField:
            print("Nice!")
        else:
            print("Not so good")

        # State input is over
        wait_for_input = False

        # Set colour field after guessing back to black
        colour_field = None

# Loop
while True:

    for event in pygame.event.get():
        # Close event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Space
        if event.type == pygame.KEYDOWN:
            # If space is pressed and game not started yet
            if event.key == pygame.K_SPACE and not game_has_started:
                # Start the game
                game_start()

        # Player event
        if event.type == pygame.USEREVENT:
            # Set for input state
            wait_for_input = True
            pygame.time.set_timer(pygame.USEREVENT, 0)

        if event.type == pygame.MOUSEBUTTONDOWN and wait_for_input:
            check_for_input(pygame.mouse.get_pos())

    # Background colour
    window.fill(BLACK)

    # Draw grid
    grid()

    pygame.display.update()