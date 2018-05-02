#https://github.com/Viliami/agario/blob/master/agar.py
import pygame
from GameObject import GameObject
from Ship import Ship

screen_width, screen_height = (800,500)
class Camera(Ship):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = screen_width
        self.height = screen_height
        self.zoom = 0.5

    def center(self,blobOrPos):
        if(isinstance(blobOrPos,Ship)):
            p = blobOrPos
            self.x = (p.startX-(p.x*self.zoom))-p.startX+((screen_width/2))
            self.y = (p.startY-(p.y*self.zoom))-p.startY+((screen_height/2))
        elif(type(blobOrPos) == tuple):
            self.x,self.y = blobOrPos