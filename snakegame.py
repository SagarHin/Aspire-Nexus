import pygame
import time
import random
import os

pygame.init()

# dimensions for screen
width = 800
height = 600

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)

# parameters
block_size = 20
speed = 15

font_style = pygame.font.SysFont(None, 50)
clock = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# store high score
high_score_file = "high_score.txt"

# Load high score from file (if exists)
if os.path.exists(high_score_file):
    with open(high_score_file, "r") as file:
        high_score = int(file.read())
else:
    high_score = 0

# Load image for the background 

background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (width, height))

def our_snake(block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, black, [x[0], x[1], block_size, block_size])

def message(msg, color, x, y):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [x, y])

def display_menu():
    """Displays the menu options for New Game, Resume, and Quit."""
    # Blit the background image instead of a solid blue color
    screen.blit(background_image, (0, 0))

    # Display the high score in the top-right corner
    message(f"High Score: {high_score}", white, width - 200, 20)

    # Display menu options
    message("New Game (N)", white, width / 6, height / 3 - 40)
    message("Resume Game (R)", white, width / 6, height / 3)
    message("Quit (Q)", white, width / 6, height / 3 + 40)

    pygame.display.update()

def save_high_score(score):
    """Save the highest score to a file."""
    global high_score
    if score > high_score:
        high_score = score
        with open(high_score_file, "w") as file:
            file.write(str(high_score))

def gameLoop(resume=False, prev_snake_list=None, prev_x=None, prev_y=None, prev_length=None):
    game_over = False
    game_close = False

    if resume and prev_snake_list:
        x1 = prev_x
        y1 = prev_y
        snake_list = prev_snake_list
        length_of_snake = prev_length
    else:
        x1 = width / 2
        y1 = height / 2
        snake_list = []
        length_of_snake = 1

    x1_change = 0
    y1_change = 0

    foodx = round(random.randrange(0, width - block_size) / block_size) * block_size
    foody = round(random.randrange(0, height - block_size) / block_size) * block_size

    score = length_of_snake - 1

    while not game_over:

        while game_close == True:
            screen.fill(white)
            message(f"You Lost! Score: {score} | High Score: {high_score}", red, width / 6, height / 3 - 40)
            message("Press C-Play Again or Q-Quit", red, width / 6, height / 3)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = block_size
                    x1_change = 0
                elif event.key == pygame.K_p:
                    # Pause the game and return current state
                    return snake_list, x1, y1, length_of_snake

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(white)
        pygame.draw.rect(screen, green, [foodx, foody, block_size, block_size])

        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(block_size, snake_list)

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - block_size) / block_size) * block_size
            foody = round(random.randrange(0, height - block_size) / block_size) * block_size
            length_of_snake += 1

        score = length_of_snake - 1
        save_high_score(score)

        pygame.display.update()
        clock.tick(speed)

    pygame.quit()
    quit()


# Main loop for the game
def main():
    resume_data = None

    while True:
        display_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:  # New game
                    gameLoop()
                elif event.key == pygame.K_r:  # Resume game
                    if resume_data:
                        gameLoop(True, *resume_data)
                elif event.key == pygame.K_q:  # Quit
                    pygame.quit()
                    quit()

        # Pausing and resuming the game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            resume_data = gameLoop(True)


if __name__ == "__main__":
    main()
