# Import the pygame, time, and random module
import pygame
import sys
import time
import random
from pygame.locals import *

# Initialize pygame
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1200

# Define colors
BLACK = ((0, 0, 0))
GRAY = ((127, 127, 127))
WHITE = ((255, 255, 255))
GREEN = ((0, 255, 0))
RED = ((255, 0, 0))

# Create the screen object, the size is determined by the game window dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()  # Initialize clock for framerate control

playerLives = 1  # Shreks lives
level = 1  # start at level 1
score_value = 0  # start with 0 score

# Define the font for the score and lives display
font = pygame.font.Font(None, 50)

pygame.display.set_caption("Shrek Game")


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    screen.fill(WHITE)
    largeText = pygame.font.Font('shrek_font.ttf', 115)
    TextSurf, TextRect = text_objects("Flying Swamp Ogre Game", largeText)
    TextRect.center = ((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(TextSurf, TextRect)

    mouse = pygame.mouse.get_pos()

    if 150 + 100 > mouse[0] > 150 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(screen, GREEN, (150, 450, 100, 50))
    else:
        pygame.draw.rect(screen, RED, (150, 450, 100, 50))

    smallText = pygame.font.Font("shrek_font.ttf", 20)
    textSurf, textRect = text_objects("Start", smallText)
    textRect.center = ()

    pygame.display.update()
    # clock.tick(30)


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "Resume":
                pass
            elif action == "Quit":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    smallText = pygame.font.Font("shrek_font.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    pygame.draw.rect(screen, GREEN, (150, 450, 100, 50))


def quitgame():
    pygame.quit()
    quit()


def unpause():
    global pause
    pause = False


def paused():
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(WHITE)
        largeText = pygame.font.Font('shrek_font.TTF', 115)
        TextSurf, TextRect = text_objects("Paused", largeText)
        TextRect.center = ((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.5))
        screen.blit(TextSurf, TextRect)
        button("Resume", 150, 450, 100, 50,
               ((0, 128, 0)), GREEN, unpause)
        button("Quit", 550, 450, 100, 50,
               ((128, 0, 0)), RED, quitgame)

        pygame.display.flip()  # same as pygame.display.update()
        # clock.tick(60)


def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('shrek_font.TTF', 215)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(TextSurf, TextRect)

    pygame.display.flip()
    time.sleep(2)


def show_score(playerLives):
    lifeText = pygame.font.Font('shrk_font.ttf', 64)
    TextSurf, TextRect = text_objects("Lives: " + str(playerLives), lifeText)
    TextRect.center = ((SCREEN_WIDTH - 1500, SCREEN_HEIGHT-10))
    screen.blit(TextSurf, TextRect)

    pygame.display.flip()

    score = font.render("Score : " + str(score_value),
                        True, WHITE)
    screen.blit(score, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Write the Lives-left to the right of the score
    lives = font.render("Lives : " + str(playerLives),
                        True, WHITE)
    screen.blit(lives, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 1150))

    '''while True:
        game_intro()
        for event in pygame.event.get():
            # show_score(score)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.flip()
        clock.tick(60)'''

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("flying_shrek_face.png").convert_alpha()
        # self.surf.set_colorkey(WHITE, RLEACCEL)
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect()

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
        self.surf.set_colorkey(BLACK, RLEACCEL)

        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(14, 20)

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
        self.surf.set_colorkey(WHITE, RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(8, 12)

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


ADDENEMY = pygame.USEREVENT + 3 * level
pygame.time.set_timer(ADDENEMY, 500)

ADDDRAGON = pygame.USEREVENT + 1 * level
pygame.time.set_timer(ADDDRAGON, 6500)

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
pygame.mixer.init()
pygame.mixer.music.load('allstar_background_music.ogg')
pygame.mixer.music.play(-1, 0.0)
# pygame.mixer.background_music.set_endevent(pygame.constants.USEREVENT)

# Sound Effects
player_dead_sound = pygame.mixer.Sound("it_all_ogre_now.mp3")
fart = pygame.mixer.Sound("shrek_fart.mp3")

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

    # game background image
    # screen.blit(255, 255, 255)
    screen.blit(background, (0, 0))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(player, enemies):
            # fart.play()
            playerLives -= 1  # minus 1 life

            if playerLives > 0:
                continue

            else:
                player_dead_sound.play()
                pygame.mixer.music.stop()
                message_display('Game Over')
                player.kill()
                time.sleep(2)
                pygame.quit()
                sys.exit()

    # Draw the player on the screen
    screen.blit(player.surf, player.rect)

    pygame.display.flip()  # Update the display

    # Ensure program maintains a rate of 60 frames per second
    clock.tick(60)
