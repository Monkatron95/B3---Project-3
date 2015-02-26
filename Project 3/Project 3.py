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
        self.treasuresound= pygame.mixer.Sound("resources/sounds/treasure.ogg")
        self.trapsound= pygame.mixer.Sound("resources/sounds/trap.ogg")
        
    def hunt(self):
        self.checkForCollision()
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
            
    def checkForCollision(self):
        global traps_left
     
        #check collision
        traps_hit_list = pygame.sprite.spritecollide(self, trap_list, True)
        treasure_hit = pygame.sprite.spritecollide(self, treasure_list, True)
        found_list.add(treasure_hit)
        
        # Check the list of collisions.
        for trap in traps_hit_list:
            self.trapsound.play()
            try:
                last = found_list.sprites()[-1]
                self.score -= last.value
                found_list.remove(last)
            except IndexError:
                pass
            traps_left -=1
            
        if traps_left==0:
            traps_left = generate_traps(10)
            
        for treasure in treasure_hit:
            self.treasuresound.play()
            self.score += treasure.value
            try:
                if treasure.value == wish_list[0]:
                    wish_list.pop(0)
            except IndexError:
                pass  
        
class Button():
    def __init__(self, x, y, width, height, text, text_color, text_size, color, active_color):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.text = text
        self.text_color=text_color
        self.text_size=text_size
        self.color=color
        self.active_color=active_color
        self.font=pygame.font.SysFont('Calibri', self.text_size, True, False)
        self.text_full= self.font.render(self.text, True, self.text_color)
        self.clicksound=pygame.mixer.Sound("resources/sounds/button.ogg")
    #def 
    def update(self, action, condition):
        mouse=pygame.mouse.get_pos()
        if self.x+self.width > mouse[0] > self.x and self.y+self.height > mouse[1] > self.y:
            pygame.draw.rect(screen, self.active_color,(self.x,self.y,self.width,self.height))
            if mouseClick():
                self.clicksound.play()
                if condition is not None:
                    action(condition)
                else:
                    action()
        else:
            pygame.draw.rect(screen, self.color,(self.x,self.y,self.width,self.height))
        screen.blit(self.text_full, [self.x+(self.width/2-self.text_size*(len(self.text)/4.8)), self.y+(self.height/5)])
            

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
    def __init__(self, x, y, width, height, color):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color
        self.font=pygame.font.Font('resources/fonts/digital.ttf', 35)
        self.frame_count=0
        self.total_seconds=-1
        self.seconds=0
        self.minutes=0
        self.start_time=0
        self.pause_time=0
        self.accumulated_time=0
        
    def update(self):
        pygame.draw.rect(screen, (0,0,0),(self.x-2,self.y,60,40))
        if self.total_seconds == 0:
            global pause
            pause=True
        elif self.total_seconds is not 0:
            self.total_seconds = 60 - (pygame.time.get_ticks()-self.start_time-self.accumulated_time)/1000# // 60
            if self.total_seconds < 0:
                self.total_seconds = 0
            self.minutes = self.total_seconds // 60
            self.seconds = self.total_seconds % 60
        time = "{00:00}:{01:02}".format(self.minutes, self.seconds)
        timer=self.font.render(time, True, (255,255,255))
        screen.blit(timer, [self.x+7, self.y+2])


class music_player():
    
    def __init__(self, x, y, width, height, color):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color
        self.playlist=["Radioactive", "Fox", "Lucky"]
        self.currentsong=0
        self.display_font=pygame.font.SysFont('Calibri', 25)
        self.path="resources/music/"
        pygame.mixer.music.load(self.path+self.playlist[self.currentsong]+".ogg")
        #create buttons
        self.playbutton=Button(self.x+5, self.y+self.height/2 ,40, 30, "play", (204, 204, 204), 12, (123, 123, 123), (102, 102, 102))
        self.stopbutton=Button(self.x+55, self.y+self.height/2 ,40, 30,"stop", (204, 204, 204), 12, (123, 123, 123), (102, 102, 102))
        self.pausebutton=Button(self.x+105, self.y+self.height/2 ,40, 30,"pause", (204, 204, 204), 12, (123, 123, 123), (102, 102, 102))
        self.prevbutton=Button(self.x+155, self.y+self.height/2 ,40, 30, "prev", (204, 204, 204), 12, (123, 123, 123), (102, 102, 102))
        self.nextbutton=Button(self.x+205, self.y+self.height/2 ,40, 30, "next",(204, 204, 204), 12, (123, 123, 123), (102, 102, 102))
        pygame.mixer.music.set_volume(0.5)
        self.volume_bar=volumeBar(self.x, self.y+self.height-5, self.width, 5, (123, 123, 123), 0.5)
        self.SONG_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.SONG_END)
    def update(self):
        pygame.draw.rect(screen, self.color,(self.x,self.y,self.width,self.height))
        self.volume_bar.update()
        songdisplay=self.display_font.render(self.playlist[self.currentsong], True, (123, 123, 123))
        screen.blit(songdisplay, [self.x + self.width/2-5*len(self.playlist[self.currentsong]), self.y+self.height/5])
        #update buttons
        self.playbutton.update(self.play, None)
        self.stopbutton.update(self.stop, None)
        self.pausebutton.update(self.pause, None)
        self.prevbutton.update(self.prevSong, None)
        self.nextbutton.update(self.nextSong, None)
        
    def nextSong(self):
        if self.currentsong < len(self.playlist)-1:
            self.currentsong+=1
        else:
            self.currentsong=0
        pygame.mixer.music.load(self.path+self.playlist[self.currentsong]+".ogg")
        self.play()
        
    def prevSong(self):
        if self.currentsong > 0 :
            self.currentsong-=1
        else:
            self.currentsong=len(self.playlist)-1
        pygame.mixer.music.load(self.path+self.playlist[self.currentsong]+".ogg")
        self.play()
        
    def pause(self):
        pygame.mixer.music.pause()
        
    def stop(self):
        pygame.mixer.music.stop()

    def play(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(1)
        else:
            pygame.mixer.music.unpause()
            
class volumeBar():
    def __init__(self, x, y, width, height, color, value):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color
        self.value=value
        self.mouse=pygame.mouse.get_pos()
    def update(self):
        self.value=self.width*pygame.mixer.music.get_volume()
        self.changeWithClick()
        if self.width> self.value > 0:
            pygame.draw.rect(screen, (123, 123, 123),(self.x,self.y,self.value,self.height))
            
    def changeWithClick(self):
        self.mouse=pygame.mouse.get_pos()
        if self.x< self.mouse[0]<self.x+self.width and self.y<self.mouse[1]<self.y+self.height and mouseClick():
            x=self.mouse[0]-self.x
            self.value=x/1.0/self.width
            pygame.mixer.music.set_volume(self.value)

class scoreboard():
    def __init__(self, x, y, width, height):
        self.x=x
        self.y=y
        self.width=100
        self.height=24
        self.color=(0,0,0)
        self.value=0
        self.font = pygame.font.Font('resources/fonts/system.ttf', 25)
        
    def update(self,value):
        pygame.draw.rect(screen, self.color,(self.x-2,self.y,self.width,self.height))
        score = self.font.render(str(value), True, (255,255,255))
        screen.blit(score, [self.x, self.y])
            
# -------- Main Program -----------
def main():
    #clear screen
    screen.fill((200,200,200))
    #set up variables
    global traps_left
    traps_left=0

    #declare images
    treasure_map = pygame.image.load("resources/images/map.png")

    #declare treasure types
    global gold, silver, bronze
    gold=Treasure(300, "resources/images/treasure_gold.gif")
    silver=Treasure(200, "resources/images/treasure_silver.gif")
    bronze=Treasure(100, "resources/images/treasure_bronze.gif")
    
    
    #declare other stuff
    global Target, running, pause
    Target=None # target of Drag/Drop
    running=True
    pause = False

    #declare fonts
    font = pygame.font.SysFont('Calibri', 25)
    button_font = pygame.font.SysFont('Calibri', 20, True, False)
    small_font = pygame.font.SysFont('Calibri', 15, True, False)

    #declare time variables
    timer =  Timer( 1170, 280, 300, 100, (0,0,0))
    timer.start_time=pygame.time.get_ticks()
    #declare lists
    global all_sprites_list, trap_list, treasure_list, found_list, wish_list
    all_sprites_list = pygame.sprite.Group() # all sprites
    trap_list = pygame.sprite.Group() # all traps
    treasure_list = pygame.sprite.Group() # all treasures
    found_list=pygame.sprite.OrderedUpdates() # found treasures
    wish_list=[] # wish list
    
    # declare robot
    robot = Robot(0, "resources/images/robot.gif")
    all_sprites_list.add(robot)
    robot.rect.x=random.randrange(900)
    robot.rect.y=random.randrange(100,650)

    #declare text
    text_add=font.render("Add treasure:", True, (154,154,154))
    text_score=font.render("Score:", True, (154,154,154))
    text_wishlist=font.render("Request:", True, (154,154,154))
    text_timer=font.render("Time left:", True, (154,154,154))
    text_speed=font.render("Adjust speed:", True, (154,154,154))

    writeText(text_add, text_score, text_wishlist, text_timer, text_speed)
    
    #declare buttons
    goldButton= Button(1010, 130, 80, 30, "Gold",(184,134,11), 20 , (255,215,0), (255,235,0))
    silverButton= Button(1100, 130, 80, 30, "Silver", (105,105,105), 20 , (160,160,160), (172,172,172))
    bronzeButton= Button(1190, 130, 80, 30, "Bronze",(184,134,11), 20 , (218,165,32), (238,195,52))

    goldwishlistButton= Button(1120, 190, 30, 30, "+", (184,134,11), 20  , (255,215,0), (255,235,0))
    silverwishlistButton= Button(1170, 190, 30, 30, "+", (105,105,105), 20  , (160,160,160), (172,172,172))
    bronzewishlistButton= Button(1220, 190, 30, 30, "+", (184,134,11), 20  , (218,165,32), (238,195,52))
    clearwishlistButton= Button(1110, 230, 150, 30, "clear wishlist",(137,74,74), 20  , (161,161,161), (171,171,171))

    speedplusButton= Button(1180, 370, 30, 30, "+", (204, 204, 204), 20 , (123, 123, 123), (102, 102, 102))
    speedminusButton= Button(1080, 370, 30, 30,  "-", (204, 204, 204), 20 , (123, 123, 123), (102, 102, 102))
    
    pauseButton= Button(1020, 660, 80, 30, "Pause", (204, 204, 204), 20 , (123, 123, 123), (102, 102, 102))
    menuButton= Button(1020, 570, 240, 30, "Main Menu  ", (204, 204, 204), 20 , (123, 123, 123), (102, 102, 102))
    resetButton= Button(1020, 610, 240, 30, "Reset", (204, 204, 204), 20 , (123, 123, 123), (102, 102, 102)) 
    quitButton= Button(1180, 660, 80, 30, "Quit", (204, 0, 0), 20 , (153, 0, 0), (102, 0, 0))

    FoundList=TreasureList( 0, 0, 1000, 20, small_font.render("found treasures", True, (100,100,100)), (60,60,60))
    WishList=TreasureList( 0, 700, 1000, 20, small_font.render("wishlist", True, (100,100,100)), (60,60,60))

    musicPlayer=music_player(1015, 450, 250, 100, (172,172,172))
    score=scoreboard(1100,60, 100, 24)    
    while running:

        #update screen and screen items
        refreshScreen(treasure_map)#, text_add, text_score, text_wishlist, text_timer,text_speed)
        refreshButtons(robot, timer, goldButton, silverButton, bronzeButton, goldwishlistButton, silverwishlistButton, bronzewishlistButton,clearwishlistButton, speedplusButton, speedminusButton, pauseButton, menuButton,resetButton, quitButton)

        displaySpeed(robot,button_font)
        #update music player
        musicPlayer.update()
        
        #check for events
        MouseDown,MousePressed, MouseReleased = checkForEvents(musicPlayer)
        
        score.update( robot.score )
        
        #select and move treasures
        selectObjects(treasure_list)
               

        
        #pause function
        if pause is not True:
            #update timer
            timer.update()
            #move robot
            robot.hunt()
        
        #update GUI lists
        FoundList.update(found_list)
        WishList.update(wish_list)

        clock.tick(60)
        pygame.display.flip()
    return # End of main program

def main_menu(): # main menu
    global screen, clock
    screen=pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Treasure Hunter")
    clock = pygame.time.Clock()

    #text
    font = pygame.font.SysFont('Calibri', 100)
    text_title=font.render("Treasure Hunter 3.0", True, (154,154,154))
    #buttons
    startButton= Button(540, 340, 200, 60, "Start",(204, 204, 204),38, (123, 123, 123), (34,139,34))
    instructionsButton= Button(540, 420, 200, 60, "Instructions",(204, 204, 204),38, (123, 123, 123), (128,0,128))
    quitButton= Button(540, 500, 200, 60, "Quit",(204, 204, 204),38, (123, 123, 123), (128,0,0))
    not_done=True
    
    global MouseDown, MousePressed, MouseReleased
    MouseDown = False
    MousePressed = False
    MouseReleased = False

    #main()
    while not_done:
        screen.fill((200,200,200))

        #update text
        screen.blit(text_title,[250,140])

        #update buttons
        startButton.update(main, None)
        instructionsButton.update(instructions, None)
        quitButton.update(terminate, None)
        
        checkForEvents(None)
        clock.tick(60)
        pygame.display.flip()
    return

def instructions():
    global reading
    reading= True
    startButton= Button(80, 650, 100, 30, "Start",(204, 204, 204),20, (123, 123, 123), (34,139,34))
    quitButton= Button(1100, 650, 100, 30, "Quit",(204, 204, 204),20, (123, 123, 123), (128,0,0))
    while reading:
        screen.fill((200,200,200))
        startButton.update(main, None)
        quitButton.update(terminate, None)
        checkForEvents(None)
        clock.tick(60)
        pygame.display.flip()
    return
#functions

def checkForEvents(musicPlayer):
     global MouseDown,MousePressed, MouseReleased
     for Event in pygame.event.get():
        if Event.type == QUIT:
            terminate()
        if Event.type == KEYDOWN:
            if Event.key == K_ESCAPE:
                terminate()
        if Event.type == pygame.MOUSEBUTTONDOWN:
            MousePressed=True 
            MouseDown=True 
            MouseReleased=False
        if Event.type == pygame.MOUSEBUTTONUP:
            MousePressed=False
            MouseReleased=True
            MouseDown=False
        if musicPlayer is not None:
            if Event.type == musicPlayer.SONG_END:
                musicPlayer.nextSong()
     return MouseDown,MousePressed, MouseReleased
            
def displaySpeed(robot,font):
    pygame.draw.rect(screen, (180,180,180),(1110,370,70,30))
    text=font.render(str(robot.speed), True, (134,134,134))
    screen.blit(text,[1140,375])
    
def clear_wishlist():
    global wish_list
    wish_list= []
    
def pause_movement(timer):
    global pause
    if pause:
        timer.accumulated_time+= pygame.time.get_ticks() - timer.pause_time
    else:
        timer.pause_time = pygame.time.get_ticks()
    pause = not pause
    
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
        trap = Trap("resources/images/trap.gif")
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
    pygame.quit()
    sys.exit()
    
def refreshScreen(background):
        # clear drawing screen
        screen.blit(background, (0,0))
        # draw objects
        all_sprites_list.draw(screen)
        
def writeText(text_add, text_score, text_wishlist, text_timer, text_speed):
        #refresh text
        screen.blit(text_add, [1070,100])
        screen.blit(text_score, [1110,20])
        screen.blit(text_wishlist, [1010,190])
        screen.blit(text_timer, [1040,290])
        screen.blit(text_speed,[1080,340])

        
def refreshButtons(robot, timer, goldButton, silverButton, bronzeButton, goldwishlistButton, silverwishlistButton, bronzewishlistButton, clearwishlistButton, speedplusButton, speedminusButton, pauseButton, menuButton,resetButton, quitButton):
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
        pauseButton.update(pause_movement, timer)
        menuButton.update(main_menu, None)
        resetButton.update(main, None)
        quitButton.update(terminate, None)
            
def selectObjects(object_list):
            global Target, MouseDown, MousePressed, MouseReleased, running
            #obtain mouse position
            mouse=pygame.mouse.get_pos()
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


if __name__ == '__main__':
    main_menu()
