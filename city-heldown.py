import pygame
import pgzrun
import os
import time 
import random
from pgzhelper import *
                                        
#initialize dimensions
WIDTH = 702
HEIGHT = 468
picture = pygame.image.load("images\\city1.PNG")
picture = pygame.transform.scale(picture, (WIDTH, 458))
end = pygame.image.load("images\\nuke.PNG")
end = pygame.transform.scale(end, (WIDTH, 458))

     
class MainMenu():
    '''class MainMenu() manages the main menu graphics and elements'''
    def __init__(self):
        '''constructor of MainMenu() - initalizes the elements of the menu screen'''
        self.start = Actor('logo',pos = (230,180))
        self.start.scale = 0.95
        self.helicopter = Actor('burning',pos = (230,410))
        self.helicopter.scale = 0.30
        self.settings = Actor("settings.png", pos = (560,200))
        self.settings.scale = 0.60
        self.exit1 = Actor("exit1.png", pos = (564,350))
        self.exit1.scale = 0.98
     
    def draw(self):
        '''Draws the elements of the main menu'''
        self.start.draw()
        self.settings.draw()
        self.exit1.draw()
        self.helicopter.draw()
        
class Settings():
    '''class Settings() manages the settings graphics and elements'''
    def __init__(self):
        '''Constructor of Settings() - initalizes the elements of the settings menu'''
        self.settingsbar = Actor("settings1.png", pos = (355,120))
        self.settingsbar.scale = 1
        self.p1 = Actor("p1.png", pos = (230,260))
        self.p1.scale = 0.65
        self.p1binds = Actor("pjump.png", pos = (450,260))
        self.p1binds.scale = 0.4
        self.p1shoot = Actor("pshoot.png", pos = (520,263))
        self.p1shoot.scale = 0.4
        self.backButton = Actor("backbutton.png", pos = (150,413))
        self.backButton.scale = 0.7
        self.startButton = Actor("startbutton.png", pos = (370,412))
        self.startButton.scale = 0.75
        self.settingsexit = Actor("settingsexit.png", pos = (570,415))
        self.settingsexit.scale = 0.75
   
    def draw(self):
        '''Draws the elements of the settings menu'''
        self.settingsbar.draw()
        self.p1.draw()
        self.p1binds.draw()
        self.p1shoot.draw()
        self.startButton.draw()
        self.backButton.draw()
        self.settingsexit.draw()
      
      
class GameElements():
    '''class GameElements() manages the game graphics and elements'''
    def __init__(self):
        '''Constructor of GameElements() - initalizes the stationary elements'''
        self.cap = Actor('cap', pos=(30,30))
        self.windjacket = Actor('windjacket', pos=(78,30))
        self.jeans = Actor('jeans', pos=(126,30))
        self.boots = Actor('boots', pos=(174,30))
        self.backpack = Actor('backpack', pos=(222,30))
        self.bandage = Actor('bandage', pos=(126,78))
        self.medkit = Actor('medickit', pos=(78,78))
        self.cannedfood = Actor('cannedfood', pos=(222,78))
        self.fresh = Actor('fresh', pos=(174,78))
        self.m4 = Actor('m4', pos=(30,78))
        self.radioactive = Actor('radioactive', pos=(630,54))
        self.radioactive.scale = 0.25
        self.zombd = Actor('zombd', pos=(630,200))
        self.zombd.scale = 0.25
        

    def draw(self):
        '''Draws the stationary elements of the game'''
        self.windjacket.draw()
        self.jeans.draw()
        self.boots.draw()
        self.backpack.draw()
        self.bandage.draw()
        self.cannedfood.draw()
        self.m4.draw()
        self.medkit.draw()
        self.cap.draw()
        self.fresh.draw()
        self.radioactive.draw()
        self.zombd.draw()
        

class DeathScreen():
    '''class DeathScreen() manages the settings graphics and elements'''
    def __init__(self):
        '''Constructor of DeathScreen() - initalizes the elements of the nuclear death screen'''
        self.defeat = Actor('defeat', pos=(550,295))
        self.defeat.scale = 0.50
        self.reset = Actor('reset', pos =(645,292))
        self.reset.scale = 0.25
  
    def draw(self):
        '''Draws the elements of the nuclear death screen'''
        self.defeat.draw()
        self.reset.draw()
     
    
class Timer():
    '''class Timer() represents the countdown timer for the nuclear bomb of the game'''
    def __init__(self):
        '''Constructor of the class - intialize the values for the time'''
        #initialize nuclear timer with a countdown of 60 seconds
        self.countdown = 13
        #initialize time availability to true
        self.timeAvailable = True
        self.deathFreeze = False
        
       
    def update(self):
        global mode
        '''Updates the available time'''
        #check if time is still available
        if self.timeAvailable == True:
            #decrement the count by 1/60 seconds
            self.countdown -= 1/60
            #if timer reaches around 1, play nuke whistle and explosion
            if self.countdown == 1.049999999999777:
                sounds.whistle.play()
                sounds.whistle.set_volume(0.1)
                sounds.explosion.play()
                self.deathFreeze = True
            
            #if timer reaches 0, set the time available to False
            if self.countdown <= 0:
                self.timeAvailable = False
                mode = 'end'
   
          
    def draw(self):
        '''Draws the time display'''
        #if time is still available, draw the countdown
        if self.timeAvailable == True:
            tx, ty = gameElements.radioactive.pos
            screen.draw.text(str(round(self.countdown, 0)), center=(tx, ty-27), color="black", fontsize=18)
   
                               
class Soldier():
    '''class Soldier() manages the attributes and behavior of the soldier (player) in the game'''
    def __init__(self):
        '''Constructor of Soldier() - initalizes the position, scale and animations of the player'''
        #initalize the soldier attributes
        self.soldier = Actor('idle1', pos=(120, 350))
        self.soldier.scale = 2.75
        self.soldier.images = ['g1run', 'g2run', 'g3run', 'g4run', 'g5run']
        self.soldier.deathImage = ['gdeath']
        self.jumpMode = ['gjump']
        self.soldier.fps = 8
        self.alive = True
        self.jump = False
        #jump parameters
        self.jumpHeight = 2000 
        self.jumpSpeed = 0
        self.dy = 0
        #initalize button used to reset game upon death
        self.srestart = Actor('gamereset',pos = (640,440))
        self.srestart.scale = 0.55

    def draw(self):
        '''Draws the player'''
        self.soldier.draw()
        #if player has died, draw the reset button
        if self.alive == False:
            self.srestart.draw()
            
        
    def update(self):
        '''Updates the player - performs movements animations (walking and jumping)'''
        #if the player is alive, execute the following
        if self.alive == True:
            #animate the soldier by traversing through the list of images
            self.soldier.animate()
            
            #check if the player is currently jumping
            if self.jump == True:
                #swap the image to jump by grabbing the first index of the list
                self.soldier.image = self.jumpMode[0]
                #moves the soldier vertically based on jump parameter
                self.soldier.y += self.dy

                #checks if the player has reached the top of the jump
                if self.soldier.y <= 350 - self.jumpHeight:
                    #if the player has reached the top, stop the vertical speed and stop the jump
                    self.dy = 0
                    self.jump = False
                #check if the player is still ascending
                elif self.soldier.y <= 350:
                    #increase the vertical speed during the jump
                    self.dy += 0.1 

    def jumpAction(self):
        '''Jump action of the player'''
        if self.alive == True:
            #if player is not jumping, allow them to jump up
            if not self.jump:
                self.jump = True
                self.dy = -6

    def gravity(self):
        '''Simulates the gravity of the jump'''
        #if player is not jumping, apply gravity
        if not self.jump:
            #increase the vertical speed of the player due to gravity
            self.dy += 0.2
        else:
            #move the player vertically based on the current vertical speed
            self.soldier.y += self.dy
            #increase the vertical speed during descent
            self.dy += 0.10

            #checks if the player has landed
            if self.soldier.y >= 357:
                #if player has landed, set the position to ground level
                self.soldier.y = 357
                #ends the jump by resetting the jump flag and vertical speed
                self.jump = False
                self.dy = 0        
                
    def trapDeath(self):
        '''Death image of player to trap'''
        #swap the image of the player to a death image if the player has died to a trap
        if self.alive == False:
            self.soldier.image = self.soldier.deathImage[0]
       
            
    def zomDeath(self):
        '''Death image of player to zombie'''
        if self.alive == False:
            #swap the image of the player to a death image if the player has died to a zombie
            self.soldier = Actor('gdeath', pos=(120, 380))
            self.soldier.scale = 2.75
        
            
class Bullet():
    '''class Bullet() governs the bullets of the game'''
    def __init__(self):
        '''Constructor of Bullet() - initalizes bullet elements'''
        #list to store bullet instances
        self.bullets = []
        #list to store bullets that need to be removed
        self.bulletsRemoval = []
        #initalize bullet speed
        self.bulletSpeed = 15
        #initailize flash image when gun shoots
        self.flash = Actor('flash', pos=(0, 0))
        self.flashVisible = False
        #initalize flash effect duration
        self.flashTimer = 0.1

    def draw(self):
        '''Draws the bullets and gun flash of the game'''
        #draw each bullet in the bullets list
        for bullet in self.bullets:
            bullet.draw()
            
        #draw flash effect if set to visible
        if self.flashVisible:
            self.flash.draw()

    def update(self):
        '''Update the position of bullets and manage collisions'''
        new_bullets = []
        for bullet in self.bullets:
            bullet.x += self.bulletSpeed
            # collision with zombie
            if mob.alive and bullet.colliderect(mob.zombie):
                sounds.splat.play()
                sounds.splat.set_volume(0.75)
                sounds.counter.play()
                sounds.counter.set_volume(0.4)
                mob.deathcounter += 1
                mob.alive = False
                continue  # skip adding bullet to new_bullets

            # keep bullet if it hasn't left the screen
            if bullet.right <= WIDTH:
                new_bullets.append(bullet)

        self.bullets = new_bullets  # replace bullets with only active ones

        # update flash effect
        if self.flashVisible:
            self.flashTimer -= 1 / 60
            if self.flashTimer <= 0:
                self.flashVisible = False
        
                

    def createBullet(self, position):
        '''Creates a new bullet at a specified position'''
        #creates the bullet actor
        bullet = Actor('bullet', position)
        #sets the size of the bullet
        bullet.scale = 2
        #add bullet to list of bullets
        self.bullets.append(bullet)
        #sets the position of the flash to the location of the player's weapon
        self.flash.x = position[0] - 45
        self.flash.y = position[1] - 2
        #resets the flash timer and makes the flash effect visible
        self.flashTimer = 0.1
        self.flashVisible = True          
          
class Zombie():
    '''class Zombie() manages the attributes and behavior of the zombie enemies in the game'''
    def __init__(self):
        '''Constructor of Zombie() - initalizes the position, scale and animations of the player'''
        #creates an Actor for the zombie's idle state and sets the position
        self.zombie = Actor('z1',pos=(900,360))
        #sets the size of the zombie
        self.zombie.scale = 3
        #list of images for the zombie's walking and fighting animations
        self.zombie.idle = ['z1', 'z2', 'z3','z4','z5','z6','z7','z8']
        self.zombie.images = self.zombie.idle.copy()
        self.zombie.fight = ['a1','a2','a3','a4','z1']
        #sets the frame per second for the zombie walking animation
        self.zombie.fps = 10
        #initalize zombie death counter
        self.deathcounter = 0
        self.attackTimer = 0
        self.alive = True
        self.isAttacking = False
        self.deathFreeze = False
        
    def update(self):
        '''Update the zombie'''
        #checks if zombie is alive
        if self.alive == True:
            #changes the walking speed of the zombie (zombie moves from the right to left)
            self.zombie.x -= 0.7
            #check if the zombie has walked past a certain point
            if self.zombie.x <= 177:
                #set the position of the zombie to that point if it has walked past it
                self.zombie.x = 177
                #checks if the zombie is at that point and make sure it is not attacking
                if self.zombie.x == 177 and self.isAttacking == False:
                    sounds.pzombie.play()
                    #change the animation of the zombie to attack mode to fight the player
                    self.zombie.images = self.zombie.fight
                    #set attack flag to True
                    self.isAttacking = True
                #if zombie attacking flag is True, execute the following 
                if self.isAttacking:
                    #increase the attack timer of the zombie
                    self.attackTimer += 1
                    #if the attack timer has reached 22, attack is over
                    if self.attackTimer == 22:
                        #set player to not alive
                        player.alive = False
                        #set game freeze to True
                        self.deathFreeze = True
                        #change the player to player death image by zombie from class Player()
                        player.zomDeath()
                        #play sound effects
                        sounds.claw.play()
                        music.stop()
                        sounds.pzdeath.play()
                        sounds.whistle.stop()
                        sounds.explosion.stop()
                        sounds.nuke.stop()
                        
                #ensures there is only attack cycle animation
                if self.zombie.image == "z1":
                    self.zombie.images = self.zombie.idle
            #animates the zombie by traveling through the list of images
            self.zombie.animate()
        
        #checks if zombie is dead
        elif self.alive == False:
            #if zombie is dead, switch back to walking animation, reset flag and attack timer
            self.zombie.images = self.zombie.idle
            self.isAttacking = False
            self.attackTimer = 0
                   
    def draw(self):
        '''Draws the zombie'''
        #draw the zombie if still alive
        if self.alive == True:
            self.zombie.draw()
        #displays on the screen how many zombies are killed
        screen.draw.text(str(round(self.deathcounter,0)), (657, 160), color="black", fontsize=30,fontname="gothic")
            

    def generate(self):
        #if zombie is dead, execute the following
        if self.alive == False:
            #generate a new random x-coordinate for the trap past the screen using the random library
            randomx = random.uniform(800, 1500)
            #set the random x-coordinate alongside the fixed the y-coordinate for the zombie
            self.zombie.midleft = (randomx, 360)
            #set the zombie to alive
            self.alive = True


            
class Trap():
    '''class Trap() manages the attributes and behavior of the trap objects in the game'''
    def __init__(self):
        '''Constructor of Trap() - initalizes the elements of the trap'''
        #creates an Actor for the trap's position
        self.trap = Actor('t1',pos=(550,390))
        #creates a list of images for the zombie's animation
        self.trap.images = ['t1','t2','t3','t4']
        #changes the size of the trap
        self.trap.scale = 2
        #sets the frame per second for the trap animation
        self.trap.fps = 1.5
        self.deathFreeze = False
    
    def draw(self):
        '''Draws the trap'''
        self.trap.draw()

    def update(self, actor):
        '''Animates the trap'''
        #checks if the player has collided with the middle of the trap
        if self.trap.colliderect(actor) and self.trap.left <= actor.centerx <= self.trap.right:
            #animates the trap only when it collides with the player
            self.trap.animate()
            #set player to dead and freeze all the elements in the game
            player.alive = False
            self.deathFreeze = True
            player.trapDeath()
            #play and stop sound effects
            music.stop()
            sounds.nuke.stop()
            sounds.beartrap.play()
            sounds.death.play()
            sounds.playerdead.play()
            sounds.whistle.stop()
            sounds.explosion.stop()
 
            
    def generate(self):
        '''generates random traps past the screen'''
        #checks if the trap has gone past the left boundary
        if self.trap.x < 20:
            #generate a new random x-coordinate for the trap past the screen using the random library
            randomx = random.uniform(1000, 2000)
            #set the random x-coordinate alongside the fixed the y-coordinate for the trap
            self.trap.midleft = (randomx, 390)
     
     
class Ground():
    '''class Ground() manages the terrain of the game for walking'''
    def __init__(self):
        '''Constructor of class Ground() - initalizes ground actor and elements'''
        #list to store instances of ground actors
        self.groundPieces = []
        #loop to create ground pieces along the width of game
        for x in range((WIDTH // 64) + 10):
            #creates ground actor instance at a specific position along x-axis
            #multiply to ensure each ground piece is 64 pixel to the right of the previous
            groundInstance = Actor('ground', pos=(x * 64, HEIGHT))
            #changes size of ground
            groundInstance.scale = 2.6
            #add ground instance to list of ground pieces
            self.groundPieces.append(groundInstance)

    def draw(self):
        '''Draws ground pieces'''
        #iterates over each ground pieces and draws them
        for groundInstance in self.groundPieces:
            groundInstance.draw()

    def update(self):
        '''Updates the position of ground pieces'''
        #set the scrolling speed of the game
        scrollSpeed = -7

        #loops through the ground pieces
        for groundInstance in self.groundPieces:
            #move ground piece horizontally with the scroll speed of the game
            groundInstance.x += scrollSpeed

            #check if the ground piece has gone beyond the left boundary
            if groundInstance.right < 0:
                #move the ground piece to the right boundary to create a continuous loop
                groundInstance.x = WIDTH - 64
    
    
def on_mouse_down(pos):
    global mode
    '''Handles mouse click events'''
    #if player clicks exit button in the start screen, play a sound and exit the game completely
    if mode == 'start':
        if menu.exit1.collidepoint(pos):
            sounds.select.play()
            quit()
        #if player clicks exit button in the start screen, play a sound and switch to settings menu
        if menu.settings.collidepoint(pos):
            sounds.select.play()
            mode = 'settings'
             
    if mode == 'settings':
        #if player clicks back button in settings screen, go back to start screen
        if settings.backButton.collidepoint(pos):
            sounds.select.play()
            mode = 'start'
            
        #if player clicks start button in settings screen, switch mode to game
        elif settings.startButton.collidepoint(pos):
            mode = 'game'
            sounds.teleport.play()
            music.stop()
            music.play('main')
            #play sound effects
            sounds.nuke.play()
            sounds.angry.play()
            sounds.angry.set_volume(0.65)
            sounds.nuke.set_volume(0.5)
            sounds.teleport.set_volume(0.40)
            
        #if player clicks exit button in settings screen, exit game completely
        elif settings.settingsexit.collidepoint(pos):
            sounds.select.play()
            quit()
            
    #if player clicks reset button in game mode, return to menu and play stop sound effects
    if mode == 'game' and player.alive == False:
        player.srestart.collidepoint(pos)
        sounds.select.play()
        sounds.playerdead.stop()
        sounds.splat.stop()
        sounds.counter.stop()
        sounds.claw.stop()
        sounds.pzdeath.stop()
        sounds.beartrap.stop()
        music.stop()
        sounds.pzombie.stop()
        sounds.death.stop()
        main()
        
    if mode == 'end':
        sounds.select.play()
        main()
    

def on_key_down(key):
    global mode, gameBegins, binaryText, decrypt
    '''Handles key press events'''
    #if the player clicks space in start menu, switch Heldown to game mode 
    if mode == 'start':
        if key == keys.SPACE:
            mode = 'game'
            sounds.teleport.play()
            music.stop()
            music.play('main')
            #play sound effects
            sounds.nuke.play()
            sounds.angry.play()
            sounds.angry.set_volume(0.65)
            sounds.nuke.set_volume(0.5)
            sounds.teleport.set_volume(0.40)

    
    #if the player clicks the 'r' key in game, create the bullets from the class, Bullet()
    if mode == 'game':
        if player.alive == True:
            if key == keys.R:
                sounds.gun.play()
                #paramaters to set positon of flash and bullets
                bullet.createBullet((player.soldier.x + 100, player.soldier.y-5))
                
            #if the player clicks 'w', perform a jump
            if key == keys.W:
                #allow the player to only jump when the zombie is beyond certain position
                if mob.zombie.x > 350:
                    player.jumpAction()
                    sounds.jump.play()
                
            # if the player clicks 'enter', decrypt the nuclear bomb
            if key == keys.RETURN:
                #countdown ends
                countdown.timeAvailable = False
                #swaps the image of the radioactive symbol to thumbs up
                gameElements.radioactive = Actor('safety', pos=(630,54))
                gameElements.radioactive.scale = 0.25
                #switch text in the top right to decoded
                binaryText = "0000000000000000000000000000000000000000"
                #swap text to say that decryption is completion
                decrypt = "PROCEDURE COMPLETE"
                #play sound effects
                sounds.decode.play()
                sounds.success.play()
                sounds.nuke.stop()
                sounds.angry.stop()
                sounds.explosion.stop()
                sounds.whistle.stop()

            
                                
def draw():
    '''Draws each actor and other ui elements'''
    global gameBegins
    #clears the screen and allows for new images to be drawn
    screen.clear()
    
    #if the mode is start, draw the elements from the class, MainMenu() 
    if mode == 'start':
        menu.draw()
    
    #if the mode is setting, draw the elements from the class, Settings() 
    if mode == 'settings':
        settings.draw()
        
    #if the mode is game, set the game state to start and draw the classes associated with the game
    if mode == 'game':
        gameBegins = True
        screen.blit(picture,(0,0))
        gameElements.draw()
        terrain.draw()
        btrap.draw()
        player.draw()
        bullet.draw()
        countdown.draw()
        mob.draw()
        
        #encrypted text
        screen.draw.text(binaryText, (WIDTH - 420, 40), fontsize=15, fontname="gothic")
        screen.draw.text(decrypt, (WIDTH - 420, 58), fontsize=11, color=(200, 200, 200), fontname="gothic")
        
    if mode == 'end':
        screen.blit(end,(0,0))
        deathScreen.draw()
        sounds.death.stop()
        sounds.playerdead.stop()
        sounds.splat.stop()
        sounds.counter.stop()
        sounds.claw.stop()
        sounds.pzdeath.stop()
        sounds.beartrap.stop()
        music.stop()
        sounds.pzombie.stop()
        
    
    
def update():
    global gameBegins
    '''Handles update logic for the game - player movement, actor generation, scrolling of game elements'''
    #if the game has started, perform the following commands
    if gameBegins == True:
        bullet.update()
        player.update()
        
        #if player has not been killed by trap or zombie, resume the game
        if btrap.deathFreeze == False and mob.deathFreeze == False:
            #update the zombie, trap player and countdown
            mob.update()
            btrap.update(player.soldier)
            player.gravity()
            countdown.update()
            
            #generates random trap
            btrap.generate()

            #generates random zombie
            mob.generate()
            
            #sets the scrolling speed of the game
            scrollSpeed = -7
            
            #move the traps and zombies horizontally based on the scroll speed
            btrap.trap.x += scrollSpeed
            mob.zombie.x += scrollSpeed

            #updates the ground
            terrain.update()
            
         
            
def main():
    global gameBegins, mode, binaryText, decrypt, deathScreen, menu, settings, gameElements, terrain, btrap, player, mob, bullet, countdown
    '''Main function of the game - used to set the start and to reset the game'''
    gameBegins = False
    mode = 'start'
    binaryText = "0100100001100101011011000110110001101111"
    decrypt = "PRESS ENTER TO DECRYPT"
    menu = MainMenu()
    settings = Settings()
    gameElements = GameElements()
    terrain = Ground()
    btrap = Trap()
    player = Soldier()
    mob = Zombie()
    bullet = Bullet()
    countdown = Timer()
    deathScreen = DeathScreen()
    sounds.explosion.stop()
    sounds.angry.stop()
    music.play('title')
    music.set_volume(1.5)

                  
main()
pgzrun.go()


 