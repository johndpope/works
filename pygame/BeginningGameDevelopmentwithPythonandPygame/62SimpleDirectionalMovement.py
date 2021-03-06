# Listing 6-2. Simple Directional Movement
import pygame
from pygame.locals import *
from sys import exit
from gameobjects.vector2 import Vector2

# constants
screensize = screenwidth,screenheight = 640,480
bgimage = 'sushiplate.jpg'
spriteimage = 'fugu.png'
black = pygame.Color('black')
white = pygame.Color('white')
red = pygame.Color('red')
green = pygame.Color('green')
blue = pygame.Color('blue')
fps = 60
pos = Vector2(200,150)
speed = 60
 
# initialize pygame 
pygame.init()
screen = pygame.display.set_mode(screensize,0,32)
bgsurf = pygame.image.load(bgimage).convert()
spritesurf = pygame.image.load(spriteimage).convert_alpha()
# clock object
clock = pygame.time.Clock()

def getText(msg,color=blue,fontsize=18):
    font = pygame.font.SysFont('bitstreamveraserif',fontsize)
    textsurf = font.render(msg,True,color) # font.render(text,antialias,fg,bg)
    return textsurf


while True:
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit(); exit()

    screen.fill(white)
    # pressed keys
    pressedkeys = pygame.key.get_pressed()
    direction = Vector2(0,0)
    if pressedkeys[K_LEFT]: direction.x = -1
    elif pressedkeys[K_RIGHT]: direction.x = +1
    elif pressedkeys[K_UP]: direction.y = -1
    elif pressedkeys[K_DOWN]: direction.y = +1

    direction.normalize() # unit direction 
    screen.blit(bgsurf,(0,0))
    screen.blit(spritesurf, pos)

    timepassed = clock.tick(fps)/1000.0 # time passed(seconds) since last frame
    pos += timepassed * speed * direction
    pygame.display.update()
