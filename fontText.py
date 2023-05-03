import pygame
import sys
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((1600, 800))
pygame.display.set_caption('Hello World!')

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)

fontObj = pygame.font.Font('shrek_font.TTF', 142)
textSurfaceObj = fontObj.render('Ogre Game', True, ((0, 80, 0)))
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (800, 150)

# Loading and playing a sound effect:
soundObj = pygame.mixer.Sound('shrek_fart.mp3')
soundObj.play()
pygame.mixer.init()
pygame.mixer.music.load('allstar_background_music.ogg')
pygame.mixer.music.play(-1, 0.0)


while True:  # main game loop
    background = pygame.image.load("shrek_background.png").convert()
    DISPLAYSURF.blit(background, (0, 0))
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    # Loading and playing background music:
    # ...some more of your code goes here...

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
