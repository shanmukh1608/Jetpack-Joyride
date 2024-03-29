from board import board
from scenery import Scenery
import subprocess
import time

rows = int(subprocess.check_output('stty size | cut -d\  -f1', shell=True))
columns = int(subprocess.check_output('stty size | cut -d\  -f2', shell=True))

obj_Board = board(rows, columns)
obj_Board.create_board()
     
obj_scenery = Scenery()
obj_scenery.create_ground(obj_Board)
obj_scenery.create_sky(obj_Board)

lives = 3
enemylives = 10
score = 0
timeleft = 15
shieldAvailable = True
shieldActive = False
speedup = False
gameOver = False
magnetActive = False
g_timer = time.time()
