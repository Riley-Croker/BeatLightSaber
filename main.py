#############
# imports
#############

import cv2
import pygame

from HandDetector import HandDetector
from saber import Saber
from shaft import Shaft

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
handIsOpen = False

#shaft and lightsaber (CHANGE COLOR LATER)
aShaft = Shaft(100,100,100,50)
aSaber = Saber(200,110,200,30,(255,0,0))

######################
## HELPER FUNCTIONS ##
######################

def mapToNewRange(val, inputMin, inputMax, outputMin, outputMax):
    return outputMin + ((outputMax - outputMin) / (inputMax - inputMin)) * (val - inputMin)

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
            if handDetector.landmarkDictionary[0][12][1] < handDetector.landmarkDictionary[0][9][1] :
                handIsOpen = True
            else:
                handIsOpen = False
            #rendering the saber and the shaft
            aShaft.render(WINDOW)
            if(not handIsOpen):
                aSaber.render(WINDOW)
        
            # updating the position of your shaft and saber based on your hand
            aShaft.updatePosition(WIDTH - mapToNewRange(handDetector.landmarkDictionary[0][9][0], 0, 640, 0, WIDTH), 
                                  mapToNewRange(handDetector.landmarkDictionary[0][9][1], 0, 480, 0, HEIGHT))
            # right Hand
            if handDetector.landmarkDictionary[0][4][0] < handDetector.landmarkDictionary[0][20][0] :
                aSaber.updatePosition(aShaft.x + aShaft.width, aShaft.y + ((aShaft.height-aSaber.height)/2))
            # left hand
            else:
                aSaber.updatePosition(aShaft.x - aSaber.width, aShaft.y + ((aShaft.height-aSaber.height)/2))

            
 
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



