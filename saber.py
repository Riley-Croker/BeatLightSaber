import pygame
from shaft import Shaft

class Saber (Shaft):

    # constructor 
    def __init__( self, aX, aY, aW, aH, aColor ):
        super().__init__(aX, aY, aW, aH)
        self.color = aColor


    def render(self, aSurface):
        pygame.draw.rect(aSurface, self.color, self.body)

        