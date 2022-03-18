import pygame


baseDroidImg = pygame.image.load('Assets\Battle_Droid.png')
baseDroidImg = pygame.transform.scale(baseDroidImg, (100, 155))

class Droid:
    ###Global Class Vars
    isDead = False


    #constructor function
    def __init__(self, ax, ay, atype, aspeed):
        self.x = ax
        self.y = ay
        self.type = atype
        self.speed = aspeed
        if(atype == "base"):
            self.width = 100
            self.height = 155
            self.hitbox = pygame.Rect(self.x,self.y,self.width,self.height)
        self.top = self.y
        self.bottom = self.y + self.height
        self.left = self.x
        self.right = self.x + self.width
        

    
    def render(self, aSurface, atype):
        if(atype == "base"):
            aSurface.blit(baseDroidImg,(self.x, self.y))

    def setSpeed(self, aSpeed):
        self.speed = aSpeed

    def moveDroid(self):
        self.y += self.speed
        self.top = self.y
        self.bottom = self.y + self.height

    def setDead(self, aBool):
        self.isDead = aBool

    def setPostion(self, ax ,ay):
        self.x = ax
        self.y = ay

    def updateHitbox(self):
        self.hitbox = pygame.Rect(self.x,self.y,self.width,self.height)

  