import pygame
from math import sqrt
from random import randint
import time


pygame.init()


HEIGHT = 600
WIDTH = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Ariel Black', 50)
end_font = pygame.font.SysFont('Ariel White', 90)
endX, endY = 240, 250

# Player variables
mouseX = 0
mouseY = 0
mouseR = 40

# Load background images
background = pygame.image.load('images/sky.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

end_background = pygame.image.load('images/sky.jpg')
end_background = pygame.transform.scale(end_background, (WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# ---------------------------------------
# picture properties
# ---------------------------------------

# Balloon images
balloon_images = [
    'images/blue.png',
    'images/bronze.png',
    'images/gold.png',
    'images/green.png',
    'images/hot_pink.png',
    'images/orange.png',
]

# Load and resize balloon images
balloon_images = [pygame.image.load(img) for img in balloon_images]

# Load and scale bomb image
bomb_image = pygame.transform.scale(pygame.image.load('images/evil_balloon.png'), (60, 120))


# -------------------------------------------------
# function that calculates distance between
# two points in coordinate system
# -------------------------------------------------
def distance(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# -------------------------------------------------
# function that redraws all objects
# -------------------------------------------------
def redraw():
    screen.blit(background, (0, 0))
    for i in range(len(balloons)):
        if balloons_visible[i]:
            if balloon_shapes[i] == -1:
                # Adjust to center bomb
                screen.blit(bomb_image, (balloon_x[i] - 30, balloon_y[i] - 60))
            else:
                resizedBalloon = pygame.transform.scale(
                    balloon_images[balloon_shapes[i]],
                    (balloon_r[i] * 2, balloon_r[i] * 3),
                )

                # Adjust to center balloon
                screen.blit(
                    resizedBalloon,
                    (balloon_x[i] - balloon_r[i], balloon_y[i] - balloon_r[i] * 1.5),
                )

    # Display score and elapsed time
    score_text = font.render('Score: ' + str(score), True, BLACK)
    screen.blit(score_text, (10, 5))
    elapsed_time = int(time.time() - start_time)
    time_text = font.render('Time: ' + str(elapsed_time), True, BLACK)
    screen.blit(time_text, (10, 60))

    pygame.display.update()


# Function to display the game over screen
def game_over():
    final_time = int(time.time() - start_time)
    screen.blit(end_background, (0, 0))
    end_text = end_font.render('GAME OVER', True, BLACK)
    screen.blit(end_text, (225, 170))
    scoreText = font.render('Score: ' + str(score), True, BLACK)
    screen.blit(scoreText, (333, 250))
    timeText = font.render('Final Time: ' + str(final_time), True, BLACK)
    screen.blit(timeText, (320, 465))
    missedText = font.render('Missed balloons: ' + str(missed_balloons), True, BLACK)
    screen.blit(missedText, (260, 410))

    # Draw play again button
    pygame.draw.rect(screen, GREEN, (200, 300, 200, 100))
    playText = font.render('REPLAY', True, BLACK)
    screen.blit(playText, (230, 330))

    # Draw quit button
    pygame.draw.rect(screen, RED, (450, 300, 200, 100))
    quitText = font.render('QUIT', True, BLACK)
    screen.blit(quitText, (500, 330))

    pygame.display.update()


# Function to generate balloons
def gen_balloons():
    numBalloons = randint(20, 30)
    for i in range(numBalloons):
        balloons.append(randint(0, WIDTH))
        balloons_visible.append(True)
        balloon_x.append(randint(0, WIDTH - 60))
        balloon_y.append(randint(HEIGHT // 2, HEIGHT))
        balloon_r.append(randint(20, 50))
        balloon_speed.append(randint(1, 5))
        balloon_shapes.append(randint(0, len(balloon_images) - 1))

    # Adding a black balloon (bomb)
    balloons.append(randint(0, WIDTH - 60))
    balloons_visible.append(True)
    balloon_x.append(randint(0, WIDTH - 60))
    balloon_y.append(randint(HEIGHT // 2, HEIGHT))
    balloon_r.append(30)
    balloon_speed.append(randint(1, 5))
    balloon_shapes.append(-1)


# ---------------------------------------#
#   Main
# ---------------------------------------#


exit_flag = False
game_on = True
play_again = False
score = 0
missed_balloons = 0
balloons = []
balloons_visible = []
balloon_x = []
balloon_y = []
balloon_r = []
balloon_speed = []
balloon_shapes = []
gen_balloons()
start_time = time.time()

# Main game loop
while game_on:
    if not exit_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_flag = True
                game_on = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                (cursorX, cursorY) = pygame.mouse.get_pos()

                if not any(balloons_visible):  # If all balloons are popped or flown away
                    if 200 < cursorX < 400 and 300 < cursorY < 400:
                        play_again = True
                    if 450 < cursorX < 650 and 300 < cursorY < 400:
                        exit_flag = True
                        game_on = False

                for i in range(len(balloons)):
                    if balloons_visible[i] and distance(cursorX, cursorY, balloon_x[i], balloon_y[i]) < balloon_r[i]:
                        if balloon_shapes[i] == -1:
                            game_over()
                            exit_flag = True
                        else:
                            balloons_visible[i] = False
                            score += 1

        for i in range(len(balloons)):
            if balloons_visible[i]:
                balloon_y[i] -= balloon_speed[i]
                if balloon_y[i] < -balloon_r[i]:  # Ensure balloons stay on screen
                    balloons_visible[i] = False
                    missed_balloons += 1

        if not any(balloons_visible):
            game_over()
            exit_flag = True

        if play_again:
            balloons = []
            balloons_visible = []
            balloon_x = []
            balloon_y = []
            balloon_r = []
            balloon_speed = []
            balloon_shapes = []
            score = 0
            missed_balloons = 0
            gen_balloons()
            exit_flag = False
            play_again = False
            start_time = time.time()

        redraw()
        clock.tick(30)

    elif exit_flag:
        game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                (cursorX, cursorY) = pygame.mouse.get_pos()
                if 200 < cursorX < 400 and 300 < cursorY < 400:
                    play_again = True
                    exit_flag = False
                elif 450 < cursorX < 650 and 300 < cursorY < 400:
                    game_on = False

pygame.quit()
pygame.display.quit()
