#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time
import atexit
import cwiid, time

#version
version = "MvB0.012"

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)
# define speed
topSpeed = 255
startSpeed = 50
#define button delay to prevent doubling
button_delay = 0.15

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	#unused mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	#unused mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

def turnLeft():
	motors['left'].run(Adafruit_MotorHAT.BACKWARD);
	motors['left'].setSpeed(motorSpeed)
	time.sleep(0.6)
	motors['left'].run(Adafruit_MotorHAT.FORWARD);

def turnRight():
	motors['right'].run(Adafruit_MotorHAT.BACKWARD);
	motors['right'].setSpeed(motorSpeed)
	time.sleep(0.6)
	motors['right'].run(Adafruit_MotorHAT.FORWARD);

def setNewMotorSpeed(motorSpeed):
	if leftMotorStarted:
		motors['left'].setSpeed(motorSpeed)
	if rightMotorStarted:
		motors['right'].setSpeed(motorSpeed)

def rumbleWii():
	wii.rumble = 1 # NOTE: This is how you RUMBLE the Wiimote
	time.sleep(1)
	wii.rumble = 0

def closeWiiConnection():
	rumbleWii()
	wii.close()

def startStopMotor(motor):
	if not rightMotorStarted:
		print('Starting right engine')
		motor.setSpeed(startSpeed)
		motor.run(Adafruit_MotorHAT.FORWARD);
		rightMotorStarted = True
	else:
		print('Stopping right engine')
		motors['right'].run(Adafruit_MotorHAT.RELEASE);
		rightMotorStarted = False

#make sure that engines are turned off at any exit
atexit.register(turnOffMotors)

print('Welcome to RCTruck %s' % version)
#connect and initiatie Wiimote
print('Please press buttons 1 + 2 on your Wiimote now ...')
time.sleep(2)

# This code attempts to connect to your Wiimote and if it fails the program quits
try:
	global wii
	wii = cwiid.Wiimote()
except RuntimeError:
	print('Cannot connect to your Wiimote. Run again and make sure you are holding buttons 1 + 2!')
	exit()

print('Wiimote connection established!\n')
rumbleWii()
print('Press PLUS and MINUS together to disconnect and quit.\n')

#Only start the engines when wiimote is connected successfully
motors = { 'left' : mh.getMotor(1), 'right' : mh.getMotor(2)}

# turn on left and right motors
motors['left'].run(Adafruit_MotorHAT.RELEASE);
motors['right'].run(Adafruit_MotorHAT.RELEASE);

time.sleep(1)

wii.rpt_mode = cwiid.RPT_BTN

leftMotorStarted = False
rightMotorStarted = False
motorSpeed = startSpeed

while True:

	buttons = wii.state['buttons']

	# Detects whether + and - are held down and if they are it quits the program
	if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
		print('\nClosing connection ...')
		closeWiiConnection()
		turnOffMotors()
		exit()

		# The following code detects whether any of the Wiimotes buttons have been pressed and then prints a statement to the screen!
		if (buttons & cwiid.BTN_LEFT):
			print('Slowing down!')
			if (motorSpeed >= 0):
				motorSpeed -= 50
				print('New speed: %i' % motorSpeed)
			else:
				print('Stopped')
				motorSpeed = 0

			setNewMotorSpeed(motorSpeed)
			time.sleep(button_delay)

		if(buttons & cwiid.BTN_RIGHT):
			print('Speeding up!')
			if (motorSpeed <= topSpeed):
				motorSpeed += 50
				print('New speed: %i' % motorSpeed)
			else:
				print('Top speed reached!')

			setNewMotorSpeed(motorSpeed)
			time.sleep(button_delay)

		# Go Left by switching left engine in backup for 1 second
		if (buttons & cwiid.BTN_UP):
			print 'Turning left'
			turnLeft()
			time.sleep(button_delay)

		# Go Right by switching right engine in backup for 1 second
		if (buttons & cwiid.BTN_DOWN):
			print 'Turning right'
			turnRight()
			time.sleep(button_delay)

		if (buttons & cwiid.BTN_1):
			if not leftMotorStarted:
				print('Starting left engine')
				motors['left'].setSpeed(startSpeed)
				motors['left'].run(Adafruit_MotorHAT.FORWARD);
				leftMotorStarted = True
			else:
				print('Stopping left engine')
				motors['left'].run(Adafruit_MotorHAT.RELEASE);
				leftMotorStarted = False

			time.sleep(button_delay)

		if (buttons & cwiid.BTN_2):
			if not rightMotorStarted:
				print('Starting right engine')
				motors['right'].setSpeed(startSpeed)
				motors['right'].run(Adafruit_MotorHAT.FORWARD);
				rightMotorStarted = True
			else:
				print('Stopping right engine')
				motors['right'].run(Adafruit_MotorHAT.RELEASE);
				rightMotorStarted = False

			time.sleep(button_delay)

		if (buttons & cwiid.BTN_A):
			print 'Toettoet!'
			time.sleep(button_delay)

		if (buttons & cwiid.BTN_B):
			rumbleWii()
			if not rightMotorStarted:
				print('Starting right engine')
				motors['right'].setSpeed(startSpeed)
				motors['right'].run(Adafruit_MotorHAT.FORWARD);
				rightMotorStarted = True
			else:
				print('Stopping right engine')
				motors['right'].run(Adafruit_MotorHAT.RELEASE);
				rightMotorStarted = False

			time.sleep(button_delay)

		if (buttons & cwiid.BTN_HOME):
			wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
			check = 0
			while check == 0:
				print(wii.state['acc'])
				time.sleep(0.01)
				check = (buttons & cwiid.BTN_HOME)
			time.sleep(button_delay)

		if (buttons & cwiid.BTN_MINUS):
			#print 'Left pressed'
			time.sleep(button_delay)

		if (buttons & cwiid.BTN_PLUS):
			#  print 'Right pressed'
			time.sleep(button_delay)
