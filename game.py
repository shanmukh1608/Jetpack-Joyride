import signal
import shutil
import os
import subprocess
import time
import readInput as hack
import random   
import cursor
import colorama
from colorama import Fore, Back, Style 

from characters import mando, dragon, babyyoda
from entity import point
from objects import coins, lasers, bullets, speedup, magnets, snowballs
import globalobjects
from globalobjects import obj_Board as board

def pos(x, y):
	return '\x1b[%d;%dH' % (y, x)

os.system('clear')
cursor.hide()

def checkCollision(obj1, obj2):
	l1 = point(obj1.retPos()[1], obj1.retPos()[0])
	r1 = point(obj1.retPos()[1] + obj1.retDim()[1], obj1.retPos()[0] + obj1.retDim()[0])

	l2 = point(obj2.retPos()[1], obj2.retPos()[0])
	r2 = point(obj2.retPos()[1] + obj2.retDim()[1], obj2.retPos()[0] + obj2.retDim()[0])

	if(l1._x > r2._x or l2._x > r1._x): 
		return 0

	if(l1._y > r2._y or l2._y > r1._y): 
		return 0
	
	return 1

startTime = time.time()
lastCoinTime = time.time()
lastLaserTime = time.time()
lastPowerUpTime = time.time() #last time of collection
lastSpeedUpTime = time.time() #last time of activation
lastSnowballTime = time.time()

lastShieldTime = time.time()

g_timer = 0
tick = 0

coinsList = []
coinCount = 0

laserList = []
laserCount = 0

powerUpList = []
powerUpCount = 0

bulletList = []
bulletCount = 0

snowballList = []
snowballCount = 0

magnetCreated = False

mando = mando(board._rows-7, 1)
kb = hack.KBHit()
columns = shutil.get_terminal_size().columns

print("\n"*23)
yoda = babyyoda(0, 0)

print("WELCOME TO JETPACK JOYRIDE!".center(columns))
print("Use WASD to move".center(columns))
print("Press F to shoot bullets".center(columns))
print("Press spacebar to activate shield".center(columns))
print("Your character has 3 lives".center(columns))
print("Beat the boss to win and rescue Baby Yoda!".center(columns))
print()
print("PRESS e TO START GAME".center(columns))
for i in yoda.retInitialMat():
	print(i)
text = "a"
while text != "e":
	if kb.kbhit():
		text = kb.getch()


while (globalobjects.lives > 0 and globalobjects.gameOver == False):
	globalobjects.timeleft = int(90 - time.time() + startTime)
	
	if (mando.retPos()[0] == board._rows - 7): # if touches ground
		globalobjects.g_timer = time.time()

	mando.gravity()

	if (globalobjects.shieldActive == True):
		mando.updateBoard(mando._shieldMat, flag="put")
	else:
		mando.updateBoard(mando._mat, flag="put")

	if (time.time() - startTime >= random.randint(30, 60)):
		if (magnetCreated is False):
			magnet = magnets(25, board._columns - 10)
			magnet.updateBoard(magnet.retMat(), flag="put")
			magnetCreated = True

	if (time.time() - lastShieldTime >= 10):
		globalobjects.shieldActive = False

	if (time.time() - lastShieldTime >= 70):
		globalobjects.shieldAvailable = True
	
	if (time.time() - lastSpeedUpTime >= 10):
		globalobjects.speedup = False

	if (mando.retPos()[0] == board._rows - 7): # if touches ground
		globalobjects.g_timer = time.time()

	if globalobjects.timeleft > 0:	
		if (time.time() - lastCoinTime > 1):
			coinsList.append(coins(random.randint(3, board._rows - 4), board._columns - 3))
			coinsList[coinCount].updateBoard(coinsList[coinCount].retMat(), flag="put")
			coinCount = coinCount + 1
			lastCoinTime = time.time()
	
		if (time.time() - lastLaserTime > 2):
			laserList.append(lasers(random.randint(3, board._rows - 8), board._columns - 7))
			laserList[laserCount].updateBoard(laserList[laserCount].retMat(), flag="put")
			laserCount = laserCount + 1
			lastLaserTime = time.time()
	
		if (time.time() - lastPowerUpTime > 10):
			powerUpList.append(speedup(random.randint(3, board._rows - 7), board._columns - 6))
			powerUpList[powerUpCount].updateBoard(powerUpList[powerUpCount].retMat(), flag="put")
			powerUpCount = powerUpCount + 1
			lastPowerUpTime = time.time()

	try:
		if (tick % 5 == 0):
			magnet.moveLeft(1)
			if (magnet.retPos()[1] < 4):
				magnet.updateBoard(magnet.retMat(), )
				del(magnet)
	except:
		pass

	for i in range(len(bulletList)):
		try:
			if (tick % 2 == 0):
				bulletList[i].moveRight(1 if globalobjects.speedup == False else 2)
		except:
			pass

		try:
			for j in range(len(laserList)):
				if (checkCollision(laserList[j], bulletList[i]) == 1):
					laserList[j].updateBoard(laserList[j].retMat(), )
					del(laserList[j])
					bulletList[i].updateBoard(bulletList[i].retMat(), )
					del(bulletList[i])
					bulletCount -= 1
					laserCount = laserCount - 1
					globalobjects.score += 1
		except:
			pass

		try:
			if (bulletList[i].retPos()[1] > board._columns - 7):
				bulletList[i].updateBoard(bulletList[i].retMat(), )
				del(bulletList[i])
				bulletCount = bulletCount - 1
		except:
			pass

		try:
			if (checkCollision(bulletList[i], enemy) == 1):
				bulletList[i].updateBoard(bulletList[i].retMat(), )
				globalobjects.enemylives -= 1
				if (globalobjects.enemylives <= 0):
					globalobjects.gameOver = True
				del(bulletList[i])
				bulletCount -= 1
		except:
			pass

		

	for i in range(len(coinsList)):

		try:
			if (tick % 3 == 0):
				coinsList[i].moveLeft(1 if globalobjects.speedup == False else 2)
		except:
			pass

		try:
			if (checkCollision(coinsList[i], mando) == 1):
				globalobjects.score = globalobjects.score + 1
				coinsList[i].updateBoard(coinsList[i].retMat(), )
				del(coinsList[i])
				coinCount = coinCount - 1
		except:
			pass
			
		try:
			if (coinsList[i].retPos()[1] < 4):
				coinsList[i].updateBoard(coinsList[i].retMat(), )
				del(coinsList[i])
				coinCount = coinCount - 1
		except:
			pass

	for i in range(len(laserList)):
		
		try:
			if (tick % 3 == 0):
				laserList[i].moveLeft(1 if globalobjects.speedup == False else 2)
		except:
			pass

		try:
			if (checkCollision(laserList[i], mando) == 1):
				if (globalobjects.shieldActive == False):
					globalobjects.lives = globalobjects.lives - 1
				laserList[i].updateBoard(laserList[i].retMat(), )
				del(laserList[i])
				laserCount = laserCount - 1
		except:
			pass

		try:
			if (laserList[i].retPos()[1] < 4):
				laserList[i].updateBoard(laserList[i].retMat(), )
				del(laserList[i])
				laserCount = laserCount - 1
		except:
			pass

	for i in range(len(powerUpList)):
		try:
			if (tick % 3 == 0):
				powerUpList[i].moveLeft(1 if globalobjects.speedup == False else 2)
		except:
			pass
			
		try:
			if (checkCollision(powerUpList[i], mando) == 1):
				globalobjects.speedup = True
				lastSpeedUpTime = time.time()
				powerUpList[i].updateBoard(powerUpList[i].retMat(), )
				del(powerUpList[i])
				powerUpCount = powerUpCount - 1
		except:
			pass

		try:
			if (powerUpList[i].retPos()[1] < 4):
				powerUpList[i].updateBoard(powerUpList[i].retMat(), )
				del(powerUpList[i])
				powerUpCount = powerUpCount - 1
		except:
			pass
		
	if 'magnet' in locals():
		if tick % 2 == 0:
			if magnet.retPos()[1] < mando.retPos()[1]:
				mando.moveLeft(1)
			elif magnet.retPos()[1] > mando.retPos()[1]:
				mando.moveRight(1)

	if globalobjects.timeleft <= 0:
		if 'enemy' not in locals():
			enemy = dragon(10, board._columns - 25)
		
		enemy.updateBoard(enemy.retMat(), )
		enemy.setX(max(8, mando.retPos()[0]) - 8)
		enemy.updateBoard(enemy.retMat(), flag="put")

		if (time.time() - lastSnowballTime >= 0.5):
			snowballList.append(snowballs(enemy.retPos()[0]+10, enemy.retPos()[1]))
			snowballList[snowballCount].updateBoard(snowballList[snowballCount].retMat(), flag = "put")
			snowballCount = snowballCount + 1
			lastSnowballTime = time.time()

		for i in range(len(snowballList)):
			try:
				snowballList[i].moveLeft(1)
			except:
				pass

			try:
				if (checkCollision(snowballList[i], mando) == 1):
					if (globalobjects.shieldActive == False):
						globalobjects.lives -= 1
					snowballList[i].updateBoard(snowballList[i].retMat(), )
					del(snowballList[i])
					snowballCount = snowballCount - 1
			except:
				pass

			try:
				if (snowballList[i].retPos()[1] < 4):
					snowballList[i].updateBoard(snowballList[i].retMat(), )
					del(snowballList[i])
					snowballCount = snowballCount - 1
			except:
				pass

	text="x"
	if kb.kbhit():
		text = kb.getch()
	
	if text == "w":
		mando.moveUp(5)
		globalobjects.g_timer = time.time()

	if text == "d":
		mando.moveRight(2 if globalobjects.speedup == False else 2*2)
	if text == "a":
		mando.moveLeft(2 if globalobjects.speedup == False else 2*2)

	if text == " ":
		if globalobjects.shieldAvailable is True:
			globalobjects.shieldActive = True
			globalobjects.shieldAvailable = False
			lastShieldTime = time.time()

	if text == "f":
		bulletList.append(bullets(mando.retPos()[0]+2, mando.retPos()[1]+7))
		bulletList[bulletCount].updateBoard(bulletList[bulletCount].retMat(), flag="put")
		bulletCount = bulletCount + 1

	if text == "q":
		globalobjects.gameOver = True

	board.printboard()

	tick = tick + 1


for i in range(board._rows):
	for j in range(board._columns):
			print('%s%s%s%s' % (pos(j, i), Back.RESET,Fore.RESET, " "), end='')
os.system('clear')

if globalobjects.lives > 0:
	for i in yoda.retMat():
		print(i)
else:
	for i in yoda.retLosingMat():
		print(i)