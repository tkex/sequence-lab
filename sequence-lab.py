
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

# Var for position of the specific highlighted field
colour_field = None

# Size for each memory field
blockSizeForField = 100

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
            '''
            # Create rectangle at position x, y (with size blockSize * blockSize)
            rectangle = pygame.Rect(x, y, blockSizeForField, blockSizeForField)
            # Create rectangle at window
            # width = 1: only the border is drawn
            pygame.draw.rect(window, WHITE, rectangle, 1)
            '''

def game_start():
    # Retrieve global defined vars (above)
    global game_has_started, colour_field

    # Set the game as started
    game_has_started = True
    print(f"The sequence game has started!")

    # Select a random field
    # First generate a random number (0 to 2) since it's 3x3 and mult by block size of a field
    # to get a rand coordinate x and y in (!) the grid
    x = random.randint(0, 2) * blockSizeForField
    y = random.randint(0, 2) * blockSizeForField

    # Store the coordinates of the highlighted field
    colour_field = (x, y)


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

    # Background colour
    window.fill(BLACK)

    # Draw grid
    grid()

    pygame.display.update()