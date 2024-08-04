import pyautogui

import time 
import threading 
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode, Key

pyautogui.PAUSE = 0.001

JUMP_PIXELS = 20
NUM_OF_THREAD = 17


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
	id = 0
	startTime = 0

	def __init__(this, id):
		super(ChildThread, this).__init__()
		this.id = id
		pass
	
	def pause(this):
		this.mIsPause = True

	def resume(this):
		this.mIsPause = False
		this.startTime = time.time()

	def exit(this):
		this.mIsPause = True
		this.mIsRunning = False

	def checkAndClick(this):
		i = this.p1.x
		j = 0
		while i < this.p2.x:
			if this.mIsPause == True or this.mIsRunning == False:
				break
			
			j = this.p1.y
			while j < this.p2.y:
				if this.mIsPause == True or this.mIsRunning == False:
					break
				if pyautogui.pixelMatchesColor(i, j, (255, 60, 105), tolerance=20):
					#pyautogui.click(i, j)
					pyautogui.click(i, j + 5)
					pass
				j += JUMP_PIXELS
			i += JUMP_PIXELS

	def run(this):
		while this.mIsRunning == True: 
			while this.mIsPause == False:
				if time.time() - this.startTime > 30.5:
					scriptCtrl.pauseAfterEndGame()
					break
				this.checkAndClick()
			time.sleep(0.1)

class ScriptController:
	p1 = None
	p2 = None

	mIsRunning = True
	mIsPause = True
	mSubThreads = []
	mInited = False

	def __init__(this):
		for i in range(0, NUM_OF_THREAD):
			child = ChildThread(i)
			child.start()
			this.mSubThreads.append(child)
		pass

	def canRun(this):
		if this.p1 is None or this.p2 is None:
			return False
		if this.p1.x > this.p2.x or this.p1.y > this.p2.y:
			return False
		return True

	def getPosition(this):
		if this.p1 is None:
			this.p1 = iPosition()
			this.p1.x, this.p1.y = pyautogui.position()
			print("P1=", this.p1.toString())
		elif this.p2 is None:
			this.p2 = iPosition()
			this.p2.x, this.p2.y = pyautogui.position()
			print("P2=", this.p2.toString())
		else:
			#this.p1.x, this.p1.y = pyautogui.position()
			#p2 = None
			print("P1 P1 is set already")

	def pauseAfterEndGame(this):
		if this.mIsPause == False:
			this.pause()
	
	def pause(this):
		this.mIsPause = True
		for i in range(0,NUM_OF_THREAD):
			this.mSubThreads[i].pause()
		print("Pause")

	def resume(this):
		this.mIsPause = False
		for i in range(0,NUM_OF_THREAD):
			this.mSubThreads[i].resume()
		print("Run...")

	def exit(this):
		this.mIsPause = True
		this.mIsRunning = False
		for i in range(0,NUM_OF_THREAD):
			this.mSubThreads[i].exit()

	def assignStartEndPoint(this):
		if this.mInited == True:
			return
		this.mInited = True
		for i in range(0,NUM_OF_THREAD):
			p1 = iPosition()
			p1.x = this.p1.x
			p1.y = this.p1.y + i * JUMP_PIXELS
			p2 = iPosition()
			p2.x = this.p2.x
			p2.y = p1.y + 1
			this.mSubThreads[i].p1 = p1
			this.mSubThreads[i].p2 = p2
			print("assign sub P1({}) P2({})".format(p1.toString(), p2.toString()))


	def on_press(this, key):
		if key == Key.f4:
			this.getPosition()
		elif key == Key.f2: 
			if this.canRun() == False:
				print("ERROR: program is not ready for running")
			else:
				this.assignStartEndPoint()
				if this.mIsPause:
					this.resume()
				else:
					this.pause()
		elif key == Key.f1:
			this.exit()
			print("__exit__")

	def start(this):
		pass

scriptCtrl = ScriptController() 
scriptCtrl.start()

def on_press(key):
	scriptCtrl.on_press(key)
	if key == Key.f1:
		listener.stop()

with Listener(on_press=on_press) as listener: 
	listener.join()
