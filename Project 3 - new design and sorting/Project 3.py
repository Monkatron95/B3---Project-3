#import libraries
import pygame, os, sys, random, time, copy
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
        self.treasuresound.set_volume(0.3)
        self.trapsound= pygame.mixer.Sound("resources/sounds/trap.ogg")
        self.trapsound.set_volume(0.5)
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
                
                if self.score > 0:
                    sort_list.pop(-1)
                    found_list.remove(last)
            except IndexError:
                pass
            traps_left -=1
            
        if traps_left==0:
            traps_left = generate_traps(10)
            
        for treasure in treasure_hit:
            self.treasuresound.play()
            self.score += treasure.value
            sort_list.append(treasure.value)
            print sort_list
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
        self.clicksound=pygame.mixer.Sound("resources/sounds/button.ogg")
        self.clicksound.set_volume(0.5)
    #def 
    def update(self, action, condition):
        self.text_full= self.font.render(self.text, True, self.text_color)
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
        pygame.draw.rect(screen, (94, 9, 2), pygame.Rect(self.x,self.y,self.width,self.height), 2)          

########################################################
def LuckySearch():

    j1 = random.randint(0,4)
    j2 = random.randint(0,4)
    j3 = random.randint(0,4)
    
    
    #ColourChange(j1, Bar3)
    #ColourChange(j2, Bar2)
    #ColourChange(j3, Bar1)
    
  
    if j1 == j2 == j3:
        print 'jackpot'        

    elif j1== j2 or j2 == j3:
        print '2 in a row'

    else:
        print 'unlucky'
        
    #time.sleep(0.5)
    #canvas.update()
    
    #reset(Bar1, Bar2, Bar3)
###################################################       
LuckySearch()           

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
        pygame.draw.rect(screen, (94,9,2),(self.x-2,self.y,60,40))
        if self.total_seconds == 0:
            global pause , running
            pause=True
            running=False
            s = pygame.Surface((1280, 720), pygame.SRCALPHA)
            s.fill((200,200,200,128))                        
            screen.blit(s, (0,0))
            pygame.mixer.music.pause()
        elif self.total_seconds is not 0:
            self.total_seconds = 60 - (pygame.time.get_ticks()-self.start_time-self.accumulated_time)/1000# // 60
            if self.total_seconds < 0:
                self.total_seconds = 0
            self.minutes = self.total_seconds // 60
            self.seconds = self.total_seconds % 60
        time = "{00:00}:{01:02}".format(self.minutes, self.seconds)
        timer=self.font.render(time, True, (255,207,27))
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
        self.playbutton=Button(self.x+5, self.y+self.height/2 ,35, 30, "play", (94, 9, 2), 12, (220, 200,160), (160, 130, 90))
        self.stopbutton=Button(self.x+45, self.y+self.height/2 ,35, 30,"stop", (94, 9, 2), 12, (220, 200, 160), (160, 130, 60))
        self.pausebutton=Button(self.x+85, self.y+self.height/2 ,35, 30,"pause", (94, 9, 2), 12, (220, 200, 160), (160, 130, 90))
        self.prevbutton=Button(self.x+125, self.y+self.height/2 ,35, 30, "prev", (94, 9, 2), 12, (220, 200, 160), (160, 130, 90))
        self.nextbutton=Button(self.x+165, self.y+self.height/2 ,35, 30, "next",(94, 9, 2), 12, (220, 200, 160), (160, 130, 90))
        pygame.mixer.music.set_volume(0.5)
        self.volume_bar=volumeBar(self.x, self.y+self.height-5, self.width, 5, (123, 123, 123), 0.5)
        self.SONG_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.SONG_END)
    def update(self):
        pygame.draw.rect(screen, self.color,(self.x,self.y,self.width,self.height))
        self.volume_bar.update()
        songdisplay=self.display_font.render(self.playlist[self.currentsong], True, (94, 9, 2))
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
            pygame.draw.rect(screen, (94, 9, 2),(self.x,self.y,self.value,self.height))
            
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
        score = self.font.render(str(value), True, (255,207,27))
        screen.blit(score, [self.x, self.y])
            
# -------- Main Program -----------
def main():
    #clear screen
    screen.fill((84,9,2))
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
    global timer
    timer =  Timer( 1170, 390, 300, 100, (0,0,0))
    timer.start_time=pygame.time.get_ticks()
    #declare lists
    global all_sprites_list, trap_list, treasure_list, found_list, wish_list, sort_list
    all_sprites_list = pygame.sprite.Group() # all sprites
    trap_list = pygame.sprite.Group() # all traps
    treasure_list = pygame.sprite.Group() # all treasures
    found_list=pygame.sprite.OrderedUpdates() # found treasures
    wish_list=[] # wish list
    sort_list = []
    
    # declare robot
    robot = Robot(0, "resources/images/robot.gif")
    all_sprites_list.add(robot)
    robot.rect.x=random.randrange(40, 900)
    robot.rect.y=random.randrange(100,650)

    #declare text
    text_add=font.render("Add treasure:", True, (94,9,2))
    text_score=font.render("Score:", True, (94,9,2))
    text_wishlist=font.render("Request:", True, (94,9,2))
    text_timer=font.render("Time left:", True, (94,9,2))
    text_speed=font.render("Adjust speed:", True, (94,9,2))

    
    
    #declare buttons
    goldButton= Button(1035, 150, 65, 30, "Gold",(184,134,11), 20 , (255,215,0), (255,235,0))
    silverButton= Button(1105, 150, 65, 30, "Silver", (105,105,105), 20 , (160,160,160), (172,172,172))
    bronzeButton= Button(1175, 150, 65, 30, "Bronze",(184,134,11), 20 , (218,165,32), (238,195,52))

    goldwishlistButton= Button(1070, 220, 30, 30, "+", (184,134,11), 20  , (255,215,0), (255,235,0))
    silverwishlistButton= Button(1120, 220, 30, 30, "+", (105,105,105), 20  , (160,160,160), (172,172,172))
    bronzewishlistButton= Button(1170, 220, 30, 30, "+", (184,134,11), 20  , (218,165,32), (238,195,52))
    clearwishlistButton= Button(1060, 260, 150, 30, "clear wishlist",(137,74,74), 20  , (161,161,161), (171,171,171))

    speedplusButton= Button(1180, 350, 30, 30, "+", (204, 204, 204), 20 , (123, 123, 123), (102, 102, 102))
    speedminusButton= Button(1080, 350, 30, 30,  "-", (204, 204, 204), 20 , (123, 123, 123), (102, 102, 102))
    
    pauseButton= Button(1040, 660, 80, 30, "Pause", (204, 204, 204), 20 , (123, 123, 123), (102, 102, 102))
    menuButton= Button(1045, 570, 180, 30, "Main Menu  ", (94, 9, 2), 20 , (160, 130, 90), (220, 200, 160))
    resetButton= Button(1045, 610, 180, 30, "Reset", (94, 9, 2), 20 , (160, 130, 90), (220, 200, 160)) 
    quitButton= Button(1150, 660, 80, 30, "Quit", (204, 0, 0), 20 , (153, 0, 0), (102, 0, 0))

    FoundList=TreasureList( 23, 30, 953, 20, small_font.render("found treasures", True, (100,100,100)), (94,9,2))
    WishList=TreasureList( 23, 675, 953, 20, small_font.render("wishlist", True, (100,100,100)), (94,9,2))

    gambleButton= Button(1020, 300, 240, 30, "Gamble", (204, 204, 204), 20 , (123, 123, 123), (102, 102, 102))    

    musicPlayer=music_player(1035, 450, 205, 100, (160,130,90))
    score=scoreboard(1110,70, 100, 24)
    bg=Block("resources/images/border1.gif")
    bg.rect.x = 0
    bg.rect.y = 0
    all_sprites_list.add(bg)

    border=Block("resources/images/border.gif")
    border.rect.x = 1035
    border.rect.y = 62
    all_sprites_list.add(border)
    while running:

        #update screen and screen items
        refreshScreen(treasure_map)#, text_add, text_score, text_wishlist, text_timer,text_speed)
        refreshButtons(robot, timer, goldButton, silverButton, bronzeButton, goldwishlistButton, silverwishlistButton, bronzewishlistButton,clearwishlistButton, speedplusButton, speedminusButton, pauseButton, menuButton,resetButton, quitButton, gambleButton)
        writeText(text_add, text_score, text_wishlist, text_timer, text_speed)
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
    select_order()
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
    
    global MouseDown, MousePressed, MouseReleased
    MouseDown = False
    MousePressed = False
    MouseReleased = False

    #main()
    while True:
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
    startButton= Button(80, 650, 100, 30, "Start",(204, 204, 204),20, (123, 123, 123), (34,139,34))
    quitButton= Button(1100, 650, 100, 30, "Quit",(204, 204, 204),20, (123, 123, 123), (128,0,0))
    while True:
        screen.fill((200,200,200))
        startButton.update(main, None)
        quitButton.update(terminate, None)
        checkForEvents(None)
        clock.tick(60)
        pygame.display.flip()
    return

def select_order():
    selecting=True
    global a, d
    font = pygame.font.SysFont('Calibri', 60)
    text_title=font.render("Select a sorting order:", True, (154,154,154))
    quitButton= Button(1150, 525, 100, 30, "Quit",(204, 0, 0), 20 , (153, 0, 0), (102, 0, 0))
    ascendingButton= Button(250, 350, 200, 50, "Ascending ",(204, 204, 204),30, (123, 123, 123), (138,43,226))
    descendingButton= Button(830, 350, 200, 50, "Descending ",(204, 204, 204),30, (123, 123, 123), (75,0,130)) 
    while True:
        pygame.draw.rect(screen, (200,200,200),(0,150,1280,420))
        #update text
        screen.blit(text_title,[370,200])
        quitButton.update(terminate, None)
        a= True
        ascendingButton.update(select_sorting, "a")
        a= False
        descendingButton.update(select_sorting, "d")
        checkForEvents(None)
        clock.tick(60)
        pygame.display.flip()


def select_sorting(option):
    global selecting , order, sort_list
    order=option
    font = pygame.font.SysFont('Calibri', 60)
    text_title=font.render("Select a sorting algorithm:", True, (154,154,154))
    quitButton= Button(1150, 525, 100, 30, "Quit",(204, 0, 0), 20 , (153, 0, 0), (102, 0, 0))
    bubble_sortButton= Button(80, 325, 200, 50, "Bubble Sort",(204, 204, 204),30, (123, 123, 123), (138,43,226))
    merge_sortButton= Button(320, 325, 200, 50, "Merge Sort",(204, 204, 204),30, (123, 123, 123), (75,0,130))
    while True:
        pygame.draw.rect(screen, (200,200,200),(0,150,1280,420))
        #update text
        screen.blit(text_title,[300,200])
        quitButton.update(terminate, None)
        if a==True:
            sort_list = bubbleSortAscending(sort_list)
        else:
            sort_list = bubbleSortDescending(sort_list)
        
        bubble_sortButton.update(sort, bubble_sortButton.text)
        if a:
            sort_list=mergesortAscending(sort_list)
        else:
            sort_list=mergesortDescending(sort_list)
        merge_sortButton.update(sort, merge_sortButton.text)
        
        checkForEvents(None)
        clock.tick(60)
        pygame.display.flip()

def sort(sort_type):
    global sorting, sort_list
    sorting=True
    
    
    
    
    
    
    small_font = pygame.font.SysFont('Calibri', 20, True, False)
    font = pygame.font.SysFont('Calibri', 60)
    text_title=font.render(sort_type, True, (154,154,154))
    quitButton= Button(1150, 525, 100, 30, "Quit",(204, 0, 0), 20 , (153, 0, 0), (102, 0, 0))
    backButton= Button(130, 525, 100, 30, "Back",(204, 204, 204),20, (123, 123, 123), (70,130,180))
    while sorting:
        pygame.draw.rect(screen, (200,200,200),(0,150,1280,420))
        #update text
        screen.blit(text_title,[1280/2-60*(len(sort_type)/4.8),200])
        SortList=TreasureList( 150, 300, 953, 30, small_font.render("sort treasures", True, (100,100,100)), (94,9,2))
        SortList.update(sort_list)
        
        quitButton.update(terminate, None)
        backButton.update(select_order, None)
        checkForEvents(None)
        clock.tick(60)
        pygame.display.flip()
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
    pygame.draw.rect(screen, (180,180,180),(1110,350,70,30))
    text=font.render(str(robot.speed), True, (94,9,2))
    screen.blit(text,[1140,355])
    
def clear_wishlist():
    global wish_list
    wish_list= []
    
def pause_movement(pauseButton):
    global pause
    if pause:
        pauseButton.text="Pause"
        timer.accumulated_time+= pygame.time.get_ticks() - timer.pause_time
    else:
        pauseButton.text="Resume  "
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
        trap.rect.x = random.randrange(40, 900)
        trap.rect.y = random.randrange(40, 600)
            
        # Add the block to the list of objects
        trap_list.add(trap)
        all_sprites_list.add(trap)
    return number

def generate_treasure(treasureType):
    #for i in range(number):
        treasure = Treasure(treasureType.value, treasureType.filename)

        # Set a random location for the block
        treasure.rect.x = random.randrange(40, 900)
        treasure.rect.y = random.randrange(40, 600)
            
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
        screen.blit(text_add, [1070,120])
        screen.blit(text_score, [1110,40])
        screen.blit(text_wishlist, [1100,190])
        screen.blit(text_timer, [1040,400])
        screen.blit(text_speed,[1080,320])

        
def refreshButtons(robot, timer, goldButton, silverButton, bronzeButton, goldwishlistButton, silverwishlistButton, bronzewishlistButton, clearwishlistButton, speedplusButton, speedminusButton, pauseButton, menuButton,resetButton, quitButton, gambleButton):
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
        pauseButton.update(pause_movement, pauseButton)
        menuButton.update(main_menu, None)
        resetButton.update(main, None)
        quitButton.update(terminate, None)
        gambleButton.update(LuckySearch, None)
            
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
                if 60<mouse[0]<940 and 600>mouse[1]>100:
                    Target.rect.x=mouse[0]-50 # move the item
                    Target.rect.y=mouse[1]-50
            if MouseReleased:
                Target=None # drop item
def mergeAscending(left, right):
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

def mergeDescending(left, right):
    result = []
    i ,j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] > right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            
            j += 1
    result += left[i:]
    result += right[j:]
    return result

def mergesortAscending(A):
    if len(A) < 2:
        return A
    middle = len(A) / 2
    left = mergesortAscending(A[:middle])
    right = mergesortAscending(A[middle:])
    return mergeAscending(left, right)
def mergesortDescending(A):
    if len(A) < 2:
        return A
    middle = len(A) / 2
    left = mergesortDescending(A[:middle])
    right = mergesortDescending(A[middle:])
    return mergeDescending(left, right)

def bubbleSortAscending(alist):
    for passnum in range(len(alist)-1,0,-1):
        for i in range(passnum):
            if alist[i]>alist[i+1]:
                temp = alist[i]
                alist[i] = alist[i+1]
                alist[i+1] = temp
    return alist
def bubbleSortDescending(alist):
    for passnum in range(len(alist)-1,0,-1):
        for i in range(passnum):
            if alist[i]<alist[i+1]:
                t = alist[i]
                alist[i] = alist[i+1]
                alist[i+1] = t
    return alist

if __name__ == '__main__':
    main_menu()
