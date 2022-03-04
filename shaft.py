import pygame

class Shaft:
    # Global Variables
    x = 0
    y = 0
    height = 100
    width = 50

    # constructor 
    def __init__( self, aX, aY, aW, aH):
        self.x = aX
        self.y = aY
        self.height = aH
        self.width = aW
        self.body = pygame.Rect(aX,aY,aW,aH)


    def render(self, aSurface):
        pygame.draw.rect(aSurface, (0,0,0), self.body)

    def updatePosition(self, aX, aY):
        self.x = aX
        self.y = aY
        self.body = pygame.Rect(aX,aY,self.width,self.height)