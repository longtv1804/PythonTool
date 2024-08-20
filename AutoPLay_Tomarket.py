import pyautogui

import time 
import threading 
import sys
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode, Key
import random

pyautogui.PAUSE = 0.001

JUMP_PIXELS = 28
NUM_OF_THREAD = 10
GAME_PLAY_TIME = 31
START_GAME_BUTTONs = 	[[200, 340], [520, 340], [840, 340], [1160, 340], [1480, 340], [1800, 340], \
						 [200, 860], [520, 860], [840, 860], [1160, 860]]
NEXT_GAME_BUTTONs =		[[150, 480], [480, 480], [800, 480], [1120, 480], [1440, 480], [1760, 480], \
						 [150, 995], [480, 995], [800, 995], [1120, 995]]
CANCEL_SHARINGs =		[[160, 140], [475, 140], [790, 140], [1105, 140], [1420, 140], [1735, 140], \
						 [160, 655], [475, 655], [790, 655], [1105, 655]]
POINTs = 	[[25, 105, 280, 404], 	\
			[340, 105, 595, 404], 	\
			[655, 105, 910, 404], 	\
			[970, 105, 1225, 404], 	\
			[1288, 105, 1540, 404], \
			[1600, 105, 1855, 404], \
			[25, 625, 280, 920], \
			[340, 625, 595, 920], \
			[655, 625, 910, 920], \
			[970, 625, 1225, 920]]

GAME_STATE_DEFAULT = 0
GAME_STATE_PLAYING = 1
GAME_STATE_PAUSE = 2
GAME_STATE_PAUSE_IN_PLAYING = 3
GAME_STATE_WAIT_NEXT_GAME = 4
GAME_STATE_NEXTING_SCREEN = 5
GAME_STATE_PAUSE_IN_NEXTING_SCREEN = 6
GAME_STATE_PAUSE_BY_USER = 7
GAME_STATE_PAUSE_IN_WAIT_NEXT_GAMGE = 8

gLDplayerId = -1
gNumOfScreens = -1

class iPosition:
	x = 0
	y = 0
	def __init__(this):
		pass
	def toString(this):
		return "({},{})".format(this.x, this.y)

class ChildThread(threading.Thread):
	mIsRunning = True
	mIsPause = True

	p1 = None
	P2 = None

	mClickedCount = 0
	mGameController = None

	def __init__(this, gameCtr):
		super(ChildThread, this).__init__()
		this.mGameController = gameCtr
		pass
	
	def pause(this):
		this.mIsPause = True

	def resume(this):
		this.mIsPause = False
		this.mClickedCount = 0

	def exit(this):
		this.mIsPause = True
		this.mIsRunning = False
	
	def getCount(this):
		return this.mClickedCount
	
	def checkAndClick(this):
		i = this.p1.x
		j = 0
		paddingPosition = random.randint(0, 20)
		while i < this.p2.x:
			if this.mIsPause == True or this.mIsRunning == False:
				break
			j = this.p1.y + paddingPosition
			while j < this.p2.y + paddingPosition:
				if this.mIsPause == True or this.mIsRunning == False:
					break
				if pyautogui.pixelMatchesColor(i, j, (255, 60, 105), tolerance=20):
					pyautogui.click(i, j + 3)
					this.mClickedCount += 1
					pass
				j += JUMP_PIXELS
			i += JUMP_PIXELS

	def run(this):
		while this.mIsRunning == True: 
			while this.mIsPause == False:
				this.checkAndClick()
			time.sleep(0.1)

class Timer(threading.Thread):
	mGameController = None
	mDuration = 0
	def __init__(this, ctrl, dur):
		super(Timer, this).__init__()
		this.mGameController = ctrl
		this.mDuration = dur
		pass
	def run(this):
		while (this.mDuration > 0):
			this.mDuration -= 0.25
			time.sleep(0.25)
		this.mGameController.timeOut()

class GameController(threading.Thread):
	mStartGameButton = None
	mNextGameButton = None
	mCancelSharingButton = None

	mSubThreads = []

	mGameState = 0
	mScreenId = 0
	mLimitOfScreen = 0

	def __init__(this, screenId, limitScreen):
		super(GameController, this).__init__()
		this.mScreenId = screenId
		this.mLimitOfScreen = limitScreen
		if limitScreen == -1 or limitScreen == 0:
			this.mLimitOfScreen = 1
		pass

	def prepare(this, id):
		print("prepare({}) mSubThreads={}".format(id, len(this.mSubThreads)))
		if id == -1:
			print("ERROR: play id is not assigned")
			return
		if len(this.mSubThreads) == 0:
			for i in range(0, NUM_OF_THREAD):
				child = ChildThread(i)
				child.start()
				this.mSubThreads.append(child)
	
	def setPosition(this, id):
		if len(this.mSubThreads) == 0:
			print("ERROR: mSubThreads has not been assinged")
			return
		gameP1 = iPosition()
		gameP2 = iPosition()
		gameP1.x = POINTs[id][0] + 8
		gameP1.y = POINTs[id][1] + 20
		gameP2.x = POINTs[id][2]
		gameP2.y = POINTs[id][3]
		print("assign sub P1({}) P2({})".format(gameP1.toString(), gameP2.toString()))
		for i in range(0, int(NUM_OF_THREAD/2)):
			p1 = iPosition()
			p1.x = gameP1.x
			p1.y = gameP1.y
			p2 = iPosition()
			p2.x = gameP1.x + JUMP_PIXELS + 1
			p2.y = gameP1.y + 1
			p3 = iPosition()
			p3.x = p1.x + int(JUMP_PIXELS/2)
			p3.y = p1.y + 35
			p4 = iPosition()
			p4.x = p2.x
			p4.y = p3.y + 1
			if i == int(NUM_OF_THREAD/2) - 1:
				p4.x = p3.x + 1
				p4.y = p3.y + 1
			this.mSubThreads[i * 2].p1 = p1
			this.mSubThreads[i * 2].p2 = p2
			this.mSubThreads[i * 2 + 1].p1 = p3
			this.mSubThreads[i * 2 + 1].p2 = p4
			print("assign sub thread-{} P1{} P2{}".format(i * 2, p1.toString(), p2.toString()))
			print("assign sub thread-{} P3{} P4{}".format(i * 2 + 1, p3.toString(), p4.toString()))
			gameP1.x += JUMP_PIXELS * 2
		
		this.mStartGameButton = iPosition()
		this.mStartGameButton.x = START_GAME_BUTTONs[id][0]
		this.mStartGameButton.y = START_GAME_BUTTONs[id][1]
		this.mNextGameButton = iPosition()
		this.mNextGameButton.x = NEXT_GAME_BUTTONs[id][0]
		this.mNextGameButton.y = NEXT_GAME_BUTTONs[id][1]
		this.mCancelSharingButton = iPosition()
		this.mCancelSharingButton.x = CANCEL_SHARINGs[id][0]
		this.mCancelSharingButton.y = CANCEL_SHARINGs[id][1]
		print("mStartGameButton({}) mNextGameButton({}) mCancelSharingButton({})".format(this.mStartGameButton.toString(), this.mNextGameButton.toString(), this.mCancelSharingButton.toString()))
	
	def startGame(this):
		print("start game at id=", this.mScreenId)
		pyautogui.click(this.mStartGameButton.x, this.mStartGameButton.y)
		time.sleep(1.5)
		this.resume()

	def nextGame(this):
		print("nextGame")
		pyautogui.click(this.mCancelSharingButton.x, this.mCancelSharingButton.y)
		time.sleep(0.5)
		pyautogui.click(this.mNextGameButton.x, this.mNextGameButton.y)
		time.sleep(0.5)
		this.resume()

	def pauseAfterEndGame(this):
		this.pause()
		clickedCount = 0
		for i in range(0,NUM_OF_THREAD):
			clickedCount += this.mSubThreads[i].getCount()
		print("pauseAfterEndGame count=", clickedCount)
		if clickedCount <  10:
			if this.mScreenId + 1 >= len(POINTs):
				print("Exit Script at last the creen")
				this.exit()
			else:
				this.nextScreen()
		else:
			print("wait next game..")
			timer = Timer(this, 9)
			timer.start()
			this.mGameState = GAME_STATE_WAIT_NEXT_GAME
		pass

	def pause(this):
		print("Pause")
		for i in range(0,NUM_OF_THREAD):
			this.mSubThreads[i].pause()
		this.mGameState = GAME_STATE_PAUSE

	def pauseInPlaying(this):
		print("pauseInPlaying")
		for i in range(0,NUM_OF_THREAD):
			this.mSubThreads[i].pause()
		this.mGameState = GAME_STATE_PAUSE_IN_PLAYING
		
	def resume(this):
		print("Run...")
		for i in range(0,NUM_OF_THREAD):
			this.mSubThreads[i].resume()
		this.mGameState = GAME_STATE_PLAYING
		timer = Timer(this, GAME_PLAY_TIME)
		timer.start()

	def exit(this):
		this.mGameState = GAME_STATE_DEFAULT
		if len(this.mSubThreads) != 0:
			for i in range(0,NUM_OF_THREAD):
				this.mSubThreads[i].exit()

	def nextScreen(this):
		this.mLimitOfScreen -= 1
		if this.mLimitOfScreen == 0:
			print("Reach Limit of Creen. EXIT()")
			this.exit()
		else:
			this.mScreenId = this.mScreenId + 1
			print("===preparing for next screen {}===========================".format(this.mScreenId))
			this.setPosition(this.mScreenId)
			timer = Timer(this, 1.5)
			timer.start()
			this.mGameState = GAME_STATE_NEXTING_SCREEN

	def timeOut(this):
		match this.mGameState:
			case 0:							#GAME_STATE_DEFAULT
				pass
			case 1:							#GAME_STATE_PLAYING
				this.pauseAfterEndGame()
			case 2:							#GAME_STATE_PAUSE
				pass
			case 3:							#GAME_STATE_PAUSE_IN_PLAYING
				this.mGameState = GAME_STATE_PAUSE_BY_USER
				pass
			case 4:							#GAME_STATE_WAIT_NEXT_GAME
				this.nextGame()
			case 5:							#GAME_STATE_NEXTING_SCREEN
				this.startGame()
			case 6:							#GAME_STATE_PAUSE_IN_NEXTING_SCREEN
				this.mGameState = GAME_STATE_PAUSE_BY_USER
				pass
			case 7:							#GAME_STATE_PAUSE_BY_USER
				pass
			case 8:							#GAME_STATE_PAUSE_IN_WAIT_NEXT_GAMGE
				this.mGameState = GAME_STATE_PAUSE_BY_USER
				pass

	def HandleF2Key(this):
		match this.mGameState:
			case 0:							#GAME_STATE_DEFAULT
				this.prepare(this.mScreenId)
				this.setPosition(this.mScreenId)
				this.startGame()
			case 1:							#GAME_STATE_PLAYING
				this.pauseInPlaying()
			case 2:							#GAME_STATE_PAUSE
				this.resume()
			case 3:							#GAME_STATE_PAUSE_IN_PLAYING
				print("can not run/pause in GAME_STATE_PAUSE_IN_PLAYING")
				pass
			case 4:							#GAME_STATE_WAIT_NEXT_GAME
				this.mGameState = GAME_STATE_PAUSE_IN_WAIT_NEXT_GAMGE
			case 5:							#GAME_STATE_NEXTING_SCREEN
				this.mGameState = GAME_STATE_PAUSE_IN_NEXTING_SCREEN
				pass
			case 6:							#GAME_STATE_PAUSE_IN_NEXTING_SCREEN
				print("can not run/pause in GAME_STATE_PAUSE_IN_NEXTING_SCREEN")
				pass
			case 7:							#GAME_STATE_PAUSE_BY_USER
				this.startGame()
			case 8:							#GAME_STATE_PAUSE_IN_WAIT_NEXT_GAMGE
				print("can not run/pause in GAME_STATE_PAUSE_IN_WAIT_NEXT_GAMGE")
				pass

	def getPosition(this):
		p = iPosition()
		p.x, p.y = pyautogui.position()
		print("P=", p.toString())

class ScriptController:
	mGameController = None

	def __init__(this, screenId, numOfScreen):
		this.mGameController = GameController(screenId, numOfScreen)
		pass

	def exit(this):
		this.mGameController.exit()
		listener.stop()
	
	def on_press(this, key):
		if key == Key.f4:
			this.mGameController.getPosition()
		elif key == Key.f2: 
			this.mGameController.HandleF2Key()
		elif key == Key.f1:
			this.mGameController.exit()
			print("__exit__")

###############################################################################
#main start
if len(sys.argv) >= 2:
	gLDplayerId = int(sys.argv[1])
if len(sys.argv) >= 3:
	gNumOfScreens = int(sys.argv[2])

print("play id={} gNumOfScreens={}".format(gLDplayerId, gNumOfScreens))

scriptCtrl = ScriptController(gLDplayerId, gNumOfScreens) 
def on_press(key):
	scriptCtrl.on_press(key)
	if key == Key.f1:
		listener.stop()
		
with Listener(on_press=on_press) as listener: 
	listener.join()
