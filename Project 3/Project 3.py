#import libraries
import pygame, os, sys, random, time, copy, math
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
        if filename is not None:
            self.image = pygame.image.load(filename).convert()
            self.image.set_colorkey((255,255,255))
            self.rect = self.image.get_rect()
        self.filename=filename
        
        # Set background color to be transparent. Adjust to WHITE if your
        # background is WHITE.
        

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        

class Sphere(Block): 

    def __init__(self, color, radius, location):
        super(Sphere, self).__init__(None)
        self.frame = pygame.Surface ((radius*2, radius*2))
        self.frame.fill ((200,200,200))
        pygame.draw.circle(self.frame, color, (radius, radius), radius) 
        self.rect = self.frame.get_rect()
        self.rect.topleft = location
        self.speed = [2,2]

    def moveSpheres(self, windowSize): 
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > windowSize[0]:
            self.speed[0] = -self.speed[0] 
        if self.rect.top < 0 or self.rect.bottom > windowSize[1]:
            self.speed[1] = -self.speed[1]

    def collide(self, group1):
        if pygame.sprite.spritecollide(self, group1, False):
            self.speed[0] = -self.speed[0]
            self.speed[1] = -self.speed[1]

class Bomb (Block):
    def __init__(self):
        super(Bomb, self).__init__("resources/images/bomb.gif")
        self.exists = False
        
    def update (self, robot):
        if self.exists:
            self.rect.y += self.speed
            hit = pygame.sprite.spritecollide(robot, bomb_list, True)
            if hit:
                robot.score=robot.score/2
            if self.rect.y>700:
                all_sprites_list.remove(self)
                self.exists=False
                
    def create(self):
        self.rect.x = random.randrange(100,900)
        self.rect.y = -100
        self.speed = random.randrange(1,10)
        self.exists = True
        all_sprites_list.add(self)
        bomb_list.add(self)
                
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
            target = self.radar()
            if target is not None:
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
        if traps_left==4:
            traps_left = traps_left + generate_traps(random.randint(2, 6))
        if traps_left==0:
            traps_left = generate_traps(10)
            
        for treasure in treasure_hit:
            self.treasuresound.play()
            if len(found_list)<35:
                found_list.add(treasure_hit)
                self.score += treasure.value
                try:
                    if treasure.value == wish_list[0]:
                        wish_list.pop(0)
                except IndexError:
                    pass
            else:
                print "max number of treasures reached"
                
    def checkWishList(self, value):
        if wish_list:
            if value != wish_list[0]:
                return False
        return True

    def wishExists(self):
        if wish_list:
            for treasure in treasure_list:
                if treasure.value == wish_list[0]:
                    return True
        return False
    
    def radar(self):
        target = None
        try:
            minimum_distance = None
            for treasure in treasure_list:
                    distance = math.sqrt(math.pow((treasure.rect.x-self.rect.x),2)+math.pow((treasure.rect.y-self.rect.y),2))
                    if (distance < minimum_distance or minimum_distance == None) and (self.checkWishList(treasure.value) or not self.wishExists()):
                            target=treasure
                            minimum_distance=distance

        except IndexError:
            pass
        return target
    
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
    
    #reset(Bar1, Bar2, Bar3)
###################################################       
  
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

class SortingList():
    def __init__(self, x, y, width, height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.gold=pygame.image.load("resources/images/treasure_gold_small.gif")
        self.silver=pygame.image.load("resources/images/treasure_silver_small.gif")
        self.bronze=pygame.image.load("resources/images/treasure_bronze_small.gif")
    def update(self, items):
        xpos=self.x+60
        ypos=self.y
        try:
                 for item in items:
                         if xpos > 1200:
                              ypos+=self.height+20
                              xpos=self.x+60
                         try:
                             temp = item.value
                         except AttributeError:
                             temp=item
                         if temp == 300:
                             screen.blit(self.gold ,(xpos,ypos))
                         elif temp == 200:
                             screen.blit(self.silver ,(xpos,ypos))
                         elif temp==100:
                             screen.blit(self.bronze ,(xpos,ypos))
                         xpos=xpos+65
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
            global pause , running
            pause=True
            s = pygame.Surface((1280, 720), pygame.SRCALPHA)
            s.fill((200,200,200,128))                        
            screen.blit(s, (0,0))
            pygame.mixer.music.pause()
            if found_list:
                select_order()
            else:
                failed()
        elif self.total_seconds is not 0:
            self.total_seconds = 60 - (pygame.time.get_ticks()-self.start_time-self.accumulated_time)/1000
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

class TrafficLight(Block):
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state
        self.black = (0, 0, 0)
        self.red = (255,0,0)
        self.dullred = (205,92,92)
        self.amber = (255,215,0)
        self.dullamber = (222,184,135)
        self.green = (50,205,50)
        self.dullgreen = (152,251,152)
        self.greenlight = self.green
        self.yellowlight=self.dullamber
        self.redlight=self.dullred
    def DrawTrafficLight(self, robot, timer):
        self.Light(robot, timer)
        pygame.draw.rect(screen, self.black, (self.x, self.y, 40, 89), 0)
        pygame.draw.circle(screen, self.redlight, (1020, 20), 12, 0)
        pygame.draw.circle(screen, self.yellowlight, (1020, 45), 12, 0)
        pygame.draw.circle(screen, self.greenlight, (1020, 70), 12, 0)
    def Light(self, robot, timer):
        global RedLight
        x = pygame.time.get_ticks()/1000
        if x==(random.randint(5, 17)):
             self.state = 2
             robot.speed = 1
        elif x==(random.randint(18, 34)):
            self.state = 3
        elif x==(random.randint(35, 48)):
            self.state = 4
            robot.speed = 1
        elif x==(random.randint(49, 60)):
            self.state = 5
        if self.state == 2:
            self.yellowlight= self.amber
            self.greenlight=self.dullgreen
        if self.state == 3:
            self.yellowlight = self.dullamber
            self.redlight = self.red
            RedLight = True
        if self.state == 4:
            self.yellowlight = self.amber
            RedLight = False
        if self.state == 5:
            self.redlight = self.dullred
            self.yellowlight = self.dullamber
            self.greenlight = self.green
            RedLight = False
        def DrawTrafficLight(self):
            black = (0, 0, 0)
            red = (255,0,0)
            dullred = (205,92,92)
            amber = (255,215,0)
            dullamber = (222,184,135)
            green = (50,205,50)
            dullgreen = (152,251,152)
            pygame.draw.rect(screen, black, (self.x, self.y, 40, 89), 0)
            pygame.draw.circle(screen, dullred, (1020, 20), 12, 0)
            pygame.draw.circle(screen, dullamber, (1020, 45), 12, 0)
            pygame.draw.circle(screen, green, (1020, 70), 12, 0)
            
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
    global Target, pause, RedLight
    Target=None # target of Drag/Drop
    pause = False
    RedLight = False

    #declare fonts
    font = pygame.font.SysFont('Calibri', 25)
    button_font = pygame.font.SysFont('Calibri', 20, True, False)
    small_font = pygame.font.SysFont('Calibri', 15, True, False)

    #declare time variables
    global timer
    timer =  Timer( 1170, 280, 300, 100, (0,0,0))
    timer.start_time=pygame.time.get_ticks()
    #declare lists
    global all_sprites_list, trap_list, treasure_list, found_list, wish_list, bomb_list
    all_sprites_list = pygame.sprite.Group() # all sprites
    trap_list = pygame.sprite.Group() # all traps
    treasure_list = pygame.sprite.Group() # all treasures
    found_list=pygame.sprite.OrderedUpdates() # found treasures
    bomb_list = pygame.sprite.Group()# all bombs
    wish_list=[] # wish list

    #declare traffic light
    Light1 = TrafficLight(1000,1,1)
    
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

    gambleButton= Button(1020, 560, 240, 30, "Gamble", (204, 204, 204), 20 , (123, 123, 123), (102, 102, 102)) 

    menuButton= Button(1020, 600, 240, 30, "Main Menu  ", (204, 204, 204), 20 , (123, 123, 123), (102, 102, 102))
    resetButton= Button(1020, 640, 240, 30, "Reset", (204, 204, 204), 20 , (123, 123, 123), (102, 102, 102))

    pauseButton= Button(1020, 680, 80, 30, "Pause", (204, 204, 204), 20 , (123, 123, 123), (102, 102, 102))
    quitButton= Button(1180, 680, 80, 30, "Quit", (204, 0, 0), 20 , (153, 0, 0), (102, 0, 0))

    FoundList=TreasureList( 0, 0, 1000, 20, small_font.render("found treasures", True, (100,100,100)), (60,60,60))
    WishList=TreasureList( 0, 700, 1000, 20, small_font.render("wishlist", True, (100,100,100)), (60,60,60))

    launchButton= Button(1020, 410, 240, 30, "Launch", (204, 204, 204), 20 , (123, 123, 123), (102, 102, 102))
    # declare Bomb
    bomb = Bomb()
    
    musicPlayer=music_player(1015, 450, 250, 100, (172,172,172))
    score=scoreboard(1100,60, 100, 24)
    
    while True:

        #update screen and screen items
        refreshScreen(treasure_map)#, text_add, text_score, text_wishlist, text_timer,text_speed)
        refreshButtons(robot, bomb, timer, goldButton, silverButton, bronzeButton, goldwishlistButton, silverwishlistButton, bronzewishlistButton,clearwishlistButton, speedplusButton, speedminusButton, launchButton, pauseButton, menuButton,resetButton, quitButton, gambleButton)

        displaySpeed(robot,button_font)
        #update music player
        musicPlayer.update()
        
        #check for events
        MouseDown,MousePressed, MouseReleased = checkForEvents(musicPlayer)
        
        score.update( robot.score )
        
        #select and move treasures
        selectObjects(treasure_list)

        #update GUI lists
        FoundList.update(found_list)
        WishList.update(wish_list)
        
        #pause function
        if pause is not True:
            #update timer
            timer.update()
            #update bomb
            bomb.update(robot)
            if RedLight is not True:
            #move robot
                robot.hunt()
            
        Light1.DrawTrafficLight(robot, timer) #Draws Traffic Light
        clock.tick(60)
        pygame.display.flip()
        
    return # End of main program

#other stages

def main_menu(): # main menu
    global screen, clock
    pygame.mixer.music.stop()
    screen=pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Treasure Hunter")
    clock = pygame.time.Clock()
    #sphere creation
    spheres = pygame.sprite.Group()
     
    amount = random.randint(5, 15)

    for i in range (amount):
        color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)) ##assign a random colour
        radius = random.randint(20, 30)
        x =random.randint(100, 1180)
        y =random.randint(100, 620)
        ball = Sphere(color, radius,(x,y))
        spheres.add(ball)
        
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

    while True:
        screen.fill((200,200,200))

        #move spheres
        for ball in spheres:
            ball.moveSpheres((1280,720))
            spheres.remove(ball)
            ball.collide(spheres)
            spheres.add(ball)
            screen.blit(ball.frame, ball.rect)
            
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

def failed():
    quitButton= Button(1150, 525, 100, 30, "Quit",(204, 0, 0), 20 , (153, 0, 0), (102, 0, 0))
    menuButton= Button(1000, 525, 100, 30, "Main Menu  ",(204, 204, 204), 18 , (123, 123, 123), (70,130,180))
    font = pygame.font.SysFont('Calibri', 50)
    text_title=font.render("Unfortunately the robot failed to retrieve any treasure", True, (128,0,0))
    pygame.draw.rect(screen, (200,200,200),(0,150,1280,420))
    screen.blit(text_title,[100,325])
    while True:
        quitButton.update(terminate, None)
        menuButton.update(main_menu, None)
        checkForEvents(None)
        clock.tick(60)
        pygame.display.flip()
        
def select_order():
    font = pygame.font.SysFont('Calibri', 60)
    text_title=font.render("Select a sorting order:", True, (154,154,154))
    quitButton= Button(1150, 525, 100, 30, "Quit",(204, 0, 0), 20 , (153, 0, 0), (102, 0, 0))
    ascendingButton= Button(250, 350, 200, 50, "Ascending ",(204, 204, 204),30, (123, 123, 123), (138,43,226))
    descendingButton= Button(830, 350, 200, 50, "Descending ",(204, 204, 204),30, (123, 123, 123), (75,0,130))
    global sorting_list
    sorting_list=[ ]
    simplifyList(found_list, sorting_list)
    while True:
        pygame.draw.rect(screen, (200,200,200),(0,150,1280,420))
        #update text
        screen.blit(text_title,[370,200])
        quitButton.update(terminate, None)
        ascendingButton.update(select_sorting, max)
        descendingButton.update(select_sorting, min)
        checkForEvents(None)
        clock.tick(60)
        pygame.display.flip()


def select_sorting(option):
    global selecting , order
    order=option
    font = pygame.font.SysFont('Calibri', 60)
    text_title=font.render("Select a sorting algorithm:", True, (154,154,154))
    quitButton= Button(1150, 525, 100, 30, "Quit",(204, 0, 0), 20 , (153, 0, 0), (102, 0, 0))
    bubble_sortButton= Button(80, 325, 200, 50, "Bubble Sort",(204, 204, 204),30, (123, 123, 123), (138,43,226))
    quick_sortButton= Button(320, 325, 200, 50, "Quick Sort",(204, 204, 204),30, (123, 123, 123), (75,0,130))
    insertion_sortButton= Button(560, 325, 200, 50, "Insertion Sort",(204, 204, 204),30, (123, 123, 123), (72,61,139))
    selection_sortButton= Button(800, 325, 200, 50, "Selection Sort",(204, 204, 204),30, (123, 123, 123), (106,90,205))
    merge_sortButton= Button(1040, 325, 200, 50, "Merge Sort",(204, 204, 204),30, (123, 123, 123), (147,112,219))
    while True:
        pygame.draw.rect(screen, (200,200,200),(0,150,1280,420))
        #update text
        screen.blit(text_title,[300,200])
        quitButton.update(terminate, None)
        bubble_sortButton.update(sort, (bubble_sortButton.text, "bubble", option))
        quick_sortButton.update(sort, (quick_sortButton.text, "quick", option))
        insertion_sortButton.update(sort, (insertion_sortButton.text, "insertion", option))
        selection_sortButton.update(sort, (selection_sortButton.text, "selection", option))
        merge_sortButton.update(sort, (merge_sortButton.text, "merge", option))
        checkForEvents(None)
        clock.tick(60)
        pygame.display.flip()

def sort(sort_type):
    isSorted=False
    sortingScreen=sorting_screen(sort_type[0],sort_type[2])
    while True:
        sortingScreen.update()
        time.sleep(1)
        if isSorted is not True:
            if sort_type[1] is "bubble":
                sortingScreen.bubble_sort(sorting_list,sort_type[2])
            elif sort_type[1] is "quick":
                sortingScreen.quick_sort(sorting_list,0,len(sorting_list)-1,sort_type[2] )
            elif sort_type[1] is "insertion":
                sortingScreen.insertion_sort(sorting_list,sort_type[2] )
            elif sort_type[1] is "selection":
                sortingScreen.selection_sort(sorting_list,sort_type[2] )
            elif sort_type[1] is "merge":
                sortingScreen.merge_sort(sorting_list,sort_type[2], 0, len(sorting_list)) 
            isSorted=True
            sortingScreen.update_status()
        else:
            sortingScreen.update()
        clock.tick(60)
        pygame.display.flip()
        
class sorting_screen():
    def __init__(self, title, order):
        self.title=title
        self.quitButton= Button(1150, 525, 100, 30, "Quit",(204, 0, 0), 20 , (153, 0, 0), (102, 0, 0))
        self.menuButton= Button(1000, 525, 100, 30, "Main Menu  ",(204, 204, 204), 18 , (123, 123, 123), (70,130,180))
        self.backButton= Button(30, 525, 100, 30, "Back",(204, 204, 204),20, (123, 123, 123), (70,130,180))
        self.display_sort = SortingList( 0, 330, 1280, 60)
        self.font = pygame.font.SysFont('Calibri', 60)
        self.text_title=self.font.render(self.title, True, (154,154,154))
        self.status_message_font=pygame.font.SysFont('Calibri', 20)
        self.status_message=self.status_message_font.render("sorting in progress", True, (128,0,0))
        if order == max:
            self.subtitle="ascending"
        else:
            self.subtitle="descending"
        self.text_subtitle=self.status_message_font.render(self.subtitle, True, (128,0,128))
        
    def update_status(self):
        self.status_message=self.status_message_font.render("sorting complete", True, (0,128,0))
        
    def update(self):
        pygame.draw.rect(screen, (200,200,200),(0,150,1280,420))
        #update text
        screen.blit(self.text_title,[1280/2-60*(len(self.title)/4.8),200])
        screen.blit(self.text_subtitle,[1280/2-20*(len(self.subtitle)/4.8),260])
        screen.blit(self.status_message,[1280/2-60,530])
        self.display_sort.update(sorting_list)
        self.quitButton.update(terminate, None)
        self.backButton.update(select_order, None)
        self.menuButton.update(main_menu, None)
        checkForEvents(None)
        clock.tick(60)
        pygame.display.flip()
        
    def bubble_sort(self,list, order):
            for passnum in range(len(list)-1,0,-1):
                for i in range(passnum):
                    if list[i]== order(list[i],list[i+1]):
                        list[i], list[i+1]= list[i+1], list[i]
                        self.update()
                        time.sleep(1)
            #self.update_status()
                    
    def quick_sort_partition(self, list, start, end, order):
        pivot = list[end]                          
        bottom = start-1                           
        top = end                                  
        done = 0
        while not done:                            

            while not done:                       
                bottom = bottom+1                  

                if bottom == top:                  
                    done = 1                       
                    break

                if list[bottom] == order(list[bottom], pivot):           
                    list[top] = list[bottom]       
                    break                          

            while not done:                   
                top = top-1           
                
                if top == bottom:               
                    done = 1                      
                    break

                if pivot==order(pivot, list[top]):        
                    list[bottom] = list[top]    
                    break                      

        list[top] = pivot
        self.update()
        time.sleep(1)
        return top                               


    def quick_sort(self, list, start, end, order):

            if start < end:                            
                split = self.quick_sort_partition(list, start, end, order)   
                self.quick_sort(list, start, split-1, order)       
                self.quick_sort(list, split+1, end, order)
            else:
                return
            
    def insertion_sort(self, list, order):
        for i in range(1, len(list)):
            j = i
            while j > 0 and list[j-1]==order(list[j], list[j-1]):
                list[j] ,list[j-1] = list[j-1], list[j]
                j -= 1
                self.update()
                time.sleep(1)
                
    def selection_sort(self, list, order):
       for fillslot in range(len(list)-1,0,-1):
           positionOfMax=0
           for location in range(1,fillslot+1):
               if list[location]==order(list[location],list[positionOfMax]):
                   positionOfMax = location
           list[fillslot], list[positionOfMax] = list[positionOfMax], list[fillslot]
           self.update()
           time.sleep(1)      
    
    def merge_sort(self, seq, order, start, end):
        if end-start > 1:
            middle = (start+end) // 2
            self.merge_sort(seq, order, start, middle)
            self.merge_sort(seq, order, middle, end)
            self.merge(seq, start, middle, middle, end,order)
            
    def merge(self, seq, left, leftEnd, right, rightEnd,order):
        while left<leftEnd and right<rightEnd:
            if seq[left]==order(seq[left], seq[right]):
                seq.insert(left, seq.pop(right))
                right += 1
                leftEnd += 1
                self.update()
                time.sleep(1) 
            else:
                left += 1
     
        
#functions

def simplifyList(a, b):
    for x in a:
        b.append(x.value)

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
      
def refreshButtons(robot, bomb, timer, goldButton, silverButton, bronzeButton, goldwishlistButton, silverwishlistButton, bronzewishlistButton, clearwishlistButton, speedplusButton, speedminusButton, launchButton, pauseButton, menuButton,resetButton, quitButton,gambleButton):
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
        launchButton.update(bomb.create, None)
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
                if mouse[0]<960 and 680>mouse[1]>40:
                    Target.rect.x=mouse[0]-50 # move the item
                    Target.rect.y=mouse[1]-50
            if MouseReleased:
                Target=None # drop item


if __name__ == '__main__':
    main_menu()
