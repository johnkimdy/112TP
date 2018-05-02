from tkinter import *
import random

####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.me = [data.width/2, data.height/2]
    data.otherStrangers = []
    data.balls=[]
    makeBalls(data.balls)
    data.colors=['pink','blue','green']
    data.offx,data.offy=0,0
    data.rows=50
    data.cols=50
    
    
def makeBalls(lst):
    for i in range(50):
        lst.append((random.randint(-1000,1000),random.randint(-1000,1000)))
        
        
        
def mousePressed(event, data):
    # use event.x and event.y
    pass

def moveBoard(x,y,data): #move only the board coordinates
    data.offx+=x
    data.offy+=y

def keyPressed(event, data):
    # use event.char and event.keysym
    dx,dy=0,0
    if (event.keysym == "Left"):
      dx=5
      moveBoard(dx, 0, data)
    elif (event.keysym == "Right"):
      dx=-5
      moveBoard(dx, 0, data)
    elif (event.keysym == "Up"):
      dy=5
      moveBoard(0, dy, data)
    elif (event.keysym == "Down"):
      dy=-5
      moveBoard(0, dy, data)
    '''
    if (dx != 0 or dy != 0):
      data.me[0] +=  dx
      data.me[1] +=  dy
      msg = "%d %d\n" % (dx, dy)
      print("sending: ", msg)
      data.server.send(msg.encode())
    '''
    
def timerFired(data):
    '''
    if (serverMsg.qsize() > 0):
      msg = serverMsg.get(False)
      try:
        print("recieved: ", msg)
        if msg.startswith("newPlayer"):
          msg = msg.split()
          newPID = int(msg[1])
          x = int(msg[2])
          y = int(msg[3])
          data.otherStrangers.append([x, y, newPID])
        elif msg.startswith("playerMoved"):
          msg = msg.split()
          PID = int(msg[1])
          dx = int(msg[2])
          dy = int(msg[3])
          for creeper in data.otherStrangers:
            if creeper[2] == PID:
              creeper[0] += dx * 5
              creeper[1] += dy * 5
              break
      except:
        print("failed")
      serverMsg.task_done()
    '''
    pass

def drawLines(canvas,data,size=5):
    wid=8*size #fix this later according to the size of me
    for i in range(data.rows):
        for j in range(data.cols):
            canvas.create_rectangle(i*wid+data.offx-1000,j*wid+data.offy-1000,i*wid+wid+data.offx-1000,j*wid+wid+data.offy-1000)

def drawBalls(canvas,data):
  #for balls # change sizes of the balls according to the size of me
  for ball in data.balls:
    x,y=ball
    canvas.create_oval(x+data.offx-10,y+data.offy-10,x+data.offx+10, y+data.offy+10, fill=random.choice(data.colors))
  

def drawMe(canvas,data):
  canvas.create_oval(data.width/2-20,
    data.height/2-20, data.width/2 + 20,
    data.height/2 + 20, fill = "red")
'''
def drawOthers(canvas,other):
  for creeper in other:
    canvas.create_oval(creeper[0] - 20,
      creeper[1] - 20, creeper[0] + 20,
      creeper[1] + 20, fill = "blue")
'''
def redrawAll(canvas, data):
  # draw in canvas
    drawLines(canvas,data)
    drawBalls(canvas,data)
    drawMe(canvas,data)
    #drawOthers(canvas,data.otherStrangers)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(500, 500)