# Source File Name: RashRoad.py
# Author's Name: Chris Bentley
# Last Modified By: Chris Bentley
# Date Last Modified: July 08, 2013
""" 
    PROGRAM DESCRIPTION: It is a Python game using the Pygame engine
                        in which the players car tries to avoid incoming traffic while
                        trying to score points.
                        
    VERSION 0.2: Outgoing Cars and Road
                    - Using a bit of Mailpilot I created a moving background for the road.
                    - Changed the sprites for the cars
                    - Added an outgoing car which the player can collide with
    
"""
import pygame, random
pygame.init()

screen = pygame.display.set_mode((640, 480))

class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/pcar.png")
        self.image = self.image.convert()
        self.transColor = self.image.get_at((1, 1))
        self.image.set_colorkey(self.transColor)
        self.rect = self.image.get_rect()
        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.rect.center = (80, mousey)

class OutCar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/car.png")
        self.image = self.image.convert()
        self.transColor = self.image.get_at((1, 1))
        self.image.set_colorkey(self.transColor)
        self.rect = self.image.get_rect()
        self.reset()
        
        self.dx = 4
    
    def update(self):
        self.rect.centerx -= self.dx
        if self.rect.right < 0:
            self.reset()
            
    def reset(self):
        self.rect.left = 640
        self.rect.centery = (random.randrange(0,3)*80) + 265

class Road(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/road.png")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (1280, 480))
        self.rect = self.image.get_rect()
        self.dx = 10
        self.reset()
        
    def update(self):
        self.rect.right -= self.dx
        print(self.rect.left, self.rect.right)
        if self.rect.left <= -640:
            self.reset()
    
    def reset(self):
        self.rect.left = 0
        
def main():
    pygame.display.set_caption("RoadRash v0.2")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    pcar = PlayerCar()
    car = OutCar()
    road = Road()
    
    allSprites = pygame.sprite.OrderedUpdates(road, pcar, car)
    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(60)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        if pcar.rect.colliderect(car.rect):
            car.reset()
                
        allSprites.update()
        allSprites.draw(screen)
        
        pygame.display.flip()
    
    #return mouse cursor
    pygame.mouse.set_visible(True) 
if __name__ == "__main__":
    main()
            
