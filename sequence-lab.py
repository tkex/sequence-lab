
import os
import pygame
import sys
import random
import time

# Initialize
pygame.init()
pygame.mixer.init()

# Constants for window size
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 300

pygame.display.set_caption("Sequence lab!")
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (65, 105, 225)

# Constants for game control
BLOCK_SIZE_FOR_FIELD = 100  # Size of each memory field
HIGHLIGHT_DURATION = 1000  # Highlight duration (of a color field) in milliseconds
ROUND_PAUSE_TIME = 1500  # Time in ms between each round
FEEDBACK_DURATION = 1000  # Duration of the feedback in milliseconds

# Colors for different states
CLICKED_FIELD_COLOUR = BLUE
SHOWN_FIELD_COLOUR = RED
WRONG_GUESSES_FIELD_COLOUR = WHITE

# Sound paths
REWARD_SOUND = pygame.mixer.Sound("audio/belohnungston.wav")
LOSE_SOUND = pygame.mixer.Sound("audio/verlorenton.wav")
DULL_SOUND = pygame.mixer.Sound("audio/stumpfer_ton.wav")

# Event-IDs
NEW_ROUND_EVENT = pygame.USEREVENT + 2
FEEDBACK_EVENT = pygame.USEREVENT + 1

# Log constants
LOG_DIRECTORY = "logs"

# Game control vars
game_has_started = False  # Control flag to determine if game has started

wait_for_input = False  # Control flag for waiting for player input

highlighted_field = None  # Stores the currently highlighted field coordinates (X/Y)

last_highlighted_field = None  # Stores the last field that was highlighted

feedback_highlight = None  # Stores information for highlighting feedback (position and color)

sequence_of_fields = []  # List to save the sequence of fields that the player needs to remember sequentially

current_sequence_idx = 0  # Index to determine the current step in the sequence the player is at

current_level = 0  # Var to track the current level

sound_mode = 0  # Var to control the sound mode (0: no sound, 1: randomized sounds, 3: dull sounds)

field_sounds = {}  # Dictionary to map fields to (randomized) sounds

sounds_assigned = False  # Control flag to check if sounds have been assigned to fields

round_start_time = 0  # Var to store the start time (of the current round)

# ------------------------------------------
# *** *** *** *** GAME LOGIC *** *** *** ***
# ------------------------------------------

# Loading all tones for mode "2"
def load_sounds_for_mode_2():
    sounds = []

    for i in range(1, 10):
        sound = pygame.mixer.Sound(f"audio/ton_{i}.wav")
        sounds.append(sound)

    return sounds


# Playing sounds
def play_sound(sound):
    if sound_mode in [2, 3]:
        sound.play()


# Function for playing the sound for a specific field
def play_sound_for_field(x, y):
    if sound_mode == 2 and (x, y) in field_sounds:
        field_sounds[(x, y)].play()
    elif sound_mode == 3:
        DULL_SOUND.play()


# Function for assigning sounds to the fields
def assign_sounds_to_fields():
    global field_sounds, sounds_assigned

    if not sounds_assigned:
        sounds = load_sounds_for_mode_2()
        random.shuffle(sounds)
        field_index = 0

        for x in range(0, WINDOW_WIDTH, BLOCK_SIZE_FOR_FIELD):
            for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE_FOR_FIELD):
                field_sounds[(x, y)] = sounds[field_index % len(sounds)]
                field_index += 1

        sounds_assigned = True


def grid():
    # Go through the grid in horizontal (x) and vertical (y) axis
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE_FOR_FIELD):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE_FOR_FIELD):
            # Create rectangle at position x, y (with size blockSize * blockSize)
            rectangle = pygame.Rect(x, y, BLOCK_SIZE_FOR_FIELD, BLOCK_SIZE_FOR_FIELD)
            if (x, y) == highlighted_field:
                # Highlight the selected field
                pygame.draw.rect(window, SHOWN_FIELD_COLOUR, rectangle)
            else:
                pygame.draw.rect(window, WRONG_GUESSES_FIELD_COLOUR, rectangle, 1)

    if feedback_highlight:
        pygame.draw.rect(window, feedback_highlight[1],
                         pygame.Rect(feedback_highlight[0][0], feedback_highlight[0][1], BLOCK_SIZE_FOR_FIELD,
                                     BLOCK_SIZE_FOR_FIELD))


def add_new_field_to_sequence():
    global current_level

    while True:
        # Random field
        x = random.randint(0, 2) * BLOCK_SIZE_FOR_FIELD
        y = random.randint(0, 2) * BLOCK_SIZE_FOR_FIELD

        new_field = (x, y)

        # Check if new field is different from the last field in the sequence
        # so that no consecutive overlapping fields are to be guessed
        if not sequence_of_fields or new_field != sequence_of_fields[-1]:
            # Add field
            sequence_of_fields.append(new_field)

            # Update the current level
            current_level += 1
            print(f"==> (Reached) Level: {current_level}")
            break


def game_start():
    # Retrieve global defined vars (above)
    global game_has_started, wait_for_input, highlighted_field, sequence_of_fields, current_sequence_idx, current_level, round_start_time

    # Set time for log data
    round_start_time = pygame.time.get_ticks()

    # Reset current level (Set to null)
    current_level = 0

    # Set the game as started
    game_has_started = True
    print(f"== The sequence game has started! ==")

    # Reset the sequence when restarting the game
    sequence_of_fields = []
    current_sequence_idx = 0
    add_new_field_to_sequence()
    highlighted_field = sequence_of_fields[current_sequence_idx]

    # False since the user is not in input state if game starts
    wait_for_input = False

    # Play sound for the first field
    if sound_mode == 2:
        play_sound_for_field(*highlighted_field)
    elif sound_mode == 3:
        play_sound(DULL_SOUND)

    pygame.time.set_timer(pygame.USEREVENT, HIGHLIGHT_DURATION)


def check_for_input(pos):
    global wait_for_input, feedback_highlight, current_sequence_idx, game_has_started, round_start_time, sound_mode

    # Calculate position of the clicked field
    # Check if mouse click position is within the bounds of the highlighted field
    # For X-Axis (top [0]) and Y-Axis (line under [1]):
    clicked_field_x = pos[0] // BLOCK_SIZE_FOR_FIELD * BLOCK_SIZE_FOR_FIELD
    clicked_field_y = pos[1] // BLOCK_SIZE_FOR_FIELD * BLOCK_SIZE_FOR_FIELD

    clicked_field = (clicked_field_x, clicked_field_y)

    # Check that save_highlighted_field is not None before checking plus whether the index is within the length of the sequence
    if current_sequence_idx < len(sequence_of_fields) and sequence_of_fields[current_sequence_idx] == clicked_field:
        print("Guessed correctly!")

        if sound_mode == 2:
            play_sound(field_sounds[clicked_field])
        elif sound_mode == 3:
            play_sound(DULL_SOUND)

        # Set feedback highlight to red for a correct guess
        feedback_highlight = (clicked_field, CLICKED_FIELD_COLOUR)

        # Increment the sequence index
        current_sequence_idx += 1

        # Check if the whole sequence has been guessed correctly
        if current_sequence_idx == len(sequence_of_fields):
            # Don't allow clicks if all fields are guessed correctly
            wait_for_input = False

            # Add event with a n-second delay before starting the new sequence
            pygame.time.set_timer(NEW_ROUND_EVENT, ROUND_PAUSE_TIME)

        # Set timer for the feedback to be displayed
        pygame.time.set_timer(FEEDBACK_EVENT, FEEDBACK_DURATION)

    else:
        print("-- Game over --")

        # Log game session time and level (for logging)
        round_end_time = pygame.time.get_ticks()
        round_duration = (round_end_time - round_start_time) / 1000
        round_duration = round(round_duration, 2)

        # Define and show log
        log_info = f"Playmode: {sound_mode}, Playtime of round: {round_duration} seconds, Reached level: {current_level}"
        print(log_info)

        # Save log into file:
        # Generate unique ID and time stamp for file naming (Unix epoch)
        unique_id = round(time.time() * 1000)
        timestamp = time.strftime("%d%m%Y-%H%M%S")

        # Create log folder in case it doesn't exist already
        if not os.path.exists(LOG_DIRECTORY):
            os.makedirs(LOG_DIRECTORY)

        # Create filename based on timestamp and the unique id
        log_filename = f"{LOG_DIRECTORY}/log_{timestamp}_{unique_id}.txt"

        # Write log info into file
        with open(log_filename, 'w') as file:
            file.write(log_info)

        # Play the losing sound if an incorrect field is selected
        # (only in sound_modus)
        play_sound(LOSE_SOUND)

        # End game if the guess is wrong
        game_has_started = False

        # Set feedback highlight to white for incorrect guess
        feedback_highlight = (clicked_field, WRONG_GUESSES_FIELD_COLOUR)

        # Set timer for the feedback to be displayed
        pygame.time.set_timer(FEEDBACK_EVENT, FEEDBACK_DURATION)

        # Disable further input (!)
        wait_for_input = False


# End of feedback light and reset it (will be called from timer event in check for input)
def end_feedback():
    global feedback_highlight, last_highlighted_field

    # Reset
    feedback_highlight = None
    last_highlighted_field = None

    # Stop Feedback event
    pygame.time.set_timer(FEEDBACK_EVENT, 0)


# Main-Loop
while True:

    for event in pygame.event.get():
        # Pygame close event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Hotkeys for different sound modi (1, 2 and 3)
        if event.type == pygame.KEYDOWN:
            # If "1" is pressed
            if event.key == pygame.K_1:
                sound_mode = 1
                print("Mode 1 activated: No sound")

        if event.type == pygame.KEYDOWN:
            # If "2" is pressed
            if event.key == pygame.K_2 and not sounds_assigned:
                sound_mode = 2
                print("Mode 2 activated: 9 different sounds")
                print("Each field now has an individual tone!")
                assign_sounds_to_fields()
                sounds_assigned = True

            # If "3" is pressed
            elif event.key == pygame.K_3 and not sounds_assigned:
                sound_mode = 3
                print("Mode 3 activated: Dull/Muffled sound")
                print("Mode 3 activated: Every field now has a dull sound")

        # If "Space" is pressed, start the game
        if event.type == pygame.KEYDOWN:
            # If space is pressed and game has not started yet
            if event.key == pygame.K_SPACE and not game_has_started:

                # Start the game
                game_start()

        # If "Enter" is pressed, restart the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not game_has_started:

                # Restart game
                game_start()

        # Player event
        if event.type == pygame.USEREVENT:
            if current_sequence_idx < len(sequence_of_fields):

                # Play sound if field is showing
                if sound_mode == 2:
                    play_sound_for_field(*sequence_of_fields[current_sequence_idx])
                elif sound_mode == 3:
                    play_sound(DULL_SOUND)

                highlighted_field = sequence_of_fields[current_sequence_idx]
                current_sequence_idx += 1

                # Only set the timer if there are other fields in the sequence
                if current_sequence_idx < len(sequence_of_fields):
                    pygame.time.set_timer(pygame.USEREVENT, HIGHLIGHT_DURATION)

                # Player not allowed to guess / click
                wait_for_input = False

            else:
                # Exits the display of the sequence and waits for user input
                wait_for_input = True
                highlighted_field = None
                current_sequence_idx = 0
                # Stop timer
                pygame.time.set_timer(pygame.USEREVENT, 0)

        if event.type == pygame.MOUSEBUTTONDOWN and wait_for_input:
            check_for_input(pygame.mouse.get_pos())

        # Will be called after 1000ms (1sec) from check for input
        if event.type == FEEDBACK_EVENT:
            end_feedback()

        if event.type == NEW_ROUND_EVENT:
            # Add new field to sequence
            add_new_field_to_sequence()

            # Reset of the sequence index
            current_sequence_idx = 0

            # Set timer for show new field in the next sequence
            pygame.time.set_timer(pygame.USEREVENT, HIGHLIGHT_DURATION)

            # Stop timer for new round
            pygame.time.set_timer(NEW_ROUND_EVENT, 0)


    # Background colour
    window.fill(BLACK)

    # Draw grid
    grid()

    pygame.display.update()