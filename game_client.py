#this whole thing is rohan's

import socket
import random
from _thread import *
from queue import Queue


HOST = ''
PORT = 50013

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect((HOST,PORT))
print("connected to server")

def handleServerMsg(server, serverMsg): #rohan v's code
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

# events-example0.py
# Barebones timer, mouse, and keyboard events

from tkinter import *

####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.me = [data.width/2, data.height/2]
    data.otherStrangers = []
    data.balls=[]
    data.colors=['red','blue','green']
    data.offx,data.offy=0,0

def mousePressed(event, data):
    # use event.x and event.y
    pass

def moveBoard(x,y,data): #move only the board coordinates
    data.offx+=x
    data.offy+=y

def keyPressed(event, data):
    # use event.char and event.keysym
    dx,dy=0
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
    if (dx != 0 or dy != 0):
      data.me[0] +=  dx
      data.me[1] +=  dy
      msg = "%d %d\n" % (dx, dy)
      print("sending: ", msg)
      data.server.send(msg.encode())

def timerFired(data):
    if (serverMsg.qsize() > 0): #rohan v's
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


def drawBoard(canvas,balls,colors,size,data):
  #for balls
  for ball in balls:
    x,y=ball
    canvas.create_oval(x+data.offx-10,y+data.offy-10,x+data.offx+10, y+data.offy-10, fill=random.choice(colors))


def drawMe(canvas,me):
  canvas.create_oval(data.width/2,
    me[1] - 20, me[0] + 20,
    me[1] + 20, fill = "red")

def drawOthers(canvas,other):
  for creeper in other:
    canvas.create_oval(creeper[0] - 20,
      creeper[1] - 20, creeper[0] + 20,
      creeper[1] + 20, fill = "blue")

def redrawAll(canvas, data):
  # draw in canvas
    drawMe(canvas,data.me)
    drawOthers(canvas,data.otherStrangers)

####################################
# use the run function as-is
####################################

def run(width, height, serverMsg=None, server=None):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
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
    data.server = server
    data.serverMsg = serverMsg
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

serverMsg = Queue(100)
start_new_thread(handleServerMsg, (server, serverMsg))

run(500, 500, serverMsg, server)