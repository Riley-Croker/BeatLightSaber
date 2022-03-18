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
pygame.init()
WIDTH = 1100
HEIGHT = 650
# make the game window object
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
# name the game window
pygame.display.set_caption("Beat Light Saber")
# font for text
font = pygame.font.SysFont('Arial', 55)

#game stuff
FPS = 60

#shaft and lightsaber (CHANGE COLOR LATER)
aShaft = Shaft(100,100,100,50)
aSaber = Saber(200,110,200,30,(255,255,255))

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
    switchVal = 0
    handIsOpen = False

    # while the opencv window is running
    while (not handDetector.shouldClose) and gameIsRunning:
        WINDOW.fill((42,42,42))
        #FOR DA LIGHTSABER
        # update the webcam feed and hand tracker calculations
        handDetector.update()
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

        # FINITE STATE MACHINE
        # COLOR SWITCH SCREEN
        if switchVal == 0:
            #TEXT
            startMessage = "Choose your saber"
            start = font.render(startMessage, True, (0,0,0))
            WINDOW.blit(start, (350, 20))

            #RECTANGLES FOR COLOR
            redRect = pygame.Rect(150,150,100,100)
            pygame.draw.rect(WINDOW, (255,0,0), redRect)
            blueRect = pygame.Rect(500,150,100,100)
            pygame.draw.rect(WINDOW, (0,0,255), blueRect)
            greenRect = pygame.Rect(850,150,100,100)
            pygame.draw.rect(WINDOW, (0,255,0), greenRect)
            purpRect = pygame.Rect(150,400,100,100)
            pygame.draw.rect(WINDOW, (128,0,255), purpRect)
            whiteRect = pygame.Rect(500,400,100,100)
            pygame.draw.rect(WINDOW, (255,255,255), whiteRect)
            yellowRect = pygame.Rect(850,400,100,100)
            pygame.draw.rect(WINDOW, (255,255,0), yellowRect)

            if not handIsOpen:
                if aSaber.collisionRect(redRect):
                    switchVal = 1
                    aSaber.changeColor(255,0,0)
                if aSaber.collisionRect(blueRect):
                    switchVal = 1
                    aSaber.changeColor(0,0,255)
                if aSaber.collisionRect(greenRect):
                    switchVal = 1
                    aSaber.changeColor(0,255,0)
                if aSaber.collisionRect(purpRect):
                    switchVal = 1
                    aSaber.changeColor(128,0,255)
                if aSaber.collisionRect(whiteRect):
                    switchVal = 1
                    aSaber.changeColor(255,255,255)
                if aSaber.collisionRect(yellowRect):
                    switchVal = 1
                    aSaber.changeColor(255,255,0)
        # STARTSCREEN
        elif switchVal == 1:
            startRect = pygame.Rect(100,250,150,150)
            pygame.draw.rect(WINDOW, (0,0,0), startRect)
            instRect = pygame.Rect(900,250,150,150)
            pygame.draw.rect(WINDOW, (0,0,0), instRect)

            startMessage = "PLAY"
            instructMessage = "INFO"
            start = font.render(startMessage, True, (255,255,255))
            WINDOW.blit(start, (120, 290))

            instruct = font.render(instructMessage, True, (255,255,255))
            WINDOW.blit(instruct, (920, 290))

            if not handIsOpen:
                if aSaber.collisionRect(startRect):
                    switchVal = 3
                if aSaber.collisionRect(instRect):
                    switchVal = 2
        # INSTRUCTIONS
        elif switchVal == 2:
            # RENDERING ALL TEXT
            startMessage = "Welcome to BeatLightSaber!"
            start = font.render(startMessage, True, (0,0,0))
            WINDOW.blit(start, (50, 70))
            instructM1 = "In this game, your goal is to slice droids with your "
            instruct1 = font.render(instructM1, True, (0,0,0))
            WINDOW.blit(instruct1, (50, 150))
            instructM2 = "lightsaber and do not let them hit the bottom"
            instruct2 = font.render(instructM2, True, (0,0,0))
            WINDOW.blit(instruct2, (50, 200))
            instructM2 = "of the screen!"
            instruct2 = font.render(instructM2, True, (0,0,0))
            WINDOW.blit(instruct2, (50, 250))
            instructM3 = "Hold the lightsaber with either hand "
            instruct3 = font.render(instructM3, True, (0,0,0))
            WINDOW.blit(instruct3, (50, 350))
            instructM4 = "and get slicing!"
            instruct4 = font.render(instructM4, True, (0,0,0))
            WINDOW.blit(instruct4, (50, 400))

            backRect = pygame.Rect(900,450,150,150)
            pygame.draw.rect(WINDOW, (0,0,0), backRect)

            backMessage = "BACK"   
            back = font.render(backMessage, True, (255,255,255))
            WINDOW.blit(back, (910, 490))
            if not handIsOpen:
                if aSaber.collisionRect(backRect):
                    switchVal = 1        

        elif switchVal == 3:
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



