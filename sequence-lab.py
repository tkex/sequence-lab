
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

feedback_highlight = None

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

    if feedback_highlight:
        pygame.draw.rect(window, feedback_highlight[1],
                         pygame.Rect(feedback_highlight[0][0], feedback_highlight[0][1], blockSizeForField,
                                     blockSizeForField))

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
    global wait_for_input, last_highlighted_field, feedback_highlight

    # Calculate position of the clicked field
    # Check if mouse click position is within the bounds of the highlighted field
    # For X-Axis (top [0]) and Y-Axis (line under [1]):
    clicked_field_x = pos[0] // blockSizeForField * blockSizeForField
    clicked_field_y = pos[1] // blockSizeForField * blockSizeForField

    clicked_field = (clicked_field_x, clicked_field_y)

    # Check that save_highlighted_field is not None before checking
    if last_highlighted_field:
        if last_highlighted_field:
            if last_highlighted_field == clicked_field:
                print("Nice!")
                feedback_highlight = (clicked_field, RED)
            else:
                print("Not so good")
                feedback_highlight = (clicked_field, WHITE)

        # Show  Feedback with 500 ms delay (before last_highlighted_field is resetted)
        pygame.time.set_timer(pygame.USEREVENT + 1, 500)


#  End of feedback light and reset it (will be called from timer event in check for input)
def end_feedback():
    global feedback_highlight, last_highlighted_field

    # Reset
    feedback_highlight = None
    last_highlighted_field = None

    # Stop Feedback event
    pygame.time.set_timer(pygame.USEREVENT + 1, 0)

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

        # Will be called after 500ms from ccheck for input
        if event.type == pygame.USEREVENT + 1:
            end_feedback()

    # Background colour
    window.fill(BLACK)

    # Draw grid
    grid()

    pygame.display.update()