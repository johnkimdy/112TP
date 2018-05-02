'''
GameObject.py

implements the base GameObject class, which defines the wraparound motion
Lukas Peraza, 2015 for 15-112 Pygame Lecture
'''
import pygame

colors_players = [(37,7,255),(35,183,253),(48,254,241),(19,79,251),(255,7,230),(255,7,23),(6,254,13)]
colors_cells = [(80,252,54),(36,244,255),(243,31,46),(4,39,243),(254,6,178),(255,211,7),(216,6,254),(145,255,7),(7,255,182),(255,6,86),(147,7,255)]
colors_viruses = [(66,254,71)]
screen_width, screen_height = (800,500)
class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image, radius):
        super(GameObject, self).__init__()
        # x, y define the center of the object
        self.x, self.y, self.image, self.radius = x, y, image, radius
        self.baseImage = image.copy()  # non-rotated version of image
        w, h = image.get_size()
        self.updateRect()
        self.velocity = (0, 0)
        self.angle = 0

    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)

    def update(self, screenWidth, screenHeight):
        self.image = pygame.transform.rotate(self.baseImage, self.angle)
        vx, vy = self.velocity
        self.x += vx
        self.y += vy
        self.updateRect()
        '''
        # wrap around, and update the rectangle again
        if self.rect.left > screenWidth:
            self.x -= screenWidth + self.width
        elif self.rect.right < 0:
            self.x += screenWidth + self.width
        if self.rect.top > screenHeight:
            self.y -= screenHeight + self.height
        elif self.rect.bottom < 0:
            self.y += screenHeight + self.height
        '''
        
        #self.updateRect()