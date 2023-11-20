
import pygame
import sys

# Initialize
pygame.init()

# Define pygame window props
width, height = 300, 300
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sequence lab!")

# Define colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def grid():
    # Size for each memory field
    blockSizeForField = 100
    # Go through the grid in horizontal (x) and vertical (y) axis
    for x in range(0, width, blockSizeForField):
        for y in range(0, height, blockSizeForField):
            # Create rectangle at position x, y (with size blockSize * blockSize)
            rectangle = pygame.Rect(x, y, blockSizeForField, blockSizeForField)
            # Create rectangle at window
            # width = 1: only the border is drawn
            pygame.draw.rect(window, WHITE, rectangle, 1)

# Loop
while True:
    # Close event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Background colour
    window.fill(BLACK)

    # Draw grid
    grid()

    pygame.display.update()