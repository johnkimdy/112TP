#Some of the pygame codes referenced from #https://github.com/Viliami/agario/blob/master/agar.py

import pygame
from Ship import Ship
from Ball import Cell
from Ball import Portal
from Ball import Piece
from Ball import Time
from Ball import AI
from pygamegame import PygameGame
from Camera import Camera
import random
import socket
from _thread import *
from queue import Queue

HOST = ''
PORT = 50013
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


colors_cells = [(236,232,254),(254,236,232),(131,146,159),(252,233,241),(163,145,147),(170,111,115),(246,224,181)]


pygame.init()  # inits from https://github.com/Viliami/agario/blob/master/agar.py
screen_width, screen_height = (800,500)
surface = pygame.display.set_mode((screen_width,screen_height))
t_surface = pygame.Surface((95,25),pygame.SRCALPHA) #transparent rect for score
t_lb_surface = pygame.Surface((155,278),pygame.SRCALPHA) #transparent rect for leaderboard
t_surface.fill((50,50,50,80))
t_lb_surface.fill((50,50,50,80))
pygame.display.set_caption("aesthetics.io")
cells = list()
portals= list()
times = list()
clock = pygame.time.Clock()
try:
    font = pygame.font.Font("cochin",20)
    big_font = pygame.font.Font("cochin",24)
except:
    print("Font file not found: Ubuntu-B.ttf")
    font = pygame.font.SysFont('Ubuntu',20,True)
    big_font = pygame.font.SysFont('Ubuntu',24,True)

def drawText(message,pos,color=(255,255,255)):
        surface.blit(font.render(message,1,color),pos)

otherStrangers = [] #[(x,y),size]
'''
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
        print(1)


        self.bgColor = (255, 255, 255)


    def mousePressed(self,x,y):
        #(x,y)=pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()==(1,0,0):
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
        print(1)
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


    def drawLines(canvas,data,size=5):
        pass
        wid=8*size #fix this later according to the size of me
        for i in range(data.rows):
            for j in range(data.cols):
                canvas.create_rectangle(i*wid+data.offx-1000,j*wid+data.offy-1000,i*wid+wid+data.offx-1000,j*wid+wid+data.offy-1000)#fill=random.choice(data.colors))




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

def drawOthers(screen,cam,other):
    for creeper in other:
       # pygame.draw.circle(screen,color,(creeper[0][0],creeper[0][1]),20)
        mass=1
        col = colors_cells[random.randint(0,len(colors_cells)-1)]
        zoom = cam.zoom
        x = cam.x
        y = cam.y
        print("creep coords ",creeper[0],creeper[1])
        pygame.draw.circle(surface,(col[0]-int(col[0]/3),int(col[1]-col[1]/3),int(col[2]-col[2]/3)),(int(creeper[0]*zoom+x),int(creeper[1]*zoom+y)),int((creeper[2]/2+3)*zoom))#int((blob.mass/2+3)*zoom))
        pygame.draw.circle(surface,col,(int(creeper[0]*zoom+cam.x),int(creeper[1]*zoom+cam.y)),int(creeper[2]/2*zoom))#int(blob.mass/2*zoom))

        if(len(self.name) > 0):
            fw, fh = self.font.size(self.name)
            drawText(self.surface,self.name,self.font, (self.x*cam.zoom+cam.x-int(fw/2),self.y*cam.zoom+cam.y-int(fh/2)),(50,50,50))



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
'''

#mine  I learned how to use fonts on https://www.pygame.org/docs/ref/font.html
def drawStartingScreen():
    myfont = pygame.font.SysFont("monospace", 40)
    myfont2 = pygame.font.SysFont("monospace", 80)
    play1 = myfont.render("PLAY!", 1, (255,192,203))
    col = colors_cells[random.randint(0,len(colors_cells)-1)]
    play2 = myfont.render("PLAY!", 1, (236,232,254))
    title = myfont2.render("a e s t h e t i c s . i o", 1, col)
    surface.fill((242,251,255))
    surface.blit(title, (screen_width/2-250,screen_height/2-100))
    surface.blit(play1, (screen_width/2-30,screen_height/2))
    (x,y)=pygame.mouse.get_pos()
    if (x>=screen_width//2-40 and y>=screen_height//2-20 and x<=screen_width//2+40 and y<=screen_height//2+20):
        surface.blit(play2, (screen_width/2-30,screen_height/2))

def drawWinScreen(): #mine
    myfont = pygame.font.SysFont("monospace", 40)
    myfont2 = pygame.font.SysFont("monospace", 80)
    play1 = myfont.render("You can stop eating now", 1, (255,192,203))
    title = myfont2.render("OK YOU WIN CHILL OUT", 1, (163,145,147))
    playagain=myfont.render("Play Again", 1, (246,224,181))
    playagain2=myfont.render("Play Again", 1, (131,146,159))
    surface.fill((242,251,255))
    surface.blit(title, (screen_width/2-320,screen_height/2-100))
    surface.blit(play1, (screen_width/2-165,screen_height/2))
    surface.blit(playagain, (screen_width/2-60,screen_height/2+100))
    (x,y)=pygame.mouse.get_pos()
    if (x>=screen_width//2-60 and y>=screen_height//2+100 and x<=screen_width//2+80 and y<=screen_height//2+120):
        surface.blit(playagain2, (screen_width/2-60,screen_height/2+100))


def drawEndingScreen():#mine
    myfont = pygame.font.SysFont("monospace", 40)
    myfont2 = pygame.font.SysFont("monospace", 80)
    play1 = myfont.render("Gotta be more fast", 1, (255,192,203))
    title = myfont2.render("GAME OVER", 1, (163,145,147))
    playagain=myfont.render("Play Again", 1, (246,224,181))
    playagain2=myfont.render("Play Again", 1, (131,146,159))
    surface.fill((242,251,255))
    surface.blit(title, (screen_width/2-180,screen_height/2-100))
    surface.blit(play1, (screen_width/2-125,screen_height/2))
    surface.blit(playagain, (screen_width/2-75,screen_height/2+100))
    (x,y)=pygame.mouse.get_pos()
    if (x>=screen_width//2-60 and y>=screen_height//2+100 and x<=screen_width//2+80 and y<=screen_height//2+120):
        surface.blit(playagain2, (screen_width/2-75,screen_height/2+100))


#spawnings referenced from the github
def spawn_cells(numOfCells):
    for i in range(numOfCells):
        cells.append(Cell(surface))

def spawn_portals(numOfPortals):
    for i in range(numOfPortals):
        portals.append(Portal(surface))

def spawn_time(numOfTimes):
    for t in range(numOfTimes):
        times.append(Time(surface))

ais=list()
def spawn_AIs(numOfAI):
    for a in range(numOfAI):
        ais.append(AI(surface,cells,portals))

def getDistance(pos1,pos2):
    x1,y1 = pos1
    x2,y2 = pos2
    diffX = x1-x2
    diffY = y1-y2

    return ((diffX**2)+(diffY**2))**(0.5)

def collisionDetection(others): #mineeee
    for other in others:
        if(getDistance((other.x,other.y),(blob.x,blob.y)) <= blob.mass/2):
            if other.mass>=1.15*blob.mass:
                other.mass+=blob.mass
                others.remove(cell)
                self.cell_list.append(Cell(self.surface))
            elif blob.mass>=1.15*other.mass:
                blob.mass+= other.mass


def draw_grid():#https://github.com/Viliami/agario/blob/master/agar.py
    for i in range(0,2001,25):
        pygame.draw.line(surface,(230,240,240),(0+camera.x,i*camera.zoom+camera.y),(2001*camera.zoom+camera.x,i*camera.zoom+camera.y),3)
        pygame.draw.line(surface,(230,240,240),(i*camera.zoom+camera.x,0+camera.y),(i*camera.zoom+camera.x,2001*camera.zoom+camera.y),3)
    myfont = pygame.font.SysFont("monospace", 50)
    play1 = myfont.render("Score 500 in a given time to win!", 1, (255,192,203))
    surface.blit(play1, ((blob.startX-50)*camera.zoom+camera.x,(blob.startY-20)*camera.zoom+camera.y))



def draw_HUD(time): #modified from https://github.com/Viliami/agario/blob/master/agar.py
    score=int(blob.mass*2)
    w,h = font.size("Score: "+str(score)+"/500 ")
    surface.blit(pygame.transform.scale(t_surface,(w,h)),(8,screen_height-30))

    #surface.blit(t_lb_surface,(screen_width-160,15))
    w1,h1 = font.size("Time: "+str(time)+" ")
    surface.blit(pygame.transform.scale(t_surface,(w1,h1)),(screen_width-90 ,8))
    drawText("Score: " + str(score)+"/500",(10,screen_height-30))
    if time<=5:
        drawText("Time: " + str(time),(screen_width-90 ,10),(255,0,0))
    else:
        drawText("Time: " + str(time),(screen_width-90 ,10))



def run(screen,playing,mode,ai,serverMsg=None, server=None): #input bool
    #this whole thing is mine
    isGameOver=False
    start_ticks=pygame.time.get_ticks()
    time1=30
    numOfAI=1
    spawn_AIs(numOfAI)
    while playing:
        if mode=="startingScreen":
            for event in pygame.event.get():
                if(event.type == pygame.KEYDOWN):
                    if(event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        quit()
                if(event.type == pygame.QUIT):
                    pygame.quit()
                    quit()

            drawStartingScreen()
            (x,y)=pygame.mouse.get_pos()
            if (x>=screen_width//2-40 and y>=screen_height//2-20 and x<=screen_width//2+40 and y<=screen_height//2+20):
                if pygame.mouse.get_pressed()==(1,0,0):
                    mode='game'
            pygame.display.flip()
            continue

        elif mode=="game":
            clock.tick(10000)
            for event in pygame.event.get():
                if(event.type == pygame.KEYDOWN):
                    if(event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        quit()
                    if(event.key == pygame.K_SPACE):
                        blob.split()
                    if(event.key == pygame.K_w):
                        blob.feed()
                if(event.type == pygame.QUIT):
                    pygame.quit()
                    quit()
            blob.move()


            #MINNEE
            if blob.collisionDetection():
                time1 += 5
            elif blob.collisionDetection()==False:
                mode="lose"
            camera.zoom = 100/(blob.mass)+0.3
            camera.center(blob)
            surface.fill((242,251,255))
            #surface.fill((0,0,0))
            draw_grid()
            for c in cells:
                c.draw(camera)
            for p in portals:
                p.draw(camera)
            for t in times:
                t.draw(camera)
            for aI in ai:
                aI.draw(camera)
                aI.moveAI(blob)
                aI.collisionDetection()

            blob.draw(camera)


            #timer by http://stackoverflow.com/questions/30720665/countdown-timer-in-pygame
            seconds=time1-(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
            if seconds<=0: # if time<=0, lose #30 seconds given
                mode="lose"
            draw_HUD(int(seconds//1))
            #drawOthers(surface,camera,otherStrangers)
            pygame.display.flip()

            score=int(blob.mass*2)
            if score>=500  :
                mode='win'

            if pygame.mouse.get_focused():
                #rohan's socket code slightly modified
                msg = "%d %d %d\n" % (blob.vx, blob.vy, blob.mass)
                print("sending: ", msg)
                server.send(msg.encode())
                if (serverMsg.qsize() > 0):#rohan v's
                    msg = serverMsg.get(False)
                try:
                    print("recieved: ", msg)
                    if msg.startswith("newPlayer"):
                        msg = msg.split()
                        newPID = int(msg[1])
                        x = int(msg[2])
                        y = int(msg[3])
                        mass=int(msg[4])
                        otherStrangers.append([x, y, mass,newPID])
                    elif msg.startswith("playerMoved"):
                        msg = msg.split()
                        PID = int(msg[1])
                        dx = int(msg[2])
                        dy = int(msg[3])
                        mass=int(msg[4])
                        for creeper in otherStrangers:
                            if creeper[3] == PID:
                                creeper[0] += dx
                                creeper[1] += dy
                                creeper[2] = mass
                                break
                except:
                    print("failed")
                    serverMsg.task_done()

            for creeper in otherStrangers:
                pass

                #if me is eaten by a stranger then isGameOver=True


        elif mode=="win":
            for event in pygame.event.get():
                if(event.type == pygame.KEYDOWN):
                    if(event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        quit()
                if(event.type == pygame.QUIT):
                    pygame.quit()
                    quit()
            drawWinScreen()
            (x,y)=pygame.mouse.get_pos()
            if (x>=screen_width//2-60 and y>=screen_height//2+100 and x<=screen_width//2+80 and y<=screen_height//2+120):
                if pygame.mouse.get_pressed()==(1,0,0):
                    mode="startingScreen"
                    blob.mass=20
                    ai=list()
                    run(surface,playing,mode,ai, serverMsg, server)
            pygame.display.flip()
            continue
        elif mode=="lose":
            for event in pygame.event.get():
                if(event.type == pygame.KEYDOWN):
                    if(event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        quit()
                if(event.type == pygame.QUIT):
                    pygame.quit()
                    quit()
            drawEndingScreen()
            (x,y)=pygame.mouse.get_pos()
            if (x>=screen_width//2-60 and y>=screen_height//2+100 and x<=screen_width//2+80 and y<=screen_height//2+120):
                if pygame.mouse.get_pressed()==(1,0,0):
                    mode="startingScreen"
                    blob.mass=20
                    ai=list()
                    run(surface,playing,mode,ai, serverMsg, server)
            pygame.display.flip()
            pass
        pass


serverMsg = Queue(100)
start_new_thread(handleServerMsg, (server, serverMsg))


mode="startingScreen"
camera = Camera()

start_ticks=pygame.time.get_ticks()
blob = Ship(surface,cells,portals,times,start_ticks,ais,font,"John Kim")
ai= AI(surface,cells,portals)
numOfCells=2000
numOfPortals=30
numOfTimes=20
#numOfAI=5
spawn_cells(numOfCells)
spawn_portals(numOfPortals)
spawn_time(numOfTimes)
#spawn_AIs(numOfAI)
playing = True
ais=list()


#run(surface,playing,mode)
run(surface,playing,mode,ais, serverMsg, server)


pygame.quit()

