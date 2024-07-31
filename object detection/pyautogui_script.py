import pyautogui

import time 
import threading 
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode, Key

#config mouse position
p1_x = 0
p1_y = 0
p2_x = 0
p2_y = 0
configId = 0
def getPosition():
	global configId, p1_x, p1_x, p1_y, p2_x, p2_y
	if configId == 0:
		point = pyautogui.position()
		p1_x = point.x;
		p1_y = point.y;
		print("get location POIN1 {} {}".format(p1_x, p1_y))
		configId = 1
	else:
		point = pyautogui.position()
		p2_x = point.x;
		p2_y = point.y;
		print("get location POIN2 {} {}".format(p2_x, p2_y))
		configId = 0
		
# config for get color	
#color = (203, 217, 3)
color = (129, 255, 41)
def getColor():
	global color
	p = pyautogui.position()
	r,g,b = pyautogui.pixel(p.x, p.y)
	color = (r, g, b)
	
def detectAndClick():
	screen_img = pyautogui.screenshot()
	x = p2_x
	y = p2_y
	while x >= p1_x:
		while y >= p1_y:
			pixelColor = screen_img.getpixel((x, y))
			if pixelColor == color:
				print("click x={} y={} {}".format(x, y, color))
				pyautogui.click(x, y)
				#return
			y -= 10
		y = p2_y
		x -= 10


# config clicking
delay = 0.05
button = Button.left 
class ClickMouse(threading.Thread): 
	
	def __init__(self, delay, button): 
		super(ClickMouse, self).__init__() 
		self.delay = delay 
		self.button = button 
		self.running = False
		self.program_running = True

	def start_clicking(self): 
		self.running = True

	def stop_clicking(self): 
		self.running = False

	def exit(self): 
		self.stop_clicking() 
		self.program_running = False

	def run(self):
		while self.program_running: 
			while self.running: 
				detectAndClick()
				time.sleep(self.delay) 
			time.sleep(0.1)
	
# config for key listener
def on_press(key):
	if key == Key.f3:
		getColor()
		print("color=".format(color))
	elif key == Key.f4:
		getPosition()
	elif key == Key.f1: 
		if click_thread.running: 
			print("pause")
			click_thread.stop_clicking() 
		else:
			print("start run..")
			click_thread.start_clicking() 
	elif key == Key.f2:
		print("__exit__")
		click_thread.exit() 
		listener.stop() 

# main function
mouse = Controller() 
click_thread = ClickMouse(delay, button) 
click_thread.start()

#add key listener
with Listener(on_press=on_press) as listener: 
	listener.join()
