#import libraries
import pygame, os, sys, random, time
from pygame.locals import *

# Initialize the game engine
pygame.init()

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
        self.speed=random.randrange(1,10)
        super(Robot, self).__init__(filename)
    def hunt(self):
        #for treasure in treasure_list:
        try:
            target = treasure_list.sprites()[0]
            try:
                for treasure in treasure_list:
                    if treasure.value == wish_list[0]:
                        target=treasure
                        break
            except IndexError:
                pass
    
            if abs(self.rect.x - target.rect.x)>=self.speed:
                if self.rect.x > target.rect.x:
                    self.rect.x -=self.speed
                elif self.rect.x < target.rect.x:
                    self.rect.x +=self.speed
            else:
                self.rect.x += 0
            if abs(self.rect.y - target.rect.y)>=self.speed:
                if self.rect.y > target.rect.y:
                    self.rect.y -=self.speed
                elif self.rect.y < target.rect.y:
                    self.rect.y +=self.speed
            else:
                self.rect.y += 0
        except IndexError:
           pass
    def adjustSpeed(self, value):
        self.speed+=value
        if 10<self.speed:
            self.speed=10
        elif self.speed<1:
            self.speed=1
        
class Button():
    def __init__(self, x, y, width, height, text, color, active_color):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.text = text
        self.color=color
        self.active_color=active_color
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
        screen.blit(self.text, [self.x+(self.width/6), self.y+(self.height/5)])

class TreasureList():
    
    def __init__(self, x, y, width, height, text, color):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.text = text
        self.color=color
        
    def update(self, items):
        position=self.x+20        
        pygame.draw.rect(screen, self.color,(self.x,self.y,self.width,self.height))
        screen.blit(self.text, [self.x+(self.width/2), self.y+(self.height/4)])
        try:
                 for item in items:
                     if position <1000:
                         try:
                             temp = item.value
                         except AttributeError:
                             temp=item
                         if temp == 300:
                             color = (255,215,0)
                         elif temp == 200:
                             color = (160, 160, 160)
                         elif temp==100:
                             color = (184,134,11) 
                         pygame.draw.circle(screen, color,(position, self.y+self.height/2), self.height/3, 0)
                         position=position+self.height/3+20
        except IndexError:
                 pass

class Timer():
    def __init__(self, x, y, width, height, color, font):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color
        self.font=font
        self.frame_count=0
        self.total_seconds=-1
        self.seconds=0
        self.minutes=0
        
    def update(self):
        pygame.draw.rect(screen, (0,0,0),(self.x-2,self.y,60,40))
        if self.total_seconds is not 0:
            self.total_seconds = 60 - pygame.time.get_ticks()/1000# // 60
            if self.total_seconds < 0:
                self.total_seconds = 0
            self.minutes = self.total_seconds // 60
            self.seconds = self.total_seconds % 60
        time = "{00:00}:{01:02}".format(self.minutes, self.seconds)
        timer=self.font.render(time, True, (255,255,255))
        screen.blit(timer, [self.x+7, self.y+2])

        
# -------- Main Program -----------
def main():
    #set up variables
    traps_left=0

    #set up main screen size and color
    global screen, mouse
    screen=pygame.display.set_mode((1280,720))
    #screen.fill((200,200,200))
    
    #declare images
    treasure_map = pygame.image.load("map.png")
    global gold_small, silver_small, bronze_small
    gold_small=pygame.image.load("wishlist_gold.gif")
    silver_small=pygame.image.load("wishlist_silver.gif")
    bronze_small=pygame.image.load("wishlist_bronze.gif")

    #declare treasure types
    global gold, silver, bronze
    gold=Treasure(300, "treasure_gold.gif")
    silver=Treasure(200, "treasure_silver.gif")
    bronze=Treasure(100, "treasure_bronze.gif")
    
    
    #declare other stuff
    global Target, MouseDown, MousePressed, MouseReleased, running, pause
    Target=None # target of Drag/Drop
    MouseDown = False
    MousePressed = False
    MouseReleased = False
    running=True
    pause = False

    #declare fonts
    font = pygame.font.SysFont('Calibri', 25)
    system_font = pygame.font.Font('system.ttf', 25)
    digital_font = pygame.font.Font('digital.ttf', 35)
    button_font = pygame.font.SysFont('Calibri', 20, True, False)
    small_font = pygame.font.SysFont('Calibri', 15, True, False)


    #declare time variables
    clock = pygame.time.Clock()
    timer =  Timer( 1170, 280, 300, 100, (0,0,0), digital_font)

    #declare lists
    global all_sprites_list, trap_list, treasure_list, found_list, wish_list
    all_sprites_list = pygame.sprite.Group() # all sprites
    trap_list = pygame.sprite.Group() # all traps
    treasure_list = pygame.sprite.Group() # all treasures
    found_list=pygame.sprite.OrderedUpdates() # found treasures
    wish_list=[] # wish list
    
    # declare robot
    robot = Robot(0, "robot.gif")
    all_sprites_list.add(robot)
    robot.rect.x=random.randrange(900)
    robot.rect.y=random.randrange(100,650)

    #declare text
    text_add=font.render("Add treasure:", True, (154,154,154))
    text_score=font.render("Score:", True, (154,154,154))
    text_wishlist=font.render("Request:", True, (154,154,154))
    text_timer=font.render("Time left:", True, (154,154,154))
    text_speed=font.render("Adjust speed:", True, (154,154,154))
    
    #declare buttons
    goldButton= Button(1010, 130, 80, 30, button_font.render(" Gold", True, (184,134,11)) , (255,215,0), (255,235,0))
    silverButton= Button(1100, 130, 80, 30, button_font.render(" Silver", True, (105,105,105)), (160,160,160), (172,172,172))
    bronzeButton= Button(1190, 130, 80, 30, button_font.render("Bronze", True, (184,134,11)), (218,165,32), (238,195,52))

    goldwishlistButton= Button(1120, 190, 30, 30, button_font.render(" +", True, (184,134,11)) , (255,215,0), (255,235,0))
    silverwishlistButton= Button(1170, 190, 30, 30, button_font.render(" +", True, (105,105,105)) , (160,160,160), (172,172,172))
    bronzewishlistButton= Button(1220, 190, 30, 30, button_font.render(" +", True, (184,134,11)) , (218,165,32), (238,195,52))
    clearwishlistButton= Button(1110, 230, 150, 30, button_font.render("clear wishlist", True, (137,74,74)) , (161,161,161), (171,171,171))

    speedplusButton= Button(1180, 370, 30, 30, button_font.render(" +", True, (204, 204, 204)), (123, 123, 123), (102, 102, 102))
    speedminusButton= Button(1080, 370, 30, 30, button_font.render(" -", True, (204, 204, 204)), (123, 123, 123), (102, 102, 102))
    
    pauseButton= Button(1020, 660, 80, 30, button_font.render("Pause", True, (204, 204, 204)), (123, 123, 123), (102, 102, 102))    
    quitButton= Button(1180, 660, 80, 30, button_font.render("  Quit", True, (204, 0, 0)), (153, 0, 0), (102, 0, 0))

    FoundList=TreasureList( 0, 0, 1000, 20, small_font.render("found treasures", True, (100,100,100)), (60,60,60))
    WishList=TreasureList( 0, 700, 1000, 20, small_font.render("wishlist", True, (100,100,100)), (60,60,60))

    while running:
        #obtain mouse position
        mouse=pygame.mouse.get_pos()
        
        #update screen and screen items
        refreshScreen(treasure_map, text_add, text_score, text_wishlist, text_timer,text_speed)
        refreshButtons(robot, goldButton, silverButton, bronzeButton, goldwishlistButton, silverwishlistButton, bronzewishlistButton,clearwishlistButton, speedplusButton, speedminusButton, pauseButton, quitButton)
        displaySpeed(robot,button_font)
        displayScore(1100,60,system_font,robot)
        
        #select and move treasures
        selectObjects(treasure_list)

        timer.update()

        #pause function
        if pause is not True:
            #move robot
            robot.hunt()

        #check collision
        traps_hit_list = pygame.sprite.spritecollide(robot, trap_list, True)
        treasure_hit = pygame.sprite.spritecollide(robot, treasure_list, True)
        found_list.add(treasure_hit)

        #update GUI lists
        FoundList.update(found_list)
        WishList.update(wish_list)
        
        # Check the list of collisions.
        for trap in traps_hit_list:
            try:
                last = found_list.sprites()[-1]
                robot.score -= last.value
                found_list.remove(last)
            except IndexError:
                pass
        if traps_left==0:
            traps_left = generate_traps(10)
            
        for treasure in treasure_hit:
            robot.score += treasure.value
            try:
                if treasure.value == wish_list[0]:
                    wish_list.pop(0)
            except IndexError:
                pass
            

        clock.tick(60)
        checkForQuit()
        pygame.display.flip()
    return # End of main program


#functions
def displaySpeed(robot,font):
    text=font.render(str(robot.speed), True, (154,154,154))
    screen.blit(text,[1140,375])
def clear_wishlist():
    global wish_list
    wish_list= []
    
def pause_movement():
    global pause
    pause= not pause
    
def displayScore(x,y,digital_font,robot):
        #update and display score
        pygame.draw.rect(screen, (0,0,0),(x-2,y,100,24))
        score = digital_font.render(str(robot.score), True, (255,255,255))
        screen.blit(score, [x, y])
        
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
        treasure.rect.x = random.randrange(900)
        treasure.rect.y = random.randrange(650)
            
        # Add the block to the list of objects
        treasure_list.add(treasure)
        all_sprites_list.add(treasure)

def addToWishlist(item):
    wish_list.append(item)
        
def terminate():
    running = False
    pygame.quit()
    sys.exit()

def releasedMouse():
    for Event in pygame.event.get():
        if Event.type == pygame.MOUSEBUTTONUP:
            return True
    return False

def refreshScreen(background, text_add, text_score, text_wishlist, text_timer, text_speed):
        #clear screen
        screen.fill((200,200,200))
        # clear drawing screen
        screen.blit(background, (0,0))
        screen.blit(text_add, [1070,100])
        screen.blit(text_score, [1110,20])
        screen.blit(text_wishlist, [1010,190])
        screen.blit(text_timer, [1040,290])
        screen.blit(text_speed,[1080,340])
        # draw objects
        all_sprites_list.draw(screen)
        
def refreshButtons(robot, goldButton, silverButton, bronzeButton, goldwishlistButton, silverwishlistButton, bronzewishlistButton, clearwishlistButton, speedplusButton, speedminusButton, pauseButton, quitButton):
        #update buttons
        goldButton.update(generate_treasure, gold)
        silverButton.update(generate_treasure, silver)
        bronzeButton.update(generate_treasure, bronze)
        goldwishlistButton.update(addToWishlist, 300)
        silverwishlistButton.update(addToWishlist, 200)
        bronzewishlistButton.update(addToWishlist, 100)
        clearwishlistButton.update(clear_wishlist, None)
        speedplusButton.update(robot.adjustSpeed, 1)
        speedminusButton.update(robot.adjustSpeed, -1)
        pauseButton.update(pause_movement, None)
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
                if mouse[0]<960 and 680>mouse[1]>40:
                    Target.rect.x=mouse[0]-50 # move the item
                    Target.rect.y=mouse[1]-50
            if MouseReleased:
                Target=None # drop item
            return Target, MouseDown,MousePressed, MouseReleased

def checkForQuit():
     for Event in pygame.event.get():
        if Event.type == QUIT:
            terminate()
        if Event.type == KEYDOWN:
            if Event.key == K_ESCAPE:
                terminate()

if __name__ == '__main__':
    main() # Execute main function
