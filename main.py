#############
# imports
#############

import cv2
from cv2 import circle
import pygame
import random

from HandDetector import HandDetector

#############
## GLOBALS ##
#############

# Define the size of the game window
WIDTH = 1100
HEIGHT = 650
# make the game window object
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
# name the game window
pygame.display.set_caption("Beat Light Saber")

#game stuff
FPS = 60

######################
## HELPER FUNCTIONS ##
######################


###################
## MAIN FUNCTION ##
###################

def main():
    # make a hand detector
    handDetector = HandDetector()

    gameIsRunning  = True

    # while the opencv window is running
    while (not handDetector.shouldClose) and gameIsRunning:
        # update the webcam feed and hand tracker calculations
        handDetector.update()

        WINDOW.fill((42,42,42))
        
        # if there is at least one hand seen
        if len(handDetector.landmarkDictionary) > 0: 
            pass
        
 
        # for all the game events
        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                gameIsRunning = False

        # put code here that should be run every frame of your game             
        pygame.display.update()

        
    # Closes all the frames
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()



