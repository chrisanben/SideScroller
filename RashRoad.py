# Source File Name: RashRoad.py
# Author's Name: Chris Bentley
# Last Modified By: Chris Bentley
# Date Last Modified: July 08, 2013
""" 
    PROGRAM DESCRIPTION: It is a Python game using the Pygame engine
                        in which the players car tries to avoid incoming traffic while
                        trying to score points.
                        
    VERSION 0.3: Incomming and Difficulty
                    - Added incomming cars in the top lane
                    - Cars can only spawn in 1 of 6 different lanes
                    - Up to a Maximun of 5 cars can appear at once
                    - Increased the screen size so the player can avoid the cars
                    - Reduced the size of the car.png
    
"""
import pygame, random
pygame.init()

screen = pygame.display.set_mode((800, 600))

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
        if mousey > 550:
            mousey = 550
        if mousey < 30:
            mousey = 30
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
    
    def update(self):
        self.rect.centerx -= self.dx
        if self.rect.centery > 340 and self.rect.centery < 700:
            self.rect.centery += self.dy
        if self.rect.right < 0:
            self.reset()
            
    def reset(self):
        self.dx = random.randrange(5, 6)
        self.dy = 0
        self.lane = random.randrange(0,3)
        self.rect.left = 800 + (random.randrange(0,20)*40)
        self.rect.centery = (self.lane*95) + 340

class InCar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/car.png")
        self.image = self.image.convert()
        self.transColor = self.image.get_at((1, 1))
        self.image.set_colorkey(self.transColor)
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.reset()
    
    def update(self):
        self.rect.centerx -= self.dx
        if self.rect.right < 0:
            self.reset()
            
    def reset(self):
        self.dx = random.randrange(9, 10)
        self.rect.left = 800 + (random.randrange(0,20)*40)
        self.rect.centery = (random.randrange(0,3)*100) + 45

class Road(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/road.png")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (1600, 600))
        self.rect = self.image.get_rect()
        self.dx = 10
        self.reset()
        
    def update(self):
        self.rect.right -= self.dx
        if self.rect.left <= -800:
            self.reset()
    
    def reset(self):
        self.rect.left = 0
        
def main():
    pygame.display.set_caption("RoadRash v0.3")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    pcar = PlayerCar()
    car1 = OutCar()
    car2 = OutCar()
    car3 = InCar()
    car4 = InCar()
    car5 = OutCar()
    road = Road()
    
    gameSprites = pygame.sprite.OrderedUpdates(road, pcar)
    carSprites = pygame.sprite.Group(car1, car2, car3, car4, car5)
    
    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(100)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True

        hitCar = pygame.sprite.spritecollide(pcar, carSprites, False)
        if hitCar:
            for carHit in hitCar:
                carHit.reset()
                
        gameSprites.update()
        gameSprites.draw(screen)
        
        carSprites.update()
        carSprites.draw(screen) 
        
        pygame.display.flip()
    
    #return mouse cursor
    pygame.mouse.set_visible(True) 
if __name__ == "__main__":
    main()
            
