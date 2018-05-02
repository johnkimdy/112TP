'''
pygamegame.py
created by Lukas Peraza
 for 15-112 F15 Pygame Optional Lecture, 11/11/15

use this code in your term project if you want
- CITE IT
- you can modify it to your liking
  - BUT STILL CITE IT

- you should remove the print calls from any function you aren't using
- you might want to move the pygame.display.flip() to your redrawAll function,
    in case you don't need to update the entire display every frame (then you
    should use pygame.display.update(Rect) instead)
'''
import pygame
from Camera import Camera
from Ship import Ship
from Ball import Cell
from Ball import Piece
x = 0
y = 0
pygame.init()
screen_width, screen_height = (800,500)
surface = pygame.display.set_mode((screen_width,screen_height))
t_surface = pygame.Surface((95,25),pygame.SRCALPHA) #transparent rect for score
t_lb_surface = pygame.Surface((155,278),pygame.SRCALPHA) #transparent rect for leaderboard
t_surface.fill((50,50,50,80))
t_lb_surface.fill((50,50,50,80))
pygame.display.set_caption("Agar.io")
cells = list()
clock = pygame.time.Clock()

try:
    font = pygame.font.Font("Ubuntu-B.ttf",20)
    big_font = pygame.font.Font("Ubuntu-B.ttf",24)
except:
    print("Font file not found: Ubuntu-B.ttf")
    font = pygame.font.SysFont('Ubuntu',20,True)
    big_font = pygame.font.SysFont('Ubuntu',24,True)
#http://stackoverflow.com/questions/4135928/pygame-display-position
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y) 


class PygameGame(object):

    def init(self):
        pass
        
    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        pass

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)
    
    def spawn_cells(self,numOfCells):
        for i in range(numOfCells):
            cell = Cell(surface)
            cell_list.append(cell)
    
    
    def draw_grid(self):
        for i in range(0,2001,25):
            pygame.draw.line(surface,(230,240,240),(0+camera.x,i*camera.zoom+camera.y),(2001*camera.zoom+camera.x,i*camera.zoom+camera.y),3)
            pygame.draw.line(surface,(230,240,240),(i*camera.zoom+camera.x,0+camera.y),(i*camera.zoom+camera.x,2001*camera.zoom+camera.y),3)
            
    def __init__(self, width=600, height=400, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()
    
    def run(self,playing,serverMsg=None, server=None):
        cell_list=list()
        camera = Camera()
        blob = Ship(surface,cell_list,font,"Player1")
        numOfCells=2000
        self.spawn_cells(numOfCells)
        while playing:
            if not isGameOver:
                clock.tick(70)
                for e in pygame.event.get():
                    if(e.type == pygame.KEYDOWN):
                        if(e.key == pygame.K_ESCAPE):
                            pygame.quit()
                            quit()
                        if(e.key == pygame.K_SPACE):
                            blob.split()
                        if(e.key == pygame.K_w):
                            blob.feed()
                    if(e.type == pygame.QUIT):
                        pygame.quit()
                        quit()
                blob.update()
                camera.zoom = 100/(blob.mass)+0.3
                camera.center(blob)
                surface.fill((242,251,255))
                #surface.fill((0,0,0))
                self.draw_grid()
                for c in cell_list:
                    c.draw(camera)
                blob.draw(camera)
                #draw_HUD()
                pygame.display.flip()
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
                '''
            else:
                pass
                #drawEndingScreen
            # stores all the keys currently being held down
            self._keys = dict()
    
            # call game-specific initialization
            self.init()
        pygame.quit()
        
    

def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()
