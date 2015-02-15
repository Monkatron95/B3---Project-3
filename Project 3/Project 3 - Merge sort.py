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
            if self.rect.x > treasure.rect.x:
                self.rect.x -=speed
            elif self.rect.x < treasure.rect.x:
                self.rect.x +=speed
            else:
                self.rect.x += 0
            if self.rect.y > treasure.rect.y:
                self.rect.y -=speed
            elif self.rect.y < treasure.rect.y:
                self.rect.y +=speed
            else:
                self.rect.y += 0
        except IndexError:
           pass
        
class Button():
    def __init__(self, screen, x, y, width, height, text, color, active_color, font,selected):
        self.screen=screen
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
    def update(self,mouse,treasure_type,screen):
        if self.x+self.width > mouse[0] > self.x and self.y+self.height > mouse[1] > self.y:
            pygame.draw.rect(self.screen, self.active_color,(self.x,self.y,self.width,self.height))
            if mouseClick():
                    generate_treasure(1, treasure_type)
        else:
            pygame.draw.rect(self.screen, self.color,(self.x,self.y,self.width,self.height))
        screen.blit(self.text, [self.x+(self.width/3), self.y+(self.height/3)])

              
# -------- Main Program -----------
def main():
    #set up variables
    traps_left=0

    #set up main screen size and color
    screen=pygame.display.set_mode((1280,720))
    screen.fill((200,200,200))
    
    #declare images
    treasure_map = pygame.image.load("map.png")

    #declare treasure types
    gold=Treasure(300, "treasure_gold.gif")
    silver=Treasure(200, "treasure_silver.gif")
    bronze=Treasure(100, "treasure_bronze.gif")
    
    #declare other stuff
    Target=None # target of Drag/Drop
    MouseDown = False
    MousePressed = False
    MouseReleased = False
    running=True
    font = pygame.font.SysFont('Calibri', 25, True, False)
    clock = pygame.time.Clock()

    #declare lists
    global all_sprites_list
    all_sprites_list = pygame.sprite.Group() # all sprites
    global trap_list
    trap_list = pygame.sprite.Group() # all traps
    global treasure_list
    treasure_list = pygame.sprite.Group() # all treasures
    global found_list
    found_list=pygame.sprite.OrderedUpdates() # found treasures
    global found
    found=[]
    # declare robot
    robot = Robot(0, "robot.gif")
    all_sprites_list.add(robot)
    
    #declare buttons
    goldButton= Button(screen, 1050, 30, 180, 70, font.render("Gold", True, (184,134,11)) , (255,215,0), (255,235,0), "arial", False)
    silverButton= Button(screen, 1050, 130, 180, 70, font.render("Silver", True, (105,105,105)), (160,160,160), (172,172,172), "arial", False)
    bronzeButton= Button(screen, 1050, 230, 180, 70, font.render("Bronze", True, (184,134,11)), (218,165,32), (238,195,52), "arial", False)
    
    # assign a numbe of randomly generated traps
    #generate_traps(10)
    
    p=340
    while running:
        
        refreshScreen(screen,treasure_map)
        mouse=pygame.mouse.get_pos()
        
        #print mouse
        traps_hit_list = pygame.sprite.spritecollide(robot, trap_list, True)
        treasure_hit = pygame.sprite.spritecollide(robot, treasure_list, True)
        
        found_list.add(treasure_hit)
        
        goldButton.update(mouse, gold,screen)
        silverButton.update(mouse, silver,screen)
        bronzeButton.update(mouse, bronze, screen)

        #update and display score
        score = font.render(str(robot.score), True, (0,100,0))
        screen.blit(score, [1100, 350])
        
        Target, MouseDown,MousePressed, MouseReleased = selectObjects(screen, mouse, Target, MouseDown,MousePressed, MouseReleased)
        
        #move robot
        robot.hunt(5)
        
        # Check the list of collisions.
        for trap in traps_hit_list:
            traps_left-=1
            print traps_left
            try:
                
                last = found_list.sprites()[-1]
                
                found_list.remove(last)
                p=p-50
                                    
                if robot.score > 0:
                    found.remove(last.value)

                robot.score -= last.value
                
                
            except IndexError:
                pass
        if traps_left==0:
            print "lol"
            traps_left = generate_traps(10)
           
        for treasure in treasure_hit:
            robot.score += treasure.value
            
            print( robot.score )
            p=p+50
           
            treasure.rect.x = 1050
            
            treasure.rect.y = p
            
           
            found.append(treasure.value)
            print found
            found = mergesort(found)
            
            print found
            
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




def generate_treasure(number, treasureType):
    for i in range(number):
        treasure = Treasure(treasureType.value, treasureType.filename)

        # Set a random location for the block
        treasure .rect.x = random.randrange(900)
        treasure .rect.y = random.randrange(650)
            
        # Add the block to the list of objects
        treasure_list.add(treasure)
        all_sprites_list.add(treasure)
        
def terminate():
    print "quit"
    running = False
    pygame.quit()
    sys.exit()

def releasedMouse():
    for Event in pygame.event.get():
        if Event.type == pygame.MOUSEBUTTONUP:
            return True
    return False

def refreshScreen(screen,treasure_map):
        #clear screen
        screen.fill((200,200,200))
        # clear drawing screen
        screen.blit(treasure_map, (0,0))
        #pygame.draw.rect(screen, (235, 235, 235) , [0, 0, 1000, 720])
        # draw objects
        all_sprites_list.draw(screen)
        found_list.draw(screen)

            
def selectObjects(screen, mouse, Target, MouseDown,MousePressed, MouseReleased):
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
                    for treasure in treasure_list: # search all items
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
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back
def merge(left, right):
    result = []
    i ,j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            
            j += 1
    result += left[i:]
    result += right[j:]
    return result

def mergesort(A):
    if len(A) < 2:
        return A
    middle = len(A) / 2
    left = mergesort(A[:middle])
    right = mergesort(A[middle:])
    return merge(left, right)
if __name__ == '__main__':
    main() # Execute main function
