import sys
import pygame
import Invader
from pygame.locals import *
import Missile

class SpaceInvaders:

    # Constructor of the basic game class.
    # This constructor calls initialize and main_loop method.
    def __init__(self):
        self.initialize()
        self.main_loop()

    # Initialization method. Allows the game to initialize different
    # parameters and load assets before the game runs
    def initialize(self):
        pygame.init()
        pygame.key.set_repeat(1, 1)

        self.width = 1024
        self.height = 768
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.caption = "Space Invader!!"
        pygame.display.set_caption(self.caption)
        
        
        self.framerate = 30

        self.clock = pygame.time.Clock()

        self.gameState = 1

        self.font = pygame.font.Font(None, 40)

        self.explosionSound = pygame.mixer.Sound("explosion.wav")
        self.shootSound = pygame.mixer.Sound("shoot.wav")
        self.leftrightSound = pygame.mixer.Sound("fastinvader1.wav")
        self.initializeGameVariables()


    def initializeGameVariables(self):        
        self.space = pygame.image.load('space.png')
        self.invaderImg = pygame.image.load('invader.png')
        self.altInvaderImg = pygame.image.load('inv12.png')
        self.rocketLauncherImg = pygame.image.load('rocketLauncher.png')        
        self.missileImg = pygame.image.load('missile1.png')
        self.missileFired = None

        self.playerScore = 0
        self.lives = 3

        self.rocketXPos = 512
        #self.alienXPos = 512
        #self.alienYPos = 100

                
        self.alienDirection = -1            
        self.alienSpeed = 7

        self.rows = 0
        self.ticks = 0
        self.InvaderRemaining = True
        self.invaders = []
        
        yPos = 100
        for r in range (5):
            xPos = 512
            for i in range(11):
                invader = Invader.Invader()
                invader.setPosX(xPos)
                invader.setPosY(yPos)
                self.invaders.append(invader)            
                xPos += 32
            yPos = yPos + 50

  
    # main loop method keeps the game running. This method continuously
    # calls the update and draw methods to keep the game alive.
    def main_loop(self):
        self.clock = pygame.time.Clock()
        while True:
            gametime = self.clock.get_time()
            self.update(gametime)
            self.draw(gametime)
            self.clock.tick(self.framerate)
            

    # Update method contains game update logic, such as updating the game
    # variables, checking for collisions, gathering input, and
    # playing audio.
    def update(self, gametime):
        if self.gameState == 1:
            self.updateStarted(gametime)
        elif self.gameState == 2:
            self.updatePlaying(gametime)
        elif self.gameState == 3:
            self.updateEnded(gametime)
        elif self.gameState == 4:
            self.updateHelp(gametime)


    def updateStarted(self, gametime):   
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.gameState = 2
                    break
                elif event.key == pygame.K_h:
                    self.gameState = 4
                    break
                
    def updateHelp(self, gametime):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    self.gameState = 4
                    break
    

    def updatePlaying(self, gametime):
        if self.InvaderRemaining == False:
            self.gameState = 3
            return

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.rocketXPos = self.rocketXPos + 4
                elif event.key == pygame.K_LEFT:
                    self.rocketXPos = self.rocketXPos - 4
                elif event.key == pygame.K_SPACE:
                    if self.missileFired == None :
                        self.missileFired = Missile.Missile(self.rocketXPos,650)
                        self.shootSound.play()
                        leftMostInvader = None
                       

    
        invaderFound = False
        for i in range(55):
            if self.invaders[i].visible != False:
                invaderFound = True
                break

        if invaderFound == False:            
            self.InvaderRemaining = False           
                        

        if self.rocketXPos < 100:
            self.rocketXPos = 100

        if self.rocketXPos > 924:
            self.rocketXPos = 924

        if self.missileFired != None:
            self.missileFired.move()
            if self.missileFired.getPosY() < 0:
                self.missileFired=None
                

        self.ticks = self.ticks + gametime

        if self.ticks < 500:
            for i in range(55):
                if self.invaders[i] != None:
                    self.invaders[i].moveHorizontal(self.alienSpeed * self.alienDirection)

            leftMostInvader = None
            rightMostInvader = None

        

        for i in range (55):
            if self.invaders[i] != None:
                leftMostInvader = self.invaders [i]
                break

        for i in range (54, -1, -1):
            if self.invaders[i] != None:
                rightMostInvader = self.invaders[i]
                break

        if leftMostInvader.getPosX() < 96:
            self.alienDirection = +1
            self.leftrightSound.play()

            xPos = 96
            for r in range (55):
                if r % 11 == 0:
                    xPos = 96
                #for i in range(11):
                if self.invaders[r] != None:
                    self.invaders[r].moveVertical(4)
                    self.invaders[r].setPosX(xPos)
                xPos = xPos + 32
   

        if rightMostInvader.getPosX() > 924 :
            self.leftrightSound.play()
            self.alienDirection = -1 
            

            xPos = 924 - 32 * 10
            for r in range (55):

                if r % 11 == 0:
                    xPos = 924 - 32 * 10 
                
                if self.invaders[r] != None:
                    self.invaders[r].moveVertical(4)
                    self.invaders[r].setPosX(xPos)
                xPos = xPos + 32
                
                    
        self.ticks = 0

        if self.missileFired != None:
            rectMissile = pygame.Rect(self.missileFired.getPosX(),
                self.missileFired.getPosY(), self.missileImg.get_width(), self.missileImg.get_height())
            for i in range(55):
                if self.invaders[i].visible:
                    rectInvader = pygame.Rect(self.invaders[i].getPosX(), self.invaders[i].getPosY(), self.invaderImg.get_width(), self.invaderImg.get_height())
                    if rectMissile.colliderect(rectInvader):
                        self.missileFired = None
                        self.invaders[i].takehit()
                        self.explosionSound.play()
                        if i < 23 :
                            self.playerScore = self.playerScore + 500
                        elif i >= 45 :
                            self.playerScore = self.playerScore + 50
                        else:
                            self.playerScore = self.playerScore + 200
                            break


    def updateEnded(self, gametime):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    self.initializeGameVariables()
                    self.gameState = 1



    # Draw method, draws the current state of the game on the screen                        
    def draw(self, gametime):
        if self.gameState == 1:
            self.drawStarted(gametime)
        elif self.gameState == 2:
            self.drawPlaying(gametime)
        elif self.gameState == 3:
            self.drawEnded(gametime)
        elif self.gameState == 4:
            self.drawHelp(gametime)

    def drawStarted(self, gametime):
        self.screen.blit(self.space, (0,0))

        width, height = self.font.size("SPACE   INVADERS!")
        text = self.font.render("SPACE  INVADERS!", True, (255, 255, 255))
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos, 200))

        width, height = self.font.size("PRESS 'S' TO START")
        text = self.font.render("PRESS 'S' TO START", True,(255, 255, 255))
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos, 400))

        width, height = self.font.size("PRESS 'H' FOR HELP")
        text = self.font.render("PRESS 'H' FOR HELP", True,(255, 255, 255))
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos, 600))
        pygame.display.flip()

    def drawHelp(self, gametime):
        self.screen.blit(self.space, (0,0))
        
        width, height = self.font.size("Shoot the aliens with the Space key.")
        text = self.font.render("Shoot the aliens with the Space key.", True, (255, 64, 64))
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos, 200))

        pygame.display.flip()   
                         



    def drawPlaying(self, gametime):
        self.screen.blit(self.space, (0,0))
        
        score_text = self.font.render("Score : %d" %self.playerScore, True,(202, 255, 112))
        self.screen.blit(score_text, (10, 10))

        lives_text = self.font.render("lives : %d" %self.lives, True,(202, 255,112))
        self.screen.blit(lives_text, (800, 10))
                         
        self.screen.blit(self.rocketLauncherImg, (self.rocketXPos, 650))
        if self.missileFired != None:
            self.screen.blit(self.missileImg, (self.missileFired.getPosX(), self.missileFired.getPosY() - self.missileImg.get_height()))
        for i in range(55):
            if self.invaders[i].visible:
                self.screen.blit(self.invaderImg, self.invaders[i].getPosition())
        pygame.display.flip()

    


    def drawEnded(self, gametime):
        self.screen.blit(self.space, (0,0))

        width, height = self.font.size("PRESS 'R' TO RESTART GAME")
        text = self.font.render("PRESS 'R' TO RESTART GAME", True, (224, 255, 255))
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos, 200))
        width, height = self.font.size("PRESS 'X' TO EXIT GAME")
        text = self.font.render("PRESS 'X' TO EXIT GAME", True, (224, 255, 255))
        width, height = self.font.size ("Score : ")
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos, 300))
        text = score_text = self.font.render("Score : %d" %self.playerScore, True,(224, 255, 255))
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos, 400))
        pygame.display.flip()

if __name__ == "__main__":
    game = SpaceInvaders()
