import pyautogui

import time 
import threading 
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode, Key

JUMP_PIXELS = 16

class iPosition:
	x = 0
	y = 0
	def __init__(this):
		pass
	def toString(this):
		return "({},{})".format(this.x, this.y)

class ScriptController(threading.Thread):
	p1 = None
	p2 = None
	color = None

	mIsRunning = True
	mIsPause = True

	def __init__(this):
		super(ScriptController, this).__init__() 
		pass

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
			this.p1.x, this.p1.y = pyautogui.position()
			p2 = None
			print("P1=", this.p1.toString())

	def checkAndClick(this):
		i = this.p1.x
		while i < this.p2.x:
			if this.mIsPause == True or this.mIsRunning == False:
				break
			j = this.p1.y
			while j < this.p2.y:
				if this.mIsPause == True or this.mIsRunning == False:
					break
				#pyautogui.click(i, j)
				if pyautogui.pixelMatchesColor(i, j, (255, 60, 105), tolerance=30):
					pyautogui.click(i, j)
					pass
				j += JUMP_PIXELS
			i += JUMP_PIXELS
	def on_press(this, key):
		if key == Key.f4:
			this.getPosition()
		elif key == Key.f1: 
			if this.mIsPause:
				this.mIsPause = False
				print("Run...")
			else:
				this.mIsPause = True
				print("Pause")
		elif key == Key.f2:
			this.mIsPause = True
			this.mIsRunning = False
			print("__exit__")

	def run(this):
		while this.mIsRunning == True: 
			while this.mIsPause == False: 
				this.checkAndClick()
			time.sleep(0.1)

scriptCtrl = ScriptController() 
scriptCtrl.start()

def on_press(key):
	scriptCtrl.on_press(key)
	if key == Key.f2:
		listener.stop()

with Listener(on_press=on_press) as listener: 
	listener.join()
