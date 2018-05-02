'''
Game.py

Actually implements the game
Lukas Peraza, 2015 for 15-112 Pygame Lecture
'''
import pygame
from Ship import Ship
from Ball import Ball
from Bullet import Bullet
from Eat import Eat
from pygamegame import PygameGame
import random
import socket
from _thread import *
from queue import Queue


HOST = ''
PORT = 50014

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

server.connect((HOST,PORT))
print("connected to server")

def handleServerMsg(server, serverMsg):# rohan v's code
  server.setblocking(1)
  msg = ""
  command = ""
  while True:
    msg += server.recv(10).decode("UTF-8")
    command = msg.split("\n")
    while (len(command) > 1):
      readyMsg = command[0]
      msg = "\n".join(command[1:])
      serverMsg.put(readyMsg)
      command = msg.split("\n")


class Game(PygameGame):
    
    def init(self):
        self.mode='startingScreen'
        self.me = [self.width/2, self.height/2] 
        #send this position as the message
        self.otherStrangers = [] #[(x,y),size]
        self.balls=[]
        #makeBalls(self.balls)
        # set up the colors
        BLACK = (  0,   0,   0)
        WHITE = (255, 255, 255)
        PINK   = (255,192,203)
        GREEN = (  0, 255,   0)
        BLUE  = (  0,   0, 255)
        self.colors=[BLACK,WHITE,PINK,GREEN,BLUE] 
        self.rows=50
        self.cols=50
        self.mysize=2
        self.offx = -500
        self.offy = -500
        self.serverMsg=serverMsg
        
        
        self.isGameOver=False
        self.bgColor = (255, 255, 255)
        Ship.init()
        ship = Ship(self.width / 2, self.height / 2)
        self.shipGroup = pygame.sprite.GroupSingle(ship)

        Ball.init()
        self.balls = pygame.sprite.Group()
        for i in range(100):
            x = random.randint(self.offx, self.width-self.offx)
            y = random.randint(self.offy, self.height-self.offy)
            self.balls.add(Ball(x, y))

        self.bullets = pygame.sprite.Group()

        Eat.init()
        self.eat = pygame.sprite.Group()

    #def getVel(
  
  
    def mousePressed(self,x,y):
        #zx        if pygame.mouse.get_pressed()==(1,0,0):
            if x>=0 and y>=0 and x<=80 and y<=50:
                self.mode='game'
        
    def keyPressed(self, code, mod):
        if self.mode=='startingScreen':
            return
        else:
            if code == pygame.K_SPACE:
                ship = self.shipGroup.sprites()[0]
                #self.bullets.add(Bullet(ship.x, ship.y, ship.angle))
            elif pygame.K_a:
                self.mode=='gameOver'

    def timerFired(self, dt):
        if self.mode=='startingScreen':
            return
        elif self.mode=='game':
            self.shipGroup.update(dt, self.isKeyPressed, self.width, self.height)
            self.balls.update(self.width, self.height)
            #self.bullets.update(self.width, self.height)
            self.eat.update(dt)
            
            ship = self.shipGroup.sprite
    
            if ((not ship.isInvincible()) and
                pygame.sprite.groupcollide(
                self.shipGroup, self.balls, False, True,
                pygame.sprite.collide_circle)):
                self.mysize+=1
                #self.balls.update2(self.mysize)
                x = random.randint(self.offx, self.width-self.offx)
                y = random.randint(self.offy, self.height-self.offy)
                self.balls.add(Ball(x, y))
                
                #self.shipGroup.update2(self.mysize,self.mysize)
                #self.eat.add(Eat(ship.x, ship.y))
                
            for ball in self.balls:
                pass
                
            vel= self.balls[0].velocity
            dx,dy=self.me[0]+vel[0]    ,self.me[1]+vel[1]
            msg = "%d %d\n" % (dx, dy)
            print("sending: ", msg)
            data.server.send(msg.encode())
            '''
            if ((not ship.isInvincible()) and
                pygame.sprite.groupcollide(
                self.shipGroup, self.otherStrangers, False, False,
                pygame.sprite.collide_circle)):
                    #85%
                    if 0.85*self.mysize>=self.otherStrangers[1]:
                        pygame.sprite.groupcollide(
                        self.shipGroup, self.otherStrangers, False, True,
                        pygame.sprite.collide_circle))
                    elif 0.85*self.otherStrangers[1]>=self.mysize:
                        pygame.sprite.groupcollide(
                        self.shipGroup, self.otherStrangers, True,False,
                        pygame.sprite.collide_circle))
                        self.mode='gameOver'
            '''
            if (serverMsg.qsize() > 0):#rohan v's
                msg = serverMsg.get(False)
            try:
                print("recieved: ", msg)
                if msg.startswith("newPlayer"):
                    msg = msg.split()
                    newPID = int(msg[1])
                    x = int(msg[2])
                    y = int(msg[3])
                    self.otherStrangers.append([x, y, newPID])
                elif msg.startswith("playerMoved"):
                    msg = msg.split()
                    PID = int(msg[1])
                    dx = int(msg[2])
                    dy = int(msg[3])
                for creeper in self.otherStrangers:
                    if creeper[2] == PID:
                        creeper[0] += dx * 5
                        creeper[1] += dy * 5
                        break
            except:
                print("failed")
            serverMsg.task_done()
            #if me is eaten by a stranger then isGameOver=True
        elif self.mode=='gameOver':
            return
    '''
    def drawLines(canvas,data,size=5):
        pass
        wid=8*size #fix this later according to the size of me
        for i in range(data.rows):
            for j in range(data.cols):
                canvas.create_rectangle(i*wid+data.offx-1000,j*wid+data.offy-1000,i*wid+wid+data.offx-1000,j*wid+wid+data.offy-1000)#fill=random.choice(data.colors))
    '''
    
    def drawScore(self,screen):
        #http://stackoverflow.com/questions/10077644/python-display-text-w-font-color
        # render text
        myfont = pygame.font.SysFont("monospace", 25)
        label = myfont.render("Your Size:%d" %self.mysize, 1, (0,0,0))
        label1= myfont.render("%d" %self.mysize, 1, (0,0,0))
        screen.blit(label, (5,5))
        screen.blit(label1, (self.width/2-5,self.height/2-10))
        #pygame.draw.circle(screen,RED ,(self.width//2,self.height//2),10)
        
    def drawBox(self,screen):
        pygame.draw.rect(screen, (0,0,0),(self.offx,self.offy, self.width-self.offx,self.height-self.offy),15)
        
    def drawStartingScreen(self,screen):
        #image = pygame.image.load('images/agario.png').convert_alpha()
        myfont = pygame.font.SysFont("monospace", 25)
        label = myfont.render("PLAY!", 1, (0,0,0))
        screen.blit(label, (5,5))
    
    def drawEndingScreen(self,screen):
        myfont = pygame.font.SysFont("monospace", 25)
        label = myfont.render("GAME OVER!", 1, (0,0,0))
        screen.blit(label, (100,100))
        label1 = myfont.render("Your Score:%d" %self.mysize, 1, (0,0,0))
        
        screen.blit(label1, (self.width/2,self.height/2))
        
    def drawOthers(self,screen,other):
        for creeper in other:
            pygame.draw.circle(screen,random.choice(self.colors),(other[0][0],other[0][1]),20)
        
        
    def redrawAll(self, screen):
        if self.mode=='startingScreen':
            self.drawStartingScreen(screen)
        elif self.mode=='game' or self.mode=='gameOver':
            self.drawBox(screen)
            self.balls.draw(screen)
            self.bullets.draw(screen)
            self.shipGroup.draw(screen)
            self.eat.draw(screen)
            self.drawScore(screen)
            self.drawOthers(screen,self.otherStrangers)
            self.drawBox(screen)
            if self.mode=='gameOver':
                self.drawEndingScreen(screen)
        

serverMsg = Queue(100) #rohan v's? not exactly but still
start_new_thread(handleServerMsg, (server, serverMsg))
#Game(500,500).run()
Game(500,500).run(serverMsg, server)
