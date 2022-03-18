import pygame
from shaft import Shaft

class Saber (Shaft):

    # constructor 
    def __init__( self, aX, aY, aW, aH, aColor ):
        super().__init__(aX, aY, aW, aH)
        self.color = aColor


    def render(self, aSurface):
        pygame.draw.rect(aSurface, self.color, self.body)

    def collisionPoint(self, aX, aY):
        return self.body.collidepoint(aX,aY)
    
    def collisionRect(self, aRect):
        return self.body.colliderect(aRect)


        