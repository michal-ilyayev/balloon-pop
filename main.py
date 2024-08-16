import pathlib
import pygame
import random
import time
from math import sqrt


pygame.init()

HEIGHT = 600
WIDTH = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial Black', 36)  # Smaller font size for gameplay
end_font = pygame.font.SysFont('Arial Black', 60)  # Smaller font size for game over screen

# ---------------------------------------
# Colors
# ---------------------------------------

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# ---------------------------------------
# picture properties
# ---------------------------------------

CWD = pathlib.Path(__file__).parent

# Balloon images
balloon_image_files = [
    CWD / 'images/blue.png',
    CWD / 'images/bronze.png',
    CWD / 'images/gold.png',
    CWD / 'images/green.png',
    CWD / 'images/hot_pink.png',
    CWD / 'images/orange.png',
]
balloon_images = [pygame.image.load(img) for img in balloon_image_files]

# Load and scale bomb image
bomb_image_file_name = pygame.image.load(CWD / 'images/evil_balloon.png')
bomb_image = pygame.transform.scale(bomb_image_file_name, (60, 120))

# Load background images
background_file_name = pygame.image.load(CWD / 'images/sky.jpg')
background = pygame.transform.scale(background_file_name, (WIDTH, HEIGHT))
end_background_file_name = pygame.image.load(CWD / 'images/sky.jpg')
end_background = pygame.transform.scale(end_background_file_name, (WIDTH, HEIGHT))


# ---------------------------------------
# functions
# ---------------------------------------


def distance(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# ---------------------------------------
# game components
# ---------------------------------------


class Balloon:
    """
    Represents a balloon in the game.

    Attributes:
        x (int): The x-coordinate of the balloon.
        y (int): The y-coordinate of the balloon.
        image (Surface): The image of the balloon.
        speed (int): The speed at which the balloon moves upwards.
        size (int): The size of the balloon.
        is_bomb (bool): Whether the balloon is a bomb.
    """

    def __init__(self, x, y, image, speed, size, is_bomb=False):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(image, (size, size * 2))
        self.speed = speed
        self.visible = True
        self.is_bomb = is_bomb
        self.size = size

    def __str__(self):
        return 'Balloon at ', {self.x}, {self.y}

    def draw_balloon(self):
        if self.visible:
            screen.blit(self.image, (self.x, self.y))

    def fly_away(self):
        if self.visible:
            self.y -= self.speed
            if self.y < -self.size * 2:
                self.visible = False
                return not self.is_bomb
        return False

    def pop(self, mouse_x, mouse_y):
        if self.visible and distance(self.x + self.size // 2, self.y + self.size, mouse_x, mouse_y) < self.size:
            self.visible = False
            return True, not self.is_bomb
        return False, False


class Bomb(Balloon):
    """
    Represents a bomb balloon in the game, inheriting from Balloon.

    """

    def __init__(self, x, y, image, speed, size, is_bomb=True):
        super().__init__(x, y, image, speed, size, is_bomb)

    def pop(self, mouse_x, mouse_y):
        """
        Override pop method for bomb behavior.
        Returns True to end the game if popped.
        """
        if self.visible and distance(self.x + self.size // 2, self.y + self.size, mouse_x, mouse_y) < self.size:
            self.visible = False
            return True
        return False


class Game:
    """
    Manages the game state and logic.

    Attributes:
        balloons (list): List of Balloon objects in the game.
        score (int): Player's score.
        missed (int): Number of balloons that flew away.
        num_balloons (int): Total number of balloons generated in the game.
    """

    def __init__(self):
        self.balloons = []
        self.score = 0
        self.missed = 0
        self.num_balloons = random.randint(20, 40)
        self.generate_balloons()

    def generate_balloons(self):
        for i in range(self.num_balloons):
            image = random.choice(balloon_images)
            x = random.randint(0, WIDTH - 60)
            y = random.randint(HEIGHT // 2, HEIGHT)
            speed = random.randint(1, 5)
            size = random.randint(30, 60)
            self.balloons.append(Balloon(x, y, image, speed, size))
        # Add a bomb balloon
        x = random.randint(0, WIDTH - 60)
        y = random.randint(HEIGHT // 2, HEIGHT)
        speed = random.randint(1, 5)
        size = random.randint(30, 60)
        self.balloons.append(Bomb(x, y, bomb_image, speed, size, is_bomb=True))

    def draw_all(self):
        for balloon in self.balloons:
            balloon.draw_balloon()
        score_text = font.render('Score: ' + str(self.score), True, BLACK)
        missed_text = font.render('Missed: ' + str(self.missed), True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(missed_text, (10, 60))

    def move_all(self):
        for balloon in self.balloons:
            if balloon.fly_away():
                self.missed += 1

    def pop_all(self, mouse_x, mouse_y):
        for balloon in self.balloons:
            if isinstance(balloon, Bomb):
                popped = balloon.pop(mouse_x, mouse_y)
                if popped:
                    return False
            else:
                popped, is_safe = balloon.pop(mouse_x, mouse_y)
                if popped:
                    if balloon.is_bomb:
                        return False
                    else:
                        self.score += 1
        return True


class GameLoop:
    """
    Manages the main game loop and handles events.

    Attributes:
        game (Game): The current game instance.
        start_time (float): The time when the game started.
        running (bool): Whether the game loop is running.
        game_over (bool): Whether the game is over.
        final_time (int): Final time when the game ends.
    """

    def __init__(self):
        self.game = Game()
        self.start_time = time.time()
        self.running = True
        self.game_over = False
        self.final_time = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if not self.game.pop_all(mouseX, mouseY):
                    self.game_over = True
                    self.final_time = int(time.time() - self.start_time)

    def update(self):
        self.game.move_all()
        if all(not balloon.visible for balloon in self.game.balloons):
            self.game_over = True
            self.final_time = int(time.time() - self.start_time)

    def render(self):
        screen.blit(background, (0, 0))
        self.game.draw_all()
        pygame.display.update()

    def game_over_screen(self):
        screen.blit(end_background, (0, 0))
        end_text = end_font.render('GAME OVER', True, BLACK)
        screen.blit(end_text, (225, 170))
        scoreText = font.render('Score: ' + str(self.game.score), True, BLACK)
        screen.blit(scoreText, (330, 250))
        time_text = font.render('Time: ' + str(self.final_time) + 's', True, BLACK)
        screen.blit(time_text, (320, 465))
        missed_text = font.render('Missed: ' + str(self.game.missed), True, BLACK)
        screen.blit(missed_text, (310, 410))

        # Draw play again button
        pygame.draw.rect(screen, GREEN, (200, 300, 200, 100))
        play_text = font.render('REPLAY', True, BLACK)
        screen.blit(play_text, (230, 330))

        # Draw quit button
        pygame.draw.rect(screen, RED, (450, 300, 200, 100))
        quit_text = font.render('QUIT', True, BLACK)
        screen.blit(quit_text, (500, 330))

        pygame.display.update()

    def handle_game_over_events(self):  # Corrected method name
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 200 < mouse_x < 400 and 300 < mouse_y < 400:  # REPLAY button
                    self.game = Game()
                    self.start_time = time.time()
                    self.game_over = False
                elif 450 < mouse_x < 650 and 300 < mouse_y < 400:  # QUIT button
                    self.running = False

    def run(self):
        while self.running:
            if not self.game_over:
                self.handle_events()
                self.update()
                self.render()
                clock.tick(30)
            else:
                self.game_over_screen()
                self.handle_game_over_events()

        pygame.quit()


if __name__ == '__main__':
    game_loop = GameLoop()
    game_loop.run()
