
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
#colour_field = None

# Size for each memory field
blockSizeForField = 100

# Highlight duration (of a colour field) in milliseconds
highlight_dur = 1000

# Save highlighted fields
highlighted_field = None

# Var to keep track of the last highlighted field
last_highlighted_field = None
def grid():
    # Go through the grid in horizontal (x) and vertical (y) axis
    for x in range(0, width, blockSizeForField):
        for y in range(0, height, blockSizeForField):
            # Create rectangle at position x, y (with size blockSize * blockSize)
            rectangle = pygame.Rect(x, y, blockSizeForField, blockSizeForField)
            if (x, y) == highlighted_field:
                # Highlight the selected field
                pygame.draw.rect(window, RED, rectangle)
            else:
                pygame.draw.rect(window, WHITE, rectangle, 1)

def game_start():
    # Retrieve global defined vars (above)
    global game_has_started, wait_for_input, highlighted_field, last_highlighted_field

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
    highlighted_field = (x, y)

    # Store the position of the highlighted field
    last_highlighted_field = highlighted_field

    pygame.time.set_timer(pygame.USEREVENT, highlight_dur)


def check_for_input(pos):
        global wait_for_input, last_highlighted_field

        # Check that save_highlighted_field is not None before checking
        if last_highlighted_field:
            # Check if mouse click position is within the bounds of the highlighted field
            # For X-Axis (top [0]) and Y-Axis (line under [1]):
            if last_highlighted_field[0] <= pos[0] <= last_highlighted_field[0] + blockSizeForField and \
                    last_highlighted_field[1] <= pos[1] <= last_highlighted_field[1] + blockSizeForField:
                print("Nice!")
                # Correct guess -- reset for next round
                highlighted_field = None
                wait_for_input = False
            else:
                print("Not so good")

        # Reset after guessing
        last_highlighted_field = None

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
            # Set field to none (BLACK) when the timer event occurs
            highlighted_field = None
            # Stop the timer once the user event happens
            #pygame.time.set_timer(pygame.USEREVENT, 0)

        if event.type == pygame.MOUSEBUTTONDOWN and wait_for_input:
            check_for_input(pygame.mouse.get_pos())

    # Background colour
    window.fill(BLACK)

    # Draw grid
    grid()

    pygame.display.update()