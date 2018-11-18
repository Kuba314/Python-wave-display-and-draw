import wave, struct, math
import pygame
from pygame.locals import *
import sys
import time

## draws a pixel bcuz pygame can't apparently do that
def pixel(surf, pos, color = (255, 255, 255)):
    pygame.draw.line(surf, color, pos, pos)

## clears whole column at specific x
def clear_vert(x):
    for y in range(HEIGHT):
        pixel(surf, (x, y), (0, 0, 0))

def setup():
    ## draws signal array(default is sine wave)
    for i in range(len(signal)):
        pixel(surf, (i, signal[i]))
    
## saves wave into file
def save():
    print 'Saving...'

    ## save pygame surface state to array
    pxarray = pygame.PixelArray(surf)
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if pxarray[x, y] == surf.map_rgb((255, 255, 255)):
                signal[x] = y
                continue

    
    sampleRate = 44100.0 # hertz - values/sec, default 44100
    volume = 32767.0

    ## setup the wave file
    wavef = wave.open('sound.wav','w')
    wavef.setnchannels(1) # mono
    wavef.setsampwidth(2) 
    wavef.setframerate(sampleRate)

##    trusignal = [0 for i in range(2*WIDTH)]
    
    ## how many samples to get into the file
    cycles = int(sampleRate)
    
    
    ## make it the right values - from (0 to WIDTH) to (-volume to volume)
    for i in range(len(signal)):
        signal[i] = (signal[i]/float(HEIGHT/2) - 1) * volume

    ## flip clone so \_ becomes \_^\ so the signal is fluent
    ## I don't even know why I did this. It's just there, not helping much
##    for i in range(len(trusignal)):
##        if i < WIDTH:
##            trusignal[i] = trusignal[i]
##        else:
##            trusignal[i] = -trusignal[2*WIDTH-i-1]

    ## put the signal into the file
    for i in range(cycles):
        data = struct.pack('<h', signal[i%WIDTH])
        wavef.writeframesraw(data)
    wavef.writeframes('')
    wavef.close()
    print 'saved'

## set up intro scene and dimensions
WIDTH = 800
HEIGHT = 450
pos = (-1, -1)

## set up pygame stuff
pygame.init()
pygame.mixer.init()
surf = pygame.display.set_mode((WIDTH, HEIGHT), 0, 8)
pygame.display.set_caption('Draw me!')

sound = pygame.mixer.Sound('sound.wav')
sound.set_volume(0.04)

## print intro signal is sine wave
## signal = [int(-math.sin(float(i)/WIDTH*3.1415965*2)*HEIGHT/4+HEIGHT/2) for i in range(WIDTH)]
signal = [int(-math.sin(float(i)/WIDTH*3.1415965*2)*HEIGHT/4+HEIGHT/2) for i in range(WIDTH)]
setup()

while True:

    ## handle SPACE press - play sound
    if pygame.key.get_pressed()[K_SPACE]:
        sound = pygame.mixer.Sound('sound.wav')
        sound.set_volume(0.02)
        sound.play()
    
    ## handle left click - drawing by clicking and making lines, new
    if pygame.mouse.get_pressed()[0]:
        if pos == (-1, -1):
            pos = pygame.mouse.get_pos()
        else:
            new_pos = pygame.mouse.get_pos()
            
            if pos[0] > new_pos[0]:
                for x in range(new_pos[0], pos[0]):
                    clear_vert(x)
            elif pos[0] == new_pos[0]:
                clear_vert(pos[0])
            else:
                for x in range(pos[0], new_pos[0]):
                    clear_vert(x)
            
            pygame.draw.line(surf, (255, 255, 255), pos, new_pos)
            pos = new_pos


    ## handle right click - save
    if pygame.mouse.get_pressed()[2]:
        save()

    ## handle middle click - exit
    if pygame.mouse.get_pressed()[1]:
        pygame.quit()
        sys.exit()
        
    ## handle normal exit through [X] button
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    ## update screen
    pygame.display.update()



