import pygame

class Saber:
    # Global Variables
    x = 0
    y = 0
    height = 100
    width = 50

    # constructor 
    def __init__( self, aX, aY, aW, aH, aColor ):
        self.x = aX
        self.y = aY
        self.height = aH
        self.width = aW
        self.color = aColor
        self.body = pygame.Rect(aX,aY,aW,aH)


    def render(self, aSurface):
        pygame.draw.rect(aSurface, self.color, self.body)
        