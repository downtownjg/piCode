#!/usr/bin/python3

'''
#
# capacitree.python3
# coded by: J. Garrison
# 11/26/2018
#
# credit:
# Code incorporated here from this informative article:
# https://learn.adafruit.com/capacitive-touch-sensors-on-the-raspberry-pi/programming-5-pad-momentary
# by C. Richardson
#
# Also from Dynetics University Class S185 – Introduction to Single Board Computers 
# code template by Greg Abbott & Ben Calahan
#
'''

import time
import os
import subprocess

try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("Error importing RPi.GPIO!")

GPIO.setmode(GPIO.BCM)

#set the GPIO input pins
pad0 = 22 
pad1 = 27
pad2 = 17
pad3 = 24
pad4 = 23

relay = 5

GPIO.setup(pad0, GPIO.IN)
GPIO.setup(pad1, GPIO.IN)
GPIO.setup(pad2, GPIO.IN)
GPIO.setup(pad3, GPIO.IN)
GPIO.setup(pad4, GPIO.IN)
GPIO.setup(relay, GPIO.OUT)

def playMusic(playIt):	
	if not playIt:
		subprocess.call(['killall', 'mpg321'])
	elif playIt:
		subprocess.Popen(['mpg321', 'musicFile.mp3'])

# Define the main() function.
def main():
	pad0alreadyPressed = False
	pad1alreadyPressed = False
	pad2alreadyPressed = False
	pad3alreadyPressed = False
	pad4alreadyPressed = False
	
	superLights = False
	playing = False

	while True:
		pad0pressed = not GPIO.input(pad0)
		pad1pressed = not GPIO.input(pad1)
		pad2pressed = not GPIO.input(pad2)
		pad3pressed = not GPIO.input(pad3)
		pad4pressed = not GPIO.input(pad4)
		
		if pad0pressed and not pad0alreadyPressed:
			print("Pad 0 pressed")
		pad0alreadyPressed = pad0pressed

		# Turn it on while it is being touched
		if pad1pressed and not superLights:
			GPIO.output(relay, True)
			if(not playing):
				playMusic(True)
				playing = True
			print("Pad 1 pressed")
		pad1alreadyPressed = pad1pressed
		
		# Turn it off immediately when you let go
		if not pad1pressed and not superLights:
			GPIO.output(relay, False)
			if(playing):
				playMusic(False)
				playing = False
		pad1alreadyPressed = pad1pressed

		if pad2pressed and not pad2alreadyPressed:
			print("Pad 2 pressed")
		pad2alreadyPressed = pad2pressed

		if pad3pressed and not pad3alreadyPressed:
			print("Pad 3 pressed")
		pad3alreadyPressed = pad3pressed

		# toggle it
		if pad4pressed and not pad4alreadyPressed:			
			superLights = not superLights
			GPIO.output(relay, superLights)
			if superLights and not playing:
				playMusic(True)
				playing = True
			else:
				playMusic(False)
				playing = False
		pad4alreadyPressed = pad4pressed

		time.sleep(0.1)
# EOF: main()
    
# ------------------------------------------------- BEGIN EXECUTION HERE --
if __name__ == '__main__':
	try:
		# Execute code in here first.
		# if an exception is raised, continue to check except blocks.
		# ~~~~~
		# Invoke the main function.
		main()
	except KeyboardInterrupt:
		# If the exception is of this type...
		# Execute this code and continue to 'finally' block.
		# ~~~~~
		# Raised when the user interrupts program execution,
		#	usually by pressing Ctrl+c.
		pass
	finally:
		# No matter what has happened previously, or whether an
		# exception was thrown, execute this code as the program ends.
		# ~~~~~
		print("Cleaning up GPIO pins...")
		# Reset the status of the GPIO pins.
		# NOTE: This will only clean up GPIO channels that your script
		#	has used. This also clears the pin numbering system in use.
		GPIO.cleanup()
