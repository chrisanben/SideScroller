# Source File Name: RashRoad.py
# Author's Name: Chris Bentley
# Last Modified By: Chris Bentley
# Date Last Modified: July 15, 2013
""" 
    PROGRAM DESCRIPTION: It is a Python game using the Pygame engine
                        in which the players car tries to avoid incoming traffic while
                        trying to score points.
                        
    VERSION 0.5: Music, Sound and Animation[s]
                    - ADDED EXPLOSION! HELL YEAH!
                    - Added a Crash sound effect
                    - Added an animation that plays if player hits a car
                    - Added a randomized sound effect that plays at times
                    - Added a looping soundtrack
    
"""
import pygame, random, time, mixer
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
        self.acceleration = 2

        pygame.mixer.init()
        self.crash = pygame.mixer.Sound("sounds/crash.wav")
        self.horn = pygame.mixer.Sound("sounds/horn.wav")
        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        diffx, diffy = pygame.mouse.get_rel()
        
        if self.rect.centery > mousey + 5.0:
            if self.rect.centery - self.acceleration > mousey:
                self.rect.centery -= self.acceleration
                self.acceleration = self.acceleration * 1.25
            else:
                self.rect.centery = mousey
                self.acceleration = 2.0
        elif self.rect.centery < mousey - 5.0:
            if self.rect.centery + self.acceleration < mousey:
                self.rect.centery += self.acceleration
                self.acceleration = self.acceleration * 1.25
            else:
                self.rect.centery = mousey
                self.acceleration = 2.0
        else:
            self.acceleration = 2.0

        #print (mousey, self.rect.centery, self.acceleration)
        
        if self.rect.centery > 550:
            self.rect.centery = 550
        if self.rect.centery < 30:
            self.rect.centery = 30
            
        self.rect.center = (80, self.rect.centery)

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

    def getPosition(self):
        return self.rect.centery
            
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

    def getPosition(self):
        return self.rect.centery
    
    def update(self):
        self.rect.centerx -= self.dx
        if self.rect.right < 0:
            self.reset()
            
    def reset(self):
        self.dx = random.randrange(9, 10)
        self.rect.left = 800 + (random.randrange(0,20)*40)
        self.rect.centery = (random.randrange(0,3)*100) + 45

class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.loadexplosion()
        
        self.image = pygame.image.load("images/animation/explosion (0).png")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = (-10,-10)
        self.frame = 0
        self.afterHit = False
        self.rect.centerx = 100

    def update(self, yCrash):
        self.frame += 1
        self.rect.centery = yCrash - 40
        if self.frame >= len(self.walkImages):
            self.frame = 0
            self.rect.centerx -= 1
            self.afterHit = False
        else:
            self.image = self.walkImages[self.frame]
            self.afterHit = True
            self.rect.centerx = 100

    def loadexplosion(self):
        self.walkImages = []
        for i in range(24):
            imgName = "images/animation/explosion ({0}).png".format(i)
            tmpImage = pygame.image.load(imgName)
            tmpImage = pygame.transform.scale(tmpImage, (150, 150))
            tmpImage = tmpImage.convert()
            transColor = tmpImage.get_at((10, 10))
            tmpImage.set_colorkey(transColor)
            self.walkImages.append(tmpImage)

class Gas(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/gas.png")
        self.image = self.image.convert()
        self.transColor = self.image.get_at((1, 1))
        self.image.set_colorkey(self.transColor)
        self.rect = self.image.get_rect()
        self.reset()
    
    def update(self):
        self.rect.centerx -= self.dx
        if self.rect.right < 0:
            self.reset()
            
    def reset(self):
        self.dx = random.randrange(7,8)
        self.rect.left = 800 + (random.randrange(0,20)*40)
        self.rect.centery = (random.randrange(0,6)*100) + 45

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

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 5
        self.fuel = 100
        self.font = pygame.font.SysFont("None", 50)
        self.time = 0
        self.distance = 0
        
    def update(self):
        self.text = "Lives: %d, Distance: %d m, Fuel: %d" % (self.lives, self.distance, self.fuel)
        self.image = self.font.render(self.text, 1, (255, 255, 0))
        self.rect = self.image.get_rect()
        
def main():
    pygame.display.set_caption("RoadRash v0.5")

    mixer.init(44100)
    music = mixer.Sound("sounds/soundtrack.wav")
    music.set_volume(0.2)
    music.play(loops=-1)
    
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    gamespeed = 60

    pcar = PlayerCar()
    car1 = OutCar()
    car2 = OutCar()
    car3 = InCar()
    car4 = InCar()
    car5 = OutCar()
    gas = Gas()
    explosion = Explosion()
    road = Road()
    scoreboard = Scoreboard()

    gameSprites = pygame.sprite.OrderedUpdates(road, gas)
    explosionSprite = pygame.sprite.Group(explosion)
    playerSprite = pygame.sprite.Group(pcar)
    carSprites = pygame.sprite.Group(car1, car2, car3, car4, car5)
    scoreSprite = pygame.sprite.Group(scoreboard)
    
    clock = pygame.time.Clock()
    keepGoing = True
    elapsed = 0
    addedtime = 0
    while keepGoing:
        seconds = elapsed/1000.0
        elapsed = clock.tick(gamespeed)
        scoreboard.time = seconds + scoreboard.time
        addedtime = scoreboard.time + addedtime
        if scoreboard.time > 0.33:
            if gamespeed < 100:
                scoreboard.fuel -= 1
                scoreboard.distance = scoreboard.distance + 10
            elif gamespeed < 150:
                scoreboard.fuel -= 2
                scoreboard.distance = scoreboard.distance + 20
            elif gamespeed < 225:
                scoreboard.fuel -= 3
                scoreboard.distance = scoreboard.distance + 30
            elif gamespeed < 300:
                scoreboard.fuel -= 4
                scoreboard.distance = scoreboard.distance + 40
            else:
                scoreboard.fuel -= 5
                scoreboard.distance = scoreboard.distance + 50
            scoreboard.time = 0
            scoreSprite.update()

        if addedtime > 5 or gamespeed < 60:
            addedtime = 0
            if gamespeed < 60:
                gamespeed = gamespeed * 1.02
                if gamespeed > 60:
                    gamespeed = 60
            else:
                gamespeed = gamespeed * 1.01

            #print int(gamespeed)

            soundchance1 = random.randrange(0,25)
            soundchance2 = random.randrange(0,25)

            if soundchance1 == soundchance2 and gamespeed > 60:
                pcar.horn.play()

        pygame.mouse.set_visible(False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True

        hitCar = pygame.sprite.spritecollide(pcar, carSprites, False)
        if hitCar:
            for carHit in hitCar:
                pcar.crash.play()
                yCrash = carHit.getPosition()
                carHit.reset()
                gamespeed = 30
                scoreboard.lives -= 1
                
                if scoreboard.lives <= 0:
                    print("Game over!")
                    scoreboard.lives = 5
                    scoreboard.fuel = 100
                    
        if pcar.rect.colliderect(gas.rect):
            gas.reset()
            scoreboard.fuel += 10
            if scoreboard.fuel > 100:
                scoreboard.fuel = 100
                
        gameSprites.update()
        gameSprites.draw(screen)

        playerSprite.update()
        playerSprite.draw(screen)

        if hitCar or explosion.afterHit:
            explosionSprite.update(yCrash)
            explosionSprite.draw(screen)

        scoreSprite.update()
        scoreSprite.draw(screen)
        
        carSprites.update()
        carSprites.draw(screen)
        pygame.display.flip()
    
    #return mouse cursor
    pygame.mouse.set_visible(True) 
if __name__ == "__main__":
    main()
            
