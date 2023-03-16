# Import the pygame module
import pygame

# import random for random numbers
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

playerLives = 5 #Shreks lives
level = 1 # start at level 1


# Define the font for the score and lives display
font = pygame.font.Font(None, 36)


caption = 'Shrek pygame'
pygame.display.set_caption(caption)

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("flying_shrek_face.png").convert_alpha()
        ### self.surf.set_colorkey(WHITE, RLEACCEL)
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
            
    def lose_life(self):
        self.lives -= 1



# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("onion.png").convert_alpha()
        ### self.surf.set_colorkey(WHITE)
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(9, 20)

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
        ### self.surf.set_colorkey(WHITE, RLEACCEL)
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the dragon based on a constant speed
    # Remove the dragon when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


    def generate_enemies(level):
        num_enemies = level * 5  # increase number of enemies by 5 for each level
        enemies = []
        for i in range(level):
            enemy = Enemy()  # create a new instance of the Enemy class
            enemies.append(enemy)
        return enemies

    # Show lives left on the screen
    def show_score(x, y):
        score = font.render("Score : " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))
        # Write the Lives-left to the right of the score
        lives = font.render("Lives : " + str(playerLives), True, (255, 255, 255))
        screen.blit(lives, (x+200, y))


# Initialize pygame
pygame.init()


# Setup clock for framerate control
clock = pygame.time.Clock()
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 2
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
background_music = pygame.mixer.Sound("allstar_background_music.ogg")
player_dead_sound = pygame.mixer.Sound("it_all_ogre_now.mp3")

#Background music
pygame.mixer.music.load('allstar_background_music.ogg')
pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
pygame.mixer.music.play(loops=-1)

# Variable to keep the main loop running
running = True

# background image
background = pygame.image.load("shrek_background.png").convert()

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False

        # Add a new enemy?
        '''for enemy in enemies:
            enemy.update()
            enemy.draw(screen)'''
        
           # Add a new enemy?
        if event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # a new Dragon?
        if event.type == ADDDRAGON:
            # Create the new draon and add it to sprite groups
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
    screen.blit(background, (0, 0))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    while pygame.sprite.spritecollideany(player, enemies) and playerLives > 0:
        
        playerLives -= 1 # if onion hits shrek, minus 1 life
        
        if playerLives <= 0: # if lives get to zero statement
        
            # If so, then remove the player and stop the loop
            player.kill()

            # if so, then play sound
            player_dead_sound.play()
            
            running = False
        
    # Draw the player on the screen
    screen.blit(player.surf, player.rect)

    # Update the display
    pygame.display.flip()
    
    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)