'''
Ship.py

'''
import pygame
import math
import random
from Ball import Piece
from Ball import Cell
from Ball import Portal
from Ball import Time
from GameObject import GameObject


#This whole thing is my code
#ONLY THE AESTHETIC COLORS
colors_players = [(236,232,254),(254,236,232),(131,146,159),(252,233,241),(163,145,147),(170,111,115),(246,224,181)]
screen_width, screen_height = (800,500)
start_ticks=pygame.time.get_ticks()

def getDistance(pos1,pos2):
    x1,y1 = pos1
    x2,y2 = pos2
    diffX = x1-x2
    diffY = y1-y2

    return ((diffX**2)+(diffY**2))**(0.5)

def drawText(surface,message,font,pos,color=(255,255,255)):
        surface.blit(font.render(message,1,color),pos)


class Ship:
    def __init__(self,surface,cell_list,portal_list,time_list,ticks,aIs,font,name = ""):
        self.seconds=30-(pygame.time.get_ticks()-ticks)/1000 #calculate how many seconds
        self.startX = self.x = random.randint(100,400)
        self.startY = self.y = random.randint(100,400)
        self.mass = 20
        self.surface = surface
        self.color = colors_players[random.randint(0,len(colors_players)-1)]
        self.name = name
        self.pieces = list()
        self.cell_list=cell_list
        self.time_list=time_list
        self.portal_list=portal_list
        self.aI=aIs
        self.font=font

        self.power = 1
        self.drag = 0.9
        self.angleSpeed = 5
        self.angle = 0  # starts pointing straight up
        self.maxSpeed = 5
        self.width,self.height=screen_width,screen_height
        self.vx,self.vy=0,0

        piece = Piece(self.surface,(self.x,self.y),self.color,self.mass,self.name)




    def collisionDetection(self):
        for cell in self.cell_list:
            if(getDistance((cell.x,cell.y),(self.x,self.y)) <= self.mass/2):
                self.mass+=0.5
                self.cell_list.remove(cell)
                self.cell_list.append(Cell(self.surface))


        for portal in self.portal_list:
                if(getDistance((portal.x,portal.y),(self.x,self.y)) <= self.mass/2):
                    self.x,self.y=(random.randint(20,1980), random.randint(20,1980))
                    self.portal_list.remove(portal)
                    self.portal_list.append(Portal(self.surface))



        for ai in self.aI:
            if(getDistance((ai.x,ai.y),(self.x,self.y)) <= self.mass/2):
                if ai.mass>=1.15*self.mass:
                    return False
                elif self.mass>=1.15*ai.mass:
                    self.mass+= ai.mass
                    self.aI.remove(ai)

        for time in self.time_list:
            if(getDistance((time.x,time.y),(self.x,self.y)) <= self.mass/2):
                self.seconds+=5
                self.time_list.remove(time)
                self.time_list.append(Time(self.surface))
                return True


    def draw(self,cam):
        col = self.color
        zoom = cam.zoom
        x = cam.x
        y = cam.y
        pygame.draw.circle(self.surface,(col[0]-int(col[0]/3),int(col[1]-col[1]/3),int(col[2]-col[2]/3)),(int(self.x*zoom+x),int(self.y*zoom+y)),int((self.mass/2+3)*zoom))
        pygame.draw.circle(self.surface,col,(int(self.x*cam.zoom+cam.x),int(self.y*cam.zoom+cam.y)),int(self.mass/2*zoom))
        if(len(self.name) > 0):
            fw, fh = self.font.size(self.name)
            drawText(self.surface,self.name,self.font, (self.x*cam.zoom+cam.x-int(fw/2),self.y*cam.zoom+cam.y-int(fh/2)),(50,50,50))

    def move(self): #mine
        x,y=pygame.mouse.get_pos()
        dx,dy=x-self.width/2,y-self.height/2

        #print(dx,dy)
        pi=math.pi
        if pygame.mouse.get_focused():
            if dx>0 and dy<0: # quad 4
                self.angle=math.degrees(pi/2-math.atan(dx/-dy))
                self.thrust(self.power)
            elif dx<0 and dy<0: #quad 3
                self.angle=math.degrees(pi/2+math.atan(dx/dy))
                self.thrust(self.power)
            elif dx>0 and dy>0: #quad 1
                self.angle=math.degrees(2*pi-math.atan(dy/dx))
                self.thrust(self.power)
            elif dx<0 and dy>0: #quad 2
                self.angle=math.degrees((3/2)*pi+math.atan(dx/dy))
                self.thrust(self.power)

            elif dx==0 and dy<0:
                self.angle=math.degrees(pi/2)
                self.thrust(self.power)
            elif dx==0 and dy>0:
                self.angle=math.degrees((3/2)*pi)
                self.thrust(self.power)
            elif dx >0 and dy==0:
                self.angle=0
                self.thrust(self.power)
            elif dx<0 and dy==0:
                self.angle=math.degrees(pi)
                self.thrust(self.power)



    def thrust(self, power): #format by Lukas Pereza but physics modified by me
        angle = math.radians(self.angle)
        vx, vy = self.vx,self.vy
        # distribute the thrust in x and y directions based on angle
        vx += power * math.cos(angle)
        vy -= power * math.sin(angle)
        speed = math.sqrt(vx ** 2 + vy ** 2)
        if speed > self.maxSpeed:
            factor = self.maxSpeed / speed
            vx *= factor
            vy *= factor
        self.vx=vx
        self.vy=vy
        self.x+=self.vx
        self.y+=self.vy
