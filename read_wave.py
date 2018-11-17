import struct
import pygame
from pygame.locals import *
import sys
from scipy.io import wavfile

#######################################################################
## .                       .                        .
##   .                 .       .                 .
##    .              .          .           .
##     .           .              .      .
##       .       .                  .  .
##           .
#######################################################################
##         WAVE FILE ANALYSIS, it's bad

## draw pixel, bcuz pygame can't apparently do that
def pixel(pos, color = (255, 255, 255)):
    pygame.draw.line(surf, color, pos, pos)

## set up pygame stuff
WIDTH = 1600
HEIGHT = 540
pygame.init()
surf = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('.wav analysis tool')

## read data from file
FILENAME = 'sound.wav'
fs, data = wavfile.read(FILENAME)

## translate data to fit onto the screen
for i in range(len(data)):
    actually = int(data[i]/32767.0*HEIGHT/2) + HEIGHT/2
    pixel((i, actually))
    
print 'File loaded, length: ', len(data)

while True:

    ## handle right click - reload
    if pygame.mouse.get_pressed()[2]:
        fs, data = wavfile.read(FILENAME)
        surf = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        for i in range(len(data)):
            actually = int(data[i]/32767.0*HEIGHT/2) + HEIGHT/2
            pixel((i, actually))
    
        print 'File re-loaded, length: ', len(data)

    ## handle middle click - exit
    if pygame.mouse.get_pressed()[1]:
        pygame.quit()
        sys.exit()

    ## handle normal exit - [X] pressed
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    ## update screen
    pygame.display.update()
