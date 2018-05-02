'''
Ball.py

implements the Ball class
Lukas Peraza, 2015 for 15-112 Pygame Lecture
'''
import pygame
import random
import math
from GameObject import GameObject


colors_cells = [(236,232,254),(254,236,232),(131,146,159),(252,233,241),(163,145,147),(170,111,115),(246,224,181)]


def getDistance(pos1,pos2):
    x1,y1 = pos1
    x2,y2 = pos2
    diffX = x1-x2
    diffY = y1-y2

    return ((diffX**2)+(diffY**2))**(0.5)

class Piece: #https://github.com/Viliami/agario/blob/master/agar.py
    def __init__(self,surface,pos,color,mass,name,transition=False):
        self.x,self.y = pos
        self.mass = mass
        self.splitting = transition
        self.surface = surface
        self.name = name

    def draw(self):
        pass

    def update(self):
        if(self.splitting):
            pass

class Cell: #https://github.com/Viliami/agario/blob/master/agar.py
    def __init__(self,surface):
        self.x = random.randint(20,1980)
        self.y = random.randint(20,1980)
        self.mass = 7
        self.surface = surface
        self.color = colors_cells[random.randint(0,len(colors_cells)-1)]

    def draw(self,cam):
        pygame.draw.circle(self.surface,self.color,(int((self.x*cam.zoom+cam.x)),int(self.y*cam.zoom+cam.y)),int(self.mass*cam.zoom))
        
        
class Portal:#mine
    def __init__(self,surface):
        self.x = random.randint(20,1980)
        self.y = random.randint(20,1980)
        self.mass = 15
        self.surface = surface
        self.color = (0,191,255)

    def draw(self,cam):#mine
        pygame.draw.circle(self.surface,self.color,(int((self.x*cam.zoom+cam.x)),int(self.y*cam.zoom+cam.y)),int(self.mass*cam.zoom))
        pygame.draw.circle(self.surface,(255,255,255),(int((self.x*cam.zoom+cam.x)),int(self.y*cam.zoom+cam.y)),int(self.mass*0.75*cam.zoom))
        
class Time:#mine
    def __init__(self,surface):
        self.x = random.randint(20,1980)
        self.y = random.randint(20,1980)
        self.mass = 15
        self.surface = surface
        self.color = (255,0,0)

    def draw(self,cam):
        pygame.draw.circle(self.surface,self.color,(int((self.x*cam.zoom+cam.x)),int(self.y*cam.zoom+cam.y)),int(self.mass*cam.zoom))
        pygame.draw.circle(self.surface,(0,0,0),(int((self.x*cam.zoom+cam.x)),int(self.y*cam.zoom+cam.y)),int(self.mass*0.75*cam.zoom))
        
class AI:#mine
    def __init__(self,surface, cell_list,portal_list):
        self.x = random.randint(20,1980)
        self.y = random.randint(20,1980)
        self.mass = 15
        self.surface = surface
        self.color = (0,0,255)
        self.name="AI"
        self.cell_list=cell_list
        self.portal_list=portal_list
        
        self.power = 0.1
        self.drag = 0.9
        self.angleSpeed = 5
        self.angle = 0  # starts pointing straight up
        self.maxSpeed = 5
       
        self.vx,self.vy=0,0
        piece = Piece(self.surface,(self.x,self.y),self.color,self.mass,self.name)
        
        

    def collisionDetection(self):#mine
        for cell in self.cell_list:
            if(getDistance((cell.x,cell.y),(self.x,self.y)) <= self.mass/2):
                self.mass+=0.5
                self.cell_list.remove(cell)
                self.cell_list.append(Cell(self.surface))
        
        for portal in self.portal_list:#mine
            if(getDistance((portal.x,portal.y),(self.x,self.y)) <= self.mass/2):
                self.x,self.y=(random.randint(20,1980), random.randint(20,1980))
                self.portal_list.remove(portal)
                self.portal_list.append(Portal(self.surface))    
        
    def moveAI(self,other): #mine
        x,y=other.x,other.y
        dx,dy=x-self.x,y-self.y
        
        #print(dx,dy)
        pi=math.pi
        if pygame.mouse.get_focused():
            if dx>0 and dy<0:
                self.angle=math.degrees(pi/2-math.atan(dx/-dy))
                self.thrust(self.power)
            elif dx<0 and dy<0:
                self.angle=math.degrees(pi/2+math.atan(dx/dy))
                self.thrust(self.power)
            elif dx>0 and dy>0:
                self.angle=math.degrees(2*pi-math.atan(dy/dx))
                self.thrust(self.power)
            elif dx<0 and dy>0:
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


    def draw(self,cam):#mine
        pygame.draw.circle(self.surface,self.color,(int((self.x*cam.zoom+cam.x)),int(self.y*cam.zoom+cam.y)),int((self.mass/2+3)*cam.zoom))
    