'''
Ship.py

implements the Ship class, which defines the player controllable ship
Lukas Peraza, 2015 for 15-112 Pygame Lecture
'''
import pygame
import math
from GameObject import GameObject


class Ship(GameObject):
    # we only need to load the image once, not for every ship we make!
    #   granted, there's probably only one ship...
    @staticmethod
    def init(x=0,y=0):
        Ship.shipImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/redcircle.png').convert_alpha(),
            (90+x,90+y)), -90)

    def __init__(self, x, y):
        super(Ship, self).__init__(x, y, Ship.shipImage, 30)
        self.power = 1
        self.drag = 0.9
        self.angleSpeed = 5
        self.angle = 0  # starts pointing straight up
        self.maxSpeed = 20
        self.invincibleTime = 1500
        self.timeAlive = 0

    def update(self, dt, keysDown, screenWidth, screenHeight):
        self.timeAlive += dt
    
     
    def update2(self,x,y):
        Ship.shipImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/redcircle.png').convert_alpha(),
            (90+x,90+y)), -90)

    
    '''
    x,y=pygame.mouse.get_pos()
    dx,dy=x-self.width/2,y-self.height/2
    #print(dx,dy)
    pi=math.pi
    print(pygame.mouse.get_focused())
    if dx>0 and dy<0:
        print('0')
        self.angle=math.degrees(pi/2-math.atan(dx/-dy))
        self.thrust(self.power)
        print(self.angle)
    elif dx<0 and dy<0:
        print('1')
        self.angle=math.degrees(pi/2+math.atan(dx/dy))
        self.thrust(self.power)
        print(self.angle)
    elif dx>0 and dy>0:
        print('2')
        self.angle=math.degrees(2*pi-math.atan(dy/dx))
        self.thrust(self.power)
        print(self.angle)
    elif dx<0 and dy>0:
        print('3')
        self.angle=math.degrees((3/2)*pi+math.atan(dx/dy))
        print(self.angle)
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
    elif keysDown(pygame.K_LEFT):
        self.angle =180
        self.thrust(self.power)

    elif keysDown(pygame.K_RIGHT):
        # not elif! if we're holding left and right, don't turn
        self.angle = 0
        self.thrust(self.power)

    elif keysDown(pygame.K_UP):
        self.angle=90
        self.thrust(self.power)
    elif keysDown(pygame.K_DOWN):
        self.angle=270
        self.thrust(self.power)

    else:
        vx, vy = self.velocity
        self.velocity = self.drag * vx, self.drag * vy

    super(Ship, self).update(screenWidth, screenHeight)
    '''
    '''
    x,y=pygame.mouse.get_pos()
    print(x,y)
    dx,dy=x-self.width/2,y-self.height/2
    pi=math.pi
    if dx>0 and dy<0:
        self.angle=pi/2-math.atan(dx/dy)
        self.thrust(self.power)
    elif dx<0 and dy<0:
        self.angle=pi/2+math.atan(dx/dy)
        self.thrust(self.power)
    elif dx>0 and dy>0:
        self.angle=2*pi-math.atan(dy/dx)
        self.thrust(self.power)
    elif dx<0 and dy>0:
        self.angle=(3/2)*pi+math.atan(dx/dy)
        self.thrust(self.power)
    elif dx==0 and dy<0:
        self.angle=pi/2
        self.thrust(self.power)
    elif dx==0 and dy>0:
        self.angle=(3/2)*pi
        self.thrust(self.power)
    elif dx >0 and dy==0:
        self.angle=0
        self.thrust(self.power)
    elif dx<0 and dy==0:
        self.angle=pi
        self.thrust(self.power)
    '''
 

    def thrust(self, power):
        angle = math.radians(self.angle)
        vx, vy = self.velocity
        # distribute the thrust in x and y directions based on angle
        vx += power * math.cos(angle)
        vy -= power * math.sin(angle)
        speed = math.sqrt(vx ** 2 + vy ** 2)
        if speed > self.maxSpeed:
            factor = self.maxSpeed / speed
            vx *= factor
            vy *= factor
        self.velocity = (vx, vy)

    def isInvincible(self):
        return self.timeAlive < self.invincibleTime