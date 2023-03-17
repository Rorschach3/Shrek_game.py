# Import the pygame, time, and random module
import pygame
import time
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1200

# Define colors
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)

# Initialize pygame
pygame.init()

# Create the screen object, the size is determined by the game window dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()  # Initialize clock for framerate control

playerLives = 5  # Shreks lives
level = 1  # start at level 1
score_value = 0  # start with 0 score


# Define the font for the score and lives display
font = pygame.font.Font(None, 36)

caption = 'Shrek Pygame'
pygame.display.set_caption(caption)

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("flying_shrek_face.png").convert_alpha()
        # self.surf.set_colorkey(WHITE, RLEACCEL)
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

        self.lives = 5

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("onion.png").convert_alpha()
        # self.surf.set_colorkey(WHITE)
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(10, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Define the dragon object by extending pygame.sprite.Sprite
# Use an image for a better-looking sprite
class Dragon(pygame.sprite.Sprite):
    def __init__(self):
        super(Dragon, self).__init__()

        # load the image
        self.surf = pygame.image.load("dragon.png").convert_alpha()
        # self.surf.set_colorkey(WHITE, RLEACCEL)
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 16)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


def generate_enemies(level):
    num_enemies = level * 5  # increase number of enemies by 5 for each level
    enemies = []
    for i in range(num_enemies):
        enemy = Enemy()  # create a new instance of the Enemy class
        enemies.append(enemy)
    return enemies


def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(TextSurf, TextRect)

    pygame.display.flip()

    time.sleep(2)

# Show lives left on the screen


def show_score(x, y):
    score = font.render("Score : " + str(score_value),
                        True, (255, 255, 255))
    screen.blit(score, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Write the Lives-left to the right of the score
    lives = font.render("Lives : " + str(playerLives),
                        True, (255, 255, 255))
    screen.blit(lives, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))

    while True:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.flip()
        clock.tick(30)


ADDENEMY = pygame.USEREVENT + 3
pygame.time.set_timer(ADDENEMY, 500)

ADDDRAGON = pygame.USEREVENT + 1
pygame.time.set_timer(ADDDRAGON, 6000)

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
dragons = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# variable created to reference the background music
background_music = pygame.mixer.music.load('allstar_background_music.ogg')
background_music = pygame.mixer.Sound("allstar_background_music.ogg")
background_music.play()

# pygame.mixer.background_music.set_endevent(pygame.constants.USEREVENT)

# Sound Effects
player_dead_sound = pygame.mixer.Sound("it_all_ogre_now.mp3")
fart = pygame.mixer.Sound("shrek_fart.mp3")


pygame.mixer.music.load("it_all_ogre_now.mp3")
# Variable to keep the main loop running
running = True

# background image
background = pygame.image.load("shrek_background.png").convert()

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():

        if event.type == KEYDOWN:  # Check for KEYDOWN event

            if event.key == K_ESCAPE:  # If the Esc key is pressed, then exit the main loop

                running = False

        elif event.type == QUIT:  # Check for QUIT event. If QUIT, then set running to false
            running = False

        if event.type == ADDENEMY:  # Add a new enemy?
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        if event.type == ADDDRAGON:  # create a new dragon and add it to sprite groups
            new_dragon = Dragon()
            dragons.add(new_dragon)
            all_sprites.add(new_dragon)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Update the position of enemies and dragons
    enemies.update()
    dragons.update()

    # game backgrounscreend image
    screen.blit(background, (0, 0))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
        print(event)
        if pygame.sprite.spritecollideany(player, enemies):
            fart.play()
            player.kill()
            playerLives -= 1  # if onion hits shrek, minus 1 life
            # if so, then play sound
            background_music.stop()
            time.sleep(2)

            if playerLives > 0:
                continue

            else:
                player_dead_sound.play()
                message_display('Game Over')
                player_dead_sound.stop()
                pygame.quit()
                quit()

        # Draw the player on the screen
        screen.blit(player.surf, player.rect)

    pygame.display.flip()  # Update the display

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(60)
