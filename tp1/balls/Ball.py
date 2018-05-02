'''
Ball.py

implements the Ball class
Lukas Peraza, 2015 for 15-112 Pygame Lecture
'''
import pygame
import random
import math
from GameObject import GameObject


class Ball(GameObject):
    @staticmethod
    def init():
        image = pygame.transform.scale(pygame.image.load('images/kosbie.gif').convert_alpha(),(240,300))
        rows, cols = 4, 4
        width, height = image.get_size()
        cellWidth, cellHeight = width / cols, height / rows
        Ball.images = []
        Ball.images.append(image)
        '''
        for i in range(rows):
            for j in range(cols):
                subImage = image.subsurface(
                    (i * cellWidth, j * cellHeight, cellWidth, cellHeight))
                Ball.images.append(subImage)
        '''
    minSize = 1
    maxSize = 1

    def __init__(self, x, y, level=None):
        if level is None:
            level = random.randint(Ball.minSize, Ball.maxSize)
        self.level = level
        factor = self.level / 6
        image = random.choice(Ball.images)
        w, h = image.get_size()
        image = pygame.transform.scale(image, (int(w * factor), int(h * factor)))
        super(Ball, self).__init__(x, y, image, w / 7 * factor)
        self.angleSpeed = 0 #random.randint(-10, 10)
        self.power = 1
        self.drag = 0.9
        self.angleSpeed = 5
        self.angle = 0  # starts pointing straight up
        self.maxSpeed = 10
        
        

    def update(self, screenWidth, screenHeight):
        self.angle += self.angleSpeed
        
        x,y=pygame.mouse.get_pos()
        dx,dy=x-screenWidth/2,y-screenHeight/2
       # print(dx,dy)
        pi=math.pi
        if pygame.mouse.get_focused():
            if dx>0 and dy<0:# I quad
                #print('0')
                self.angle=math.degrees((3/2)*pi+math.atan(dx/dy))
                self.thrust(self.power)
                #print(self.angle)
            elif dx<0 and dy<0:# II quad
                #print('1')
                self.angle=math.degrees(2*pi-math.atan(dy/dx))
                self.thrust(self.power)
                #print(self.angle)
            elif dx>0 and dy>0: # IV quad
                #print('2')
                self.angle=math.degrees(pi/2+math.atan(dx/dy))
            
                self.thrust(self.power)
                #print(self.angle)
            elif dx<0 and dy>0:# III quad
                #print('3')
                self.angle=math.degrees(pi/2-math.atan(dx/-dy))
                #print(self.angle)
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
    
    
            super(Ball, self).update(screenWidth, screenHeight)
        '''
        def update2(self, d):
            image = pygame.transform.scale(pygame.image.load('images/kosbie.gif').convert_alpha(),(240-d,300-d))
            Ball.images=[image]
        
        #super(Ball, self).update2(x)
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



####
    def breakApart(self):
        if self.level == Ball.minSize:
            return []
        else:
            return [Ball(self.x, self.y, self.level - 1),
                    Ball(self.x, self.y, self.level - 1)]
