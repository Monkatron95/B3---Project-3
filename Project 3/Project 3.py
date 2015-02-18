#import libraries
import pygame, os, sys, random, time
from pygame.locals import *

# Initialize the game engine
pygame.init()

#obtaining project root folder
path = sys.path[0]

#classes

class Block(pygame.sprite.Sprite):
    def __init__(self, filename):
        # Call the parent class (Sprite) constructor
        super(Block,self).__init__() 

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load(filename).convert()

        self.filename=filename
        
        # Set background color to be transparent. Adjust to WHITE if your
        # background is WHITE.
        self.image.set_colorkey((255,255,255))

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        
class Trap(Block):
    def __init__(self, filename):
        self.value=-50
        super(Trap, self).__init__(filename)

class Treasure(Block):
    def __init__(self, value, filename):
        self.value=value
        super(Treasure, self).__init__(filename)
                
class Robot(Block):
    def __init__(self, score,filename):
        self.score=score
        super(Robot, self).__init__(filename)
    def hunt(self, speed):
        #for treasure in treasure_list:
        try:
            treasure = treasure_list.sprites()[0]
            if abs(self.rect.x - treasure.rect.x)>=speed:
                if self.rect.x > treasure.rect.x:
                    self.rect.x -=speed
                elif self.rect.x < treasure.rect.x:
                    self.rect.x +=speed
            else:
                self.rect.x += 0
            if abs(self.rect.y - treasure.rect.y)>=speed:
                if self.rect.y > treasure.rect.y:
                    self.rect.y -=speed
                elif self.rect.y < treasure.rect.y:
                    self.rect.y +=speed
            else:
                self.rect.y += 0
        except IndexError:
           pass
        
class Button():
    def __init__(self, x, y, width, height, text, color, active_color, font,selected):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.text = text
        self.color=color
        self.active_color=active_color
        self.font=font
        self.selected=selected
    #def 
    def update(self, action, condition):
        if self.x+self.width > mouse[0] > self.x and self.y+self.height > mouse[1] > self.y:
            pygame.draw.rect(screen, self.active_color,(self.x,self.y,self.width,self.height))
            if mouseClick():
                if condition is not None:
                    action(condition)
                else:
                    action()
        else:
            pygame.draw.rect(screen, self.color,(self.x,self.y,self.width,self.height))
        screen.blit(self.text, [self.x+(self.width/3), self.y+(self.height/3)])

              
# -------- Main Program -----------
def main():
    #set up variables
    traps_left=0

    #set up main screen size and color
    global screen, mouse
    screen=pygame.display.set_mode((1280,720))
    screen.fill((200,200,200))
    
    #declare images
    treasure_map = pygame.image.load("map.png")

    #declare treasure types
    global gold, silver, bronze
    gold=Treasure(300, "treasure_gold.gif")
    silver=Treasure(200, "treasure_silver.gif")
    bronze=Treasure(100, "treasure_bronze.gif")
    
    #declare other stuff
    global Target, MouseDown, MousePressed, MouseReleased, running
    Target=None # target of Drag/Drop
    MouseDown = False
    MousePressed = False
    MouseReleased = False
    running=True
    font = pygame.font.SysFont('Calibri', 25, True, False)
    clock = pygame.time.Clock()

    #declare lists
    global all_sprites_list, trap_list, treasure_list, found_list
    all_sprites_list = pygame.sprite.Group() # all sprites
    trap_list = pygame.sprite.Group() # all traps
    treasure_list = pygame.sprite.Group() # all treasures
    found_list=pygame.sprite.Group() # found treasures
    
    # declare robot
    robot = Robot(0, "robot.gif")
    all_sprites_list.add(robot)
    
    #declare buttons
    goldButton= Button(1050, 30, 180, 70, font.render("Gold", True, (184,134,11)) , (255,215,0), (255,235,0), "arial", False)
    silverButton= Button(1050, 130, 180, 70, font.render("Silver", True, (105,105,105)), (160,160,160), (172,172,172), "arial", False)
    bronzeButton= Button(1050, 230, 180, 70, font.render("Bronze", True, (184,134,11)), (218,165,32), (238,195,52), "arial", False)
    quitButton= Button(1050, 630, 180, 70, font.render("Quit", True, (204, 0, 0)), (153, 0, 0), (102, 0, 0), "arial", False)


    

    while running:
        
        #obtain mouse position
        mouse=pygame.mouse.get_pos()
        
        #update screen and screen items
        refreshScreen(treasure_map)
        refreshButtons(goldButton, silverButton, bronzeButton, quitButton)

        #select and move treasures
        selectObjects(treasure_list)
        
        #move robot
        robot.hunt(5)

        #check collision
        traps_hit_list = pygame.sprite.spritecollide(robot, trap_list, True)
        treasure_hit = pygame.sprite.spritecollide(robot, treasure_list, True)
        found_list.add(treasure_hit)
        

        
        #update and display score
        score = font.render(str(robot.score), True, (0,100,0))
        screen.blit(score, [1100, 500])
        

        
        # Check the list of collisions.
        for trap in traps_hit_list:
            traps_left-=1
            print traps_left
            try:
                last = found_list.sprites()[0]
                robot.score -= last.value
                found_list.remove(last)
            except IndexError:
                pass
        if traps_left==0:
            traps_left = generate_traps(10)
            
        for treasure in treasure_hit:
            robot.score += treasure.value
            print( robot.score )
            
        pygame.display.flip()
        clock.tick(60)
        checkForQuit()
    return # End of main program


#functions
def mouseClick():
    for Event in pygame.event.get():
                if Event.type == pygame.MOUSEBUTTONDOWN:
                    return True
    return False
        
def generate_traps(number):
    for i in range(number):
        trap = Trap("trap.gif")
        # Set a random location for the block
        trap.rect.x = random.randrange(900)
        trap.rect.y = random.randrange(650)
            
        # Add the block to the list of objects
        trap_list.add(trap)
        all_sprites_list.add(trap)
    return number

def generate_treasure(treasureType):
    #for i in range(number):
        treasure = Treasure(treasureType.value, treasureType.filename)

        # Set a random location for the block
        treasure .rect.x = random.randrange(900)
        treasure .rect.y = random.randrange(650)
            
        # Add the block to the list of objects
        treasure_list.add(treasure)
        all_sprites_list.add(treasure)
        
def terminate():
    running = False
    pygame.quit()
    sys.exit()

def releasedMouse():
    for Event in pygame.event.get():
        if Event.type == pygame.MOUSEBUTTONUP:
            return True
    return False

def refreshScreen(background):
        #clear screen
        screen.fill((200,200,200))
        # clear drawing screen
        screen.blit(background, (0,0))
        #pygame.draw.rect(screen, (235, 235, 235) , [0, 0, 1000, 720])
        # draw objects
        all_sprites_list.draw(screen)
        
def refreshButtons(goldButton, silverButton, bronzeButton, quitButton):
        #update buttons
        goldButton.update(generate_treasure, gold)
        silverButton.update(generate_treasure, silver)
        bronzeButton.update(generate_treasure, bronze)
        quitButton.update(terminate, None)
            
def selectObjects(object_list):
            global Target, MouseDown, MousePressed, MouseReleased, running
            for Event in pygame.event.get():
                if Event.type == pygame.MOUSEBUTTONDOWN:
                    MousePressed=True 
                    MouseDown=True 
                    MouseReleased=False
                if Event.type == pygame.MOUSEBUTTONUP:
                    MousePressed=False
                    MouseReleased=True
                    MouseDown=False

            if MousePressed==True:
                if Target is None:
                    for treasure in object_list: # search all items
                            if treasure.rect.collidepoint(mouse):
                                Target=treasure # "pick up" item
            if MouseDown and Target is not None: # if dragging
                if mouse[0]<960:
                    Target.rect.x=mouse[0]-50 # move the item
                    Target.rect.y=mouse[1]-50
            if MouseReleased:
                Target=None # drop item
            return Target, MouseDown,MousePressed, MouseReleased

def checkForQuit():
    Event = pygame.event.wait ()
    if Event.type == QUIT:
        terminate()
    if Event.type == KEYDOWN:
        print Event.key
        if Event.key == K_ESCAPE:
            terminate()

if __name__ == '__main__':
    main() # Execute main function
