
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

# List to save the sequence of fields
sequence_of_fields = []
# Index for the current step in the sequence
current_sequence_index = 0

# Global variables for the duration of the display and feedback
highlight_duration = 1000  # Duration of highlighting a field in milliseconds
feedback_duration = 200    # Duration of the feedback in milliseconds

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


def add_new_field_to_sequence():
    # Random field
    x = random.randint(0, 2) * blockSizeForField
    y = random.randint(0, 2) * blockSizeForField

    # Add field
    sequence_of_fields.append((x, y))


def game_start():
    # Retrieve global defined vars (above)
    global game_has_started, wait_for_input, highlighted_field, sequence_of_fields, current_sequence_index

    # Set the game as started
    game_has_started = True
    print(f"The sequence game has started!")

    # Reset the sequence when restarting the game
    sequence_of_fields = []
    current_sequence_index = 0
    add_new_field_to_sequence()
    highlighted_field = sequence_of_fields[current_sequence_index]
    last_highlighted_field = None

    # False since the user is not in input state if game starts
    wait_for_input = False

    # Select a random field
    # First generate a random number (0 to 2) since it's 3x3 and mult by block size of a field
    # to get a rand coordinate x and y in (!) the grid
    #x = random.randint(0, 2) * blockSizeForField
    #y = random.randint(0, 2) * blockSizeForField

    # Store the coordinates of the highlighted field
    #highlighted_field = (x, y)

    # Store the position of the highlighted field
    last_highlighted_field = highlighted_field

    pygame.time.set_timer(pygame.USEREVENT, highlight_duration)


def check_for_input(pos):
    global wait_for_input, feedback_highlight, current_sequence_index, game_has_started

    # Calculate position of the clicked field
    # Check if mouse click position is within the bounds of the highlighted field
    # For X-Axis (top [0]) and Y-Axis (line under [1]):
    clicked_field_x = pos[0] // blockSizeForField * blockSizeForField
    clicked_field_y = pos[1] // blockSizeForField * blockSizeForField

    clicked_field = (clicked_field_x, clicked_field_y)

    # Check that save_highlighted_field is not None before checking
    if sequence_of_fields[current_sequence_index] == clicked_field:
        print("Nice!")
        # Set feedback highlight to red for a correct guess
        feedback_highlight = (clicked_field, RED)

        # Increment the sequence index
        current_sequence_index += 1

        # Check if the whole sequence has been guessed correctly
        if current_sequence_index == len(sequence_of_fields):
            # Add new sequence field
            add_new_field_to_sequence()

            # Reset sequence index
            current_sequence_index = 0

            # Set timer to display the next field in sequence
            pygame.time.set_timer(pygame.USEREVENT, highlight_duration)

        # Set timer for the feedback to be displayed
        pygame.time.set_timer(pygame.USEREVENT + 1, 200)
    else:
        print("Game over")
        # End game if the guess is wrong
        game_has_started = False

        # Set feedback highlight to white for incorrect guess
        feedback_highlight = (clicked_field, WHITE)

        # Set timer for the feedback to be displayed
        pygame.time.set_timer(pygame.USEREVENT + 1, feedback_duration)



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
            if current_sequence_index < len(sequence_of_fields):
                highlighted_field = sequence_of_fields[current_sequence_index]
                current_sequence_index += 1
                # Only set the timer if there are other fields in the sequence
                if current_sequence_index < len(sequence_of_fields):
                    pygame.time.set_timer(pygame.USEREVENT, highlight_duration)
            else:
                # Exits the display of the sequence and waits for user input
                wait_for_input = True
                highlighted_field = None
                current_sequence_index = 0
                # Stop timer
                pygame.time.set_timer(pygame.USEREVENT, 0)

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