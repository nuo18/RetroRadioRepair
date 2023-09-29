import pygame
import sys
import time

# Function to initialize a new level
def init_level(level_number):
    # Load image paths and set up other level-specific data
    block_image_paths = levels[level_number]["image_paths"]
    block_images = [[pygame.image.load(path) for path in col] for col in zip(*block_image_paths)]
    block_images = [[pygame.transform.scale(image, (GRID_WIDTH, GRID_HEIGHT)) for image in row] for row in block_images]

    return block_images

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
GRID_SIZE = 4
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
GRID_COLOR = (0, 0, 0)
RECTANGLE_COLOR = (128, 128, 128)

# Define levels with image paths
levels = [
    {"image_paths": [
        ["b.png", "R1.png", "R3.png", "R3.png"],
        ["0.png", "R2.png", "R2.png", "R1.png"],
        ["R1.png", "R3.png", "0.png", "0.png"],
        ["R2.png", "R2.png", "R1.png", "L0.png"],
    ]},
    # Add more levels here with their image paths
    {"image_paths": [
        ["b.png", "0.png", "0.png", "B1.png"],
        ["B2.png", "B1.png", "B3.png", "0.png"],
        ["B1.png", "B2.png", "B3.png", "B1.png"],
        ["0.png", "B3.png", "B1.png", "L0.png"],
    ]},
    # Level 3
    {"image_paths": [
        ["b.png", "R3.png", "0.png", "B1.png"],
        ["B2.png", "R2.png", "R2.png", "R2.png"],
        ["R3.png", "B3.png", "R3.png", "R1.png"],
        ["R2.png", "R3.png", "R2.png", "L0.png"],
    ]},
]

# Initialize rotation angles for each block
angles = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Retro Radio Repair")

# Load the start menu image
start_menu_image = pygame.image.load("start_menu.png")
start_menu_image = pygame.transform.scale(start_menu_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load the game over image
game_over_image = pygame.image.load("game_over.png")
game_over_image = pygame.transform.scale(game_over_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Calculate block positions
block_positions = [(x * GRID_WIDTH, y * GRID_HEIGHT) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]

# Flag to indicate if the game has started
game_started = False

# Flag to indicate if the user has won
user_won = False

# Current level
current_level = 0

# Variables to control displaying images
display_sad_bob = False
display_happy_bob = False

# Import images
sad_bob_image = pygame.image.load("sadbob.png")
happy_bob_image = pygame.image.load("happybob.png")

# Scale the images to fit the screen
sad_bob_image = pygame.transform.scale(sad_bob_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
happy_bob_image = pygame.transform.scale(happy_bob_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for mouse click events
        if not game_started and event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click occurred within the start menu area
            if pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT).collidepoint(event.pos):
                game_started = True

        if game_started and not user_won:
            # Check for mouse click events during the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, (x, y) in enumerate(block_positions):
                    block_rect = pygame.Rect(x, y, GRID_WIDTH, GRID_HEIGHT)
                    if block_rect.collidepoint(event.pos):
                        # Rotate the clicked block by 90 degrees
                        angles[i // GRID_SIZE][i % GRID_SIZE] += 90
                        if angles[i // GRID_SIZE][i % GRID_SIZE] >= 360:
                            angles[i // GRID_SIZE][i % GRID_SIZE] = 0

    # Clear the screen
    screen.fill(GRID_COLOR)

    # Load the current level's block images
    block_images = init_level(current_level)

    # Display the start menu if the game hasn't started yet
    if not game_started:
        screen.blit(start_menu_image, (0, 0))
    else:
        # Draw the grid
        for x in range(0, SCREEN_WIDTH, GRID_WIDTH):
            pygame.draw.line(screen, RECTANGLE_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_HEIGHT):
            pygame.draw.line(screen, RECTANGLE_COLOR, (0, y), (SCREEN_WIDTH, y))

        # Draw the rotated blocks
        for i, (x, y) in enumerate(block_positions):
            block_rect = pygame.Rect(x, y, GRID_WIDTH, GRID_HEIGHT)
            block_image_rotated = pygame.transform.rotate(
                block_images[i // GRID_SIZE][i % GRID_SIZE], angles[i // GRID_SIZE][i % GRID_SIZE]
            )
            screen.blit(block_image_rotated, block_rect.topleft)

        # Store the angles for each block in a 2D array
        angle_array = [[angles[i // GRID_SIZE][i % GRID_SIZE] for i in range(GRID_SIZE * GRID_SIZE)] for _ in range(GRID_SIZE)]

        # Checking if user finished the game
        win = False

        # Flatten angle_array and store its elements in storage
        storage = []
        for row in angle_array:
            for angle in row:
                storage.append(angle)

        # For debugging
        print(storage)

        # Check if the user has won the game for the current level
        # You can add win conditions for levels 2 and 3 here
        if current_level == 0:
            if (
                storage[8] in (90, 180)
                and storage[6] in (90, 270)
                and storage[4] in (0, 180)
                and storage[11] in (0, 180)
                and storage[9] == storage[11] == 0
                and storage[5] == 180
                and storage[0] == storage[7] == storage[15] == 270
            ):
                user_won = True
        elif current_level == 1:
                        # Add win conditions for level 2 here
            if (
                storage[0] == storage[6] == 180
                and storage[1] == storage[15] == 270
                and storage[5] in (0, 180)
                and storage[7] in (0, 270)
                and storage[9] in (90, 180)
                and storage[10] in (0, 90)
                and storage[11] in (0, 180)
            ):
                user_won = True
        elif current_level == 2:
            # Add win conditions for level 3 here
            if (
                storage[0] == storage[5] == storage[11] == storage[15] == 270
                and storage[4] in (90, 180)
                and storage[10] in (90, 270)
                and storage[9] == 90
            ):
                user_won = True

    # Display the game over image if the user has won
    if user_won:
        pygame.display.flip()
        time.sleep(0.5)
        x = 3 * GRID_WIDTH
        y = 3 * GRID_HEIGHT

        l1_image = pygame.image.load("L1.png")
        l1_image = pygame.transform.scale(l1_image, (GRID_WIDTH, GRID_HEIGHT))

        l1_image_rotated = pygame.transform.rotate(l1_image, storage[15])  # Rotate the new image
        screen.blit(l1_image_rotated, (x, y))  # Display the rotated image

        pygame.display.flip()  # Update the screen to display the L1.png image
        time.sleep(2)  # Add a longer delay to keep the L1.png image visible

        # Check if there are more levels to go to
        if current_level < len(levels) - 1:
            # Move to the next level
            current_level += 1
            # Reset game state for the new level
            user_won = False
            angles = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

            # Display sadbob.png for 2 seconds
            display_sad_bob = True
            pygame.display.flip()
            time.sleep(2)
            display_sad_bob = False
        else:
            # All levels completed, display game over screen
            screen.blit(game_over_image, (0, 0))
            pygame.display.flip()
            running = False

    # Display sadbob.png or happybob.png depending on the level
    if current_level < len(levels) - 1:
        if display_sad_bob:
            screen.blit(sad_bob_image, (0, 0))
    else:
        # Display happybob.png for level 3
        if display_happy_bob:
            screen.blit(happy_bob_image, (0, 0))

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
