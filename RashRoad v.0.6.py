# Source File Name: RashRoad.py
# Author's Name: Chris Bentley
# Last Modified By: Chris Bentley
# Date Last Modified: July 15, 2013
""" 
    PROGRAM DESCRIPTION: It is a Python game using the Pygame engine
                        in which the players car tries to avoid incoming traffic while
                        trying to score points.
                        
    VERSION 0.6: Bug Fixing and Added Features
                    - Cars can no longer clip over other cars... (Or at least not as much, it's hard to tell)
                    - Randomized Car design
                    - Made gas cans slightly more visible
    
"""
import pygame, random, time, mixer
pygame.init()

screen = pygame.display.set_mode((800, 600))

#The player controlled car class, it determines the location of the player when playing

class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        #Set variables for Player Car
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/pcar.png")
        self.image = self.image.convert()
        self.transColor = self.image.get_at((1, 1))
        self.image.set_colorkey(self.transColor)
        self.rect = self.image.get_rect()
        self.rect.centery = 300
        self.acceleration = 2

        #Load sounds for Player Car
        pygame.mixer.init()
        self.crash = pygame.mixer.Sound("sounds/crash.wav")
        self.horn = pygame.mixer.Sound("sounds/horn.wav")

    def getPosition(self):
        #Return Y position
        return self.rect.centery
        
    def update(self):
        #Get mouse x,y coordinates and the difference from previous coordinates
        mousex, mousey = pygame.mouse.get_pos()
        diffx, diffy = pygame.mouse.get_rel()

        #If the mouse movement is downward within a certain value
        if self.rect.centery > mousey + 5.0:
            #Move the Car downward an exponential increasing amount
            if self.rect.centery - self.acceleration > mousey:
                self.rect.centery -= self.acceleration
                self.acceleration = self.acceleration * 1.25
            #Stop acceleration
            else:
                self.rect.centery = mousey
                self.acceleration = 2.0
        #If the mouse movement is upward within a certain value
        elif self.rect.centery < mousey - 5.0:
            #Move the Car upward an exponential increasing amount
            if self.rect.centery + self.acceleration < mousey:
                self.rect.centery += self.acceleration
                self.acceleration = self.acceleration * 1.25
            #Stop acceleration
            else:
                self.rect.centery = mousey
                self.acceleration = 2.0
        #If no movement, reset the sideways acceleration
        else:
            self.acceleration = 2.0

        #print (mousey, self.rect.centery, self.acceleration)

        #Set boundaries for the car to move in
        if self.rect.centery > 550:
            self.rect.centery = 550
        if self.rect.centery < 30:
            self.rect.centery = 30

        #Set position of the car    
        self.rect.center = (80, self.rect.centery)

#Enemy Car that goes in the same direction as the player albeit slower, takes the bottom 3 lanes
class OutCar(pygame.sprite.Sprite):
    def __init__(self):
        #Set variables for a car in the outgoing lane
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("images/car (0).png")
        self.image = self.image.convert()
        self.transColor = self.image.get_at((1, 1))
        self.image.set_colorkey(self.transColor)
        self.rect = self.image.get_rect()
        self.reset()
    
    def update(self):
        #Make the illusion of movement and speed, by moving car backwards
        self.rect.centerx -= self.dx
        #If the car leaves the view field, reset it
        if self.rect.centery > 340 and self.rect.centery < 700:
            self.rect.centery += self.dy
        if self.rect.right < 0:
            self.reset()

    def getPosition(self):
        #Get y position of the car
        return self.rect.centery

    def getXPosition(self):
        return self.rect.centerx
            
    def reset(self):
        #Reset values for reuse when car is past the screen
        self.dx = random.randrange(5, 6)
        self.dy = 0
        self.lane = random.randrange(0,3)
        self.rect.left = 800 + (random.randrange(0,20)*40)
        self.rect.centery = (self.lane*95) + 340

        #Randomizes the image of the car
        randomCar = random.randrange(4)
        if randomCar == 1:
            self.image = pygame.image.load("images/car (0).png")
        elif randomCar == 2:
            self.image = pygame.image.load("images/car (1).png")
        elif randomCar == 3:
            self.image = pygame.image.load("images/car (2).png")
        self.image = self.image.convert()
        self.transColor = self.image.get_at((1, 1))
        self.image.set_colorkey(self.transColor)

#Enemy Car that goes in the opposite direction of the player, takes the top 3 lanes
class InCar(pygame.sprite.Sprite):
    def __init__(self):
        #Set variables for a car in the outgoing lane
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/car (0).png")
        self.image = self.image.convert()
        self.transColor = self.image.get_at((1, 1))
        self.image.set_colorkey(self.transColor)
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.reset()

    def getPosition(self):
        #Get y position of the car
        return self.rect.centery

    def getXPosition(self):
        return self.rect.centerx
    
    def update(self):
        #Make the illusion of movement and speed, by moving car backwards
        self.rect.centerx -= self.dx
        if self.rect.right < 0:
            self.reset()
            
    def reset(self):
        #Reset values for reuse when car is past the screen
        self.dx = random.randrange(9, 10)
        self.rect.left = 800 + (random.randrange(0,20)*40)
        self.rect.centery = (random.randrange(0,3)*100) + 45

        #Randomizes the image of the car
        randomCar = random.randrange(4)
        if randomCar == 1:
            self.image = pygame.image.load("images/car (0).png")
            self.image = pygame.transform.flip(self.image, True, False)
        elif randomCar == 2:
            self.image = pygame.image.load("images/car (1).png")
            self.image = pygame.transform.flip(self.image, True, False)
        elif randomCar == 3:
            self.image = pygame.image.load("images/car (2).png")
            self.image = pygame.transform.flip(self.image, True, False)
        self.image = self.image.convert()
        self.transColor = self.image.get_at((1, 1))
        self.image.set_colorkey(self.transColor)

#In charge of explosion animation when a player loses or car hits something
class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        #Initializes the settings for the explosions
        pygame.sprite.Sprite.__init__(self)
        self.loadexplosion()
        self.image = pygame.image.load("images/animation/explosion (0).png")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = (-100,-100)
        self.frame = 0
        self.afterHit = False #Determines if the player has already hit a car
        self.rect.centerx = 100 #Fixed x position for explosion

    def update(self, yCrash):
        #Creates an explosion animation by shifting upwars through the frames
        self.frame += 1
        self.rect.centery = yCrash - 40
        #If the frameset is over, reset the sequence for further use
        if self.frame >= len(self.walkImages):
            self.frame = 0
            self.rect.centerx -= 1
            self.afterHit = False
        else:
            self.image = self.walkImages[self.frame]
            self.afterHit = True
            self.rect.centerx = 100

    def loadexplosion(self):
        #Loads the images of the explosion from folder
        self.walkImages = []
        for i in range(24):
            imgName = "images/animation/explosion ({0}).png".format(i)
            tmpImage = pygame.image.load(imgName)
            tmpImage = pygame.transform.scale(tmpImage, (150, 150))
            tmpImage = tmpImage.convert()
            transColor = tmpImage.get_at((10, 10))
            tmpImage.set_colorkey(transColor)
            self.walkImages.append(tmpImage)
        
#"SCORING" system, instead of giving you score, it gives you a longer timer to get score.
class Gas(pygame.sprite.Sprite):
    def __init__(self):
        #Initialize the variables for the placement
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/gas.png")
        self.image = self.image.convert()
        self.transColor = self.image.get_at((1, 1))
        self.image.set_colorkey(self.transColor)
        self.image.set_shifts((16,8,16,0))
        self.rect = self.image.get_rect()
        self.reset()

    def update(self):
        #Scrolls the gas from right to left
        self.rect.centerx -= self.dx
        if self.rect.right < 0:
            self.reset()
            
    def reset(self):
        #Resets values when gas is off screen
        self.dx = random.randrange(7,8)
        self.rect.left = 800 + (random.randrange(0,20)*40)
        self.rect.centery = (random.randrange(0,6)*100) + 45

#Infinetely scrolling background, which is a road
class Road(pygame.sprite.Sprite):
    def __init__(self):
        #Sets up necessary variables for scrolling road
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/road.png")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (1600, 600)) #Stretched image, numbers tell me how long should I do the scrolling
        self.rect = self.image.get_rect()
        self.dx = 10
        self.reset()
        
    def update(self):
        #Scrolls the road image
        self.rect.right -= self.dx
        if self.rect.left <= -800:
            #If the image is half done scrolling, reset it
            self.reset()
    
    def reset(self):
        #Move the image back to here, gives a faint illusion of scrolling.
        self.rect.left = 0
        
#Displays scoreboard
class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        #Initialize display
        pygame.sprite.Sprite.__init__(self)
        self.lives = 5
        self.fuel = 100
        self.font = pygame.font.SysFont("None", 50)
        self.time = 0
        self.distance = 0
        
    def update(self):
        #Display Scoreboard
        self.text = "Lives: %d          Fuel: %d%%          Distance: %d m" % (self.lives, self.fuel, self.distance)
        self.image = self.font.render(self.text, 1, (255, 255, 0))
        self.rect = self.image.get_rect()

#The engine of the game, this is the game. This has all of the components inside, all of the checking. ALL!
def game():
    #Set initial setting on the screen
    pygame.display.set_caption("RoadRash v0.6")
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    #Construct all the needed classes (Sadly, I forgot to change this to a more line friendly format)
    pcar = PlayerCar()
    gas = Gas()
    explosion = Explosion()
    road = Road()
    scoreboard = Scoreboard()

    cars = []
    for index in range(6):
        if index < 3:
            cars.append(OutCar())
        else:
            cars.append(InCar())

    #Set up the sprites and their groups
    gameSprites = pygame.sprite.OrderedUpdates(road, gas)
    explosionSprite = pygame.sprite.Group(explosion)
    playerSprite = pygame.sprite.Group(pcar)
    carSprites = pygame.sprite.Group(cars)
    scoreSprite = pygame.sprite.Group(scoreboard)

    #Initialize the clock
    clock = pygame.time.Clock()

    #Variables used in the loop
    keepGoing = True
    elapsed = 0     #Ticks of Clock
    addedtime = 0   #Total time played
    gamespeed = 45  #Clock speed
    
    while keepGoing:
        #Calculation for time
        seconds = elapsed/1000.0
        elapsed = clock.tick(gamespeed)
        #Time is used for ticks, Addedtime for longer checks
        scoreboard.time = seconds + scoreboard.time
        addedtime = scoreboard.time + addedtime

        #3 times a second, decrease fuel depending on speed and increase points
        if scoreboard.time > 0.33:
            if gamespeed < 60:
                scoreboard.fuel -= 1
                scoreboard.distance = scoreboard.distance + 10
            elif gamespeed < 125:
                scoreboard.fuel -= 2
                scoreboard.distance = scoreboard.distance + 20
            elif gamespeed < 175:
                scoreboard.fuel -= 3
                scoreboard.distance = scoreboard.distance + 30
            elif gamespeed < 250:
                scoreboard.fuel -= 4
                scoreboard.distance = scoreboard.distance + 40
            else:
                scoreboard.fuel -= 5
                scoreboard.distance = scoreboard.distance + 50

            scoreboard.fuel += 5

            #If out of fuel, give game over
            if scoreboard.fuel <= 0:
                scoreboard.fuel = 0
                keepGoing = False

            #Reset time for ticks and update
            scoreboard.time = 0
            scoreSprite.update()

        #If addedtime is 5seconds increase speed. If speed is under normal, accelerate it quicker.
        if addedtime > 5 or gamespeed < 45:
            addedtime = 0 #Reset time
            if gamespeed < 45:
                gamespeed = gamespeed * 1.02 #Don't be fooled, because it ignores ticks this accelerates quickly.
                if gamespeed > 45:
                    gamespeed = 45
            else:
                if gamespeed < 250:
                    gamespeed = gamespeed + 1

            #print int(gamespeed)

            #Some random sound effect I added. You have a 4% chance of hearing it every 5 seconds.
            soundchance1 = random.randrange(0,25)
            soundchance2 = random.randrange(0,25)
            if soundchance1 == soundchance2 and gamespeed > 60:
                pcar.horn.play()

        #Set the mouse invisible
        pygame.mouse.set_visible(False)

        #Quit if player quits
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True


        #Checks for Overlapping cars and resets one of the overlapping ones
        for index in range(6):
            for idx in range(6):
                if index != idx:
                    if cars[idx].getPosition() == cars[index].getPosition():
                        if cars[idx].getXPosition() < cars[index].getXPosition():
                            if cars[idx].getXPosition() - 125 <= cars[index].getXPosition() <= cars[idx].getXPosition() + 125:
                                #print "Car[%d] is near Car[%d]" % (index, idx)
                                #print "======================="
                                cars[index].reset()

            
        #Create hit car collision detection with player car
        hitCar = pygame.sprite.spritecollide(pcar, carSprites, False)
        #If a car hits player
        if hitCar:
            for carHit in hitCar:
                #Play car crash sound
                pcar.crash.play()
                yCrash = carHit.getPosition()

                #Reset car location
                carHit.reset()

                #Reduce speed and decrease lives
                gamespeed = 30
                scoreboard.lives -= 1

                #Lose if got no lives
                if scoreboard.lives <= 0:
                    keepGoing = False

        #If player hits gas can, increase gas but not over 100
        if pcar.rect.colliderect(gas.rect):
            gas.reset()
            scoreboard.fuel += 10
            if scoreboard.fuel > 100:
                scoreboard.fuel = 100

        #Draw/Update Road and Gas Sprites
        gameSprites.update()
        gameSprites.draw(screen)

        #Draw/Update Player Sprites
        playerSprite.update()
        playerSprite.draw(screen)

        #If player hit a car. Play animation, end when reached last frame.
        if hitCar or explosion.afterHit:
            explosionSprite.update(yCrash)
            explosionSprite.draw(screen)

        #Draw/Update Scoreboard
        scoreSprite.update()
        scoreSprite.draw(screen)

        #Draw/Update Inbound/Outbound cars
        carSprites.update()
        carSprites.draw(screen)
        pygame.display.flip()
        
    #END PLAYER CAR EXPLOSION ANIMATION
    endExplosion = True
    counter = 0
    pcar.crash.play()
    while endExplosion:
        clock.tick(30)
        counter += 1
        yCrash = pcar.getPosition()
        explosionSprite.update(yCrash)
        explosionSprite.draw(screen)
        if counter == 25:
            endExplosion = False
        pygame.display.flip()

    #Set mouse to visible
    pygame.mouse.set_visible(True)
    
    return scoreboard.distance

def intro(score):
    pygame.display.set_caption("RoadRash v0.6")

    #This is MailPilots intro Screen stuff. Basically, the game with no win/lose conditions.
    pcar = PlayerCar()
    road = Road()
    allSprites = pygame.sprite.OrderedUpdates(road, pcar)

    #Write/Draw instructions plus Score
    insFont = pygame.font.SysFont(None, 50)
    insLabels = []
    instructions = (
    "",
    "Road Rash.     Last Run: %d m" % score ,
    "Instructions:  A bomb is been planted in",
    "your car if you don't go fast, you'll explode!",
    "",
    "Run over the gas cans to keep your fuel up,",
    "but be careful not to run into traffic.",
    "The car is rigged to constantly go faster.",
    "",
    "click to start, escape to quit..."
    )

    for line in instructions:
        tempLabel = insFont.render(line, 2, (255, 255, 255))
        insLabels.append(tempLabel)
 

    #Game "engine", it updates, draws and determines what happens.
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN: #Click to start game
                keepGoing = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True
    
        allSprites.update()
        allSprites.draw(screen)

        #Draws the instructions
        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()

    #Set mouse visible again
    pygame.mouse.set_visible(True)
    return donePlaying

def main():
    #Plays soundtrack for the game
    mixer.init(44100)
    music = mixer.Sound("sounds/soundtrack.wav")
    music.set_volume(0.2)
    music.play(loops=-1)
    score = 0
    donePlaying = False

    #The main game loop, keeps playing the game until the player quites it
    while not donePlaying:
        donePlaying = intro(score) #This is the first screen
        if not donePlaying:
            score = game() #This is the game

    music.stop()
    
    
if __name__ == "__main__":
    main()
            
