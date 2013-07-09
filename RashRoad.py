# Source File Name: RashRoad.py
# Author's Name: Chris Bentley
# Last Modified By: Chris Bentley
# Date Last Modified: July 08, 2013
""" 
    PROGRAM DESCRIPTION: It is a Python game using the Pygame engine
                        in which the players car tries to avoid incoming traffic while
                        trying to score points.
                        
    VERSION 0.1: In the Works
                    - Created RoadRash using MailPilot, credit to Tom for the original file.
                    - Changed orientation of the car.
    
"""
import pygame
pygame.init()

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
        
def main():
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Mail Pilot! mpPlane.py - creating the Plane sprite")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 255))
    screen.blit(background, (0, 0))
    car = PlayerCar()
    
    allSprites = pygame.sprite.Group(car)
    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(60)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        
        pygame.display.flip()
    
    #return mouse cursor
    pygame.mouse.set_visible(True) 
if __name__ == "__main__":
    main()
            
