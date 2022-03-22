#############
# imports
#############

import cv2
import numpy
import pygame
import random
from HandDetector import HandDetector
from droid import Droid
from saber import Saber
from shaft import Shaft

############
## IMAGES ##
############

saberScreen = pygame.image.load('Assets\SaberScreen.jpg')
saberScreen = pygame.transform.scale(saberScreen, (1100, 650))
menuScreen = pygame.image.load('Assets\MenuScreen.jpg')
menuScreen = pygame.transform.scale(menuScreen, (1100, 650))
level1Screen = pygame.image.load('Assets\Level1Screen.jpg')
level1Screen = pygame.transform.scale(level1Screen, (1100, 650))
level2Screen = pygame.image.load('Assets\Level2Screen.jpg')
level2Screen = pygame.transform.scale(level2Screen, (1100, 650))
level3Screen = pygame.image.load('Assets\Level3Screen.jpg')
level3Screen = pygame.transform.scale(level3Screen, (1100, 650))
level4Screen = pygame.image.load('Assets\Level4Screen.jpg')
level4Screen = pygame.transform.scale(level4Screen, (1100, 650))
vaderScreen = pygame.image.load('Assets\VaderScreen.jpg')
vaderScreen = pygame.transform.scale(vaderScreen, (1100, 650))
winScreen = pygame.image.load('Assets\WinScreen.jpg')
winScreen = pygame.transform.scale(winScreen, (1100, 650))
loseScreen = pygame.image.load('Assets\LoseScreen.jpg')
loseScreen = pygame.transform.scale(loseScreen, (1100, 650))


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

# ENEMY LIST
enemyTypeList = ["base", "battle", "droideka"]
droidList = []
maxSpeed = 4

#shaft and lightsaber (CHANGE COLOR LATER)
aShaft = Shaft(100,100,100,50)
aSaber = Saber(200,110,200,30,(255,255,255))

######################
## HELPER FUNCTIONS ##
######################

def mapToNewRange(val, inputMin, inputMax, outputMin, outputMax):
    return outputMin + ((outputMax - outputMin) / (inputMax - inputMin)) * (val - inputMin)

#Fills the enemylist with a number of enemies
def fillDroidList(num, maxSpeed):
    droidList.clear()
    for i in range(num):
        xPos = (random.randrange(0, 1000, 50))
        yPos = (random.randrange(-1000, -100, 25))
        enemyType = (random.choice(enemyTypeList))
        enemySpeed = random.randrange(2,maxSpeed)
        droid = Droid( xPos, yPos, enemyType, enemySpeed )
        droidList.append(droid)


#Renders and moves to the left side of the sceen 
def animateDroid():
    for droid in droidList:
        droid.render(WINDOW, droid.type)
        droid.moveDroid()
        droid.updateHitbox()

#Checks if any droids have hit the bottom
def checkDroidFinish():
    for droid in droidList:
        if(droid.bottom >= 650):
            return True
    return False

#check droid collision
def droidCollision():
    for droid in droidList:
        if(aSaber.collisionRect(droid.hitbox)):
            droidList.remove(droid)
    

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
        #For Backgrounds:
        if switchVal == 0:
            WINDOW.blit(saberScreen, (0,0))
        elif switchVal == 1 or switchVal == 2:
            WINDOW.blit(menuScreen, (0,0))
        elif switchVal == 3:
            WINDOW.blit(level1Screen, (0,0))
        elif switchVal == 4:
            WINDOW.blit(level2Screen, (0,0))
        elif switchVal == 5:
            WINDOW.blit(level3Screen, (0,0))
        elif switchVal == 6:
            WINDOW.blit(level4Screen, (0,0))
        elif switchVal == 7:
            WINDOW.blit(vaderScreen, (0,0))
        elif switchVal == 8:
            WINDOW.blit(winScreen, (0,0))
        elif switchVal == 99:
            WINDOW.blit(loseScreen, (0,0))
        
        

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

            #rotation
            # changeInX = abs(handDetector.landmarkDictionary[0][3][0] - handDetector.landmarkDictionary[0][17][0])
            # changeInY = abs(handDetector.landmarkDictionary[0][3][1] - handDetector.landmarkDictionary[0][17][1])
            # theta = numpy.arcsin((changeInY/changeInX))
            # aShaft.rotate(theta)

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
                    fillDroidList(5,5)
                if aSaber.collisionRect(instRect):
                    switchVal = 2
        # INSTRUCTIONS
        elif switchVal == 2:
            # RENDERING ALL TEXT
            startMessage = "Welcome to BeatLightSaber!"
            start = font.render(startMessage, True, (44,44,44))
            WINDOW.blit(start, (50, 70))
            instructM1 = "In this game, your goal is to slice droids with your "
            instruct1 = font.render(instructM1, True, (44,44,44))
            WINDOW.blit(instruct1, (50, 150))
            instructM2 = "lightsaber and do not let them hit the bottom"
            instruct2 = font.render(instructM2, True, (44,44,44))
            WINDOW.blit(instruct2, (50, 200))
            instructM2 = "of the screen!"
            instruct2 = font.render(instructM2, True, (44,44,44))
            WINDOW.blit(instruct2, (50, 250))
            instructM3 = "Hold the lightsaber with either hand "
            instruct3 = font.render(instructM3, True, (44,44,44))
            WINDOW.blit(instruct3, (50, 350))
            instructM4 = "and get slicing!"
            instruct4 = font.render(instructM4, True, (44,44,44))
            WINDOW.blit(instruct4, (50, 400))

            backRect = pygame.Rect(900,450,150,150)
            pygame.draw.rect(WINDOW, (0,0,0), backRect)

            backMessage = "BACK"   
            back = font.render(backMessage, True, (255,255,255))
            WINDOW.blit(back, (910, 490))
            if not handIsOpen:
                if aSaber.collisionRect(backRect):
                    switchVal = 1        
        #Level 1
        elif switchVal == 3:
            animateDroid()
            if(not handIsOpen):
                droidCollision()
            if(len(droidList) == 0):
                switchVal = 4
                fillDroidList(8,6)
            if(checkDroidFinish()):
                switchVal = 99
        #Level 2
        elif switchVal == 4:
            animateDroid()
            if(not handIsOpen):
                droidCollision()
            if(len(droidList) == 0):
                switchVal = 5
                fillDroidList(11,8)
            if(checkDroidFinish()):
                switchVal = 99
        #Level 3
        elif switchVal == 5:
            animateDroid()
            if(not handIsOpen):
                droidCollision()
            if(len(droidList) == 0):
                switchVal = 6
                fillDroidList(15,8)
            if(checkDroidFinish()):
                switchVal = 99
        #Level 4
        elif switchVal == 6:
            animateDroid()
            if(not handIsOpen):
                droidCollision()
            if(len(droidList) == 0):
                switchVal = 7
                fillDroidList(20,10)
            if(checkDroidFinish()):
                switchVal = 99
        #Boss Level
        elif switchVal == 7:
            animateDroid()
            if(not handIsOpen):
                droidCollision()
            if(len(droidList) == 0):
                switchVal = 8
            if(checkDroidFinish()):
                switchVal = 99
        #Win Screen
        elif switchVal == 8:
            winMessage = "YOU WIN!"
            win = font.render(winMessage, True, (255,255,255))
            WINDOW.blit(win, (400, 20))

        

        # lose screen
        elif switchVal == 99:
            loseMessage = "YOU LOSE!"
            lose = font.render(loseMessage, True, (255,255,255))
            WINDOW.blit(lose, (400, 20))

            backRect = pygame.Rect(900,450,150,150)
            pygame.draw.rect(WINDOW, (0,0,0), backRect)
            backMessage = "BACK"   
            back = font.render(backMessage, True, (255,255,255))
            WINDOW.blit(back, (910, 490))
            if not handIsOpen:
                if aSaber.collisionRect(backRect):
                    switchVal = 1    
            
 
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



