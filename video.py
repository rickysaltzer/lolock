# Created By Monstrado
# Description:
# A hook is inserted into the system, upon any mouse down events the 
# system will lock and take a picture with the default webcam. 
#----------------------------

# Import modules
import pyHook
import pythoncom
import os
import sys
import re
import random
import time
import subprocess
from mailer import Mailer
from mailer import Message

# Load camera module
try:
	from VideoCapture import Device
	print("Loading Camera...Done")
except ImportError, e:
	raise ImportError("Dependency Check Failed\nVideoCapture - http://videocapture.sourceforge.net")	# Inform user of dependency issue. 

# Settings (locker)
SNAPSHOT_DIR = "C:\\snaps"     # Snapshot diectory, use two backslashes for paths
COUNT_DOWN = 5 # Define the Final Countdown

# Settings (mailer)
SEND_MAIL = False
SMTP_HOST = 'smtp.domain.com' # SMTP Host
MAIL_FROM = 'lolock@domain.com' # From address
MAIL_TO = 'user@domain.com' # To address
MAIL_SUBJECT = 'LOLOCK - Intruder Detected' # Email subject
MAIL_HTML = "<HTML>Someone tried to touch your computer <i>inappropriately.</i></HTML>" # Email message (HTML)
MAIL_BODY = "Someone tried to touch your computer inappropriately." # Email message (Plain text)

combo=False

def send_email(image):
	# Format email message
	message = Message(From=MAIL_FROM,To=MAIL_TO)
	message.Subject = MAIL_SUBJECT
	message.Html = MAIL_HTML
	message.Body = MAIL_BODY
	message.attach(image)

	# Send message to SMTP server
	sender = Mailer(SMTP_HOST)
	sender.send(message)

def is_black(img):
	# Check if entire image is black (0,0,0)
	# This shit is so ghetto, I know.
	for x in range(0,img.size[0]):
		for y in range(0,img.size[1]):
			if img.getpixel((x,y)) != (0,0,0):
				return False
	return True

def take_picture():
	# Start camera device
	cam = Device()

	# Some machines take longer to initialize the camera and so 
	# black images can occur if the module is loaded too quickly. 
	# We will keep taking images until the image is not completely
	# black.
	while True:
		img = cam.getImage()
		if not is_black(img):
			break
		
	# Get a quick image count in the directory
	image_count = len([fi for fi in os.listdir(SNAPSHOT_DIR) if re.search('.jpg$',fi)])
	if not image_count:
		location = '\\'.join([SNAPSHOT_DIR,'lolock']) + '.jpg'
	else:
		location = '\\'.join([SNAPSHOT_DIR,'lolock.'+str(image_count+1)]) + '.jpg'

	# Save image to disk
	img.save(location)

	# Unload device
	del(cam)

	# Send email if enabled
	if SEND_MAIL:
		send_email(location)

def lock_computer():
	# Lock workstation
	subprocess.Popen("rundll32.exe user32.dll, LockWorkStation")

def check_directory():
	# Check if SNAPSHOT_DIR exists, if it doesn't try to create it.
	if not os.path.exists(SNAPSHOT_DIR):
		try:
			os.makedirs(SNAPSHOT_DIR)
		except:
			raise NameError("Error creating %s directory." % (SNAPSHOT_DIR))

def view_snapshots():
	# Open windows explorer to the snapshot directory
    	subprocess.Popen("explorer %s" % (SNAPSHOT_DIR)) # Run subprocess

def on_click(event):
	lock_computer()
	take_picture()
	view_snapshots()
	sys.exit(1)

def exit_key(event):
	global combo
	if int(event.KeyID) == 74 and combo == True:
		sys.exit(1)

	if int(event.KeyID) == 164:	# Check for ALT key, exit if true
		combo = True
	else:
		combo = False
	
	# pyhook likes for me to return this lol
	return -1

def main():
	# Splash
	print("-"*25)
	print("LOLOCK")
	print("Created By: Monstrado")
	print("-"*25)

	check_directory()

	# Count down from user defined setting
	for sec in range(COUNT_DOWN, 0, -1):
		print("Starting in %d") % sec
    		time.sleep(1)	

	hm = pyHook.HookManager() 	# Start hook manager
	hm.SubscribeMouseAllButtonsDown(on_click) 	# Insert hook
	km = pyHook.HookManager() 	# Start keyboard hook
	km.KeyDown = exit_key 	# Check key press
	km.HookKeyboard() 	# Init keyboard
	hm.HookMouse()		# Init mouse
	print("Hook Inserted...Done")	# Print Hook
	pythoncom.PumpMessages() 	# Start loop
	hm.UnhookMouse()	# Unhook mouse

if __name__ == "__main__":
	main()
