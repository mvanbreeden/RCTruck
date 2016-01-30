#!/usr/bin/python
# Copyright (c) 2016 Marcel van Breeden
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the added License file.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# For more info on Adafruit libs and set up see:
# https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/installing-software

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time
import atexit
import cwiid, time

#version
version = "MvB0.15"

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)
# define speed
topSpeed = 300
startSpeed = 40
#define button delay to prevent doubling
button_delay = 0.15

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	#unused mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	#unused mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

def turn(direction):
	if motorSpeed > 0:
		motors[direction].run(Adafruit_MotorHAT.BACKWARD)
		motors[direction].setSpeed(motorSpeed)
		time.sleep(0.3)
		motors[direction].run(Adafruit_MotorHAT.FORWARD)
	else:
		motors[direction].run(Adafruit_MotorHAT.FORWARD)
		motors[direction].setSpeed(motorSpeed)
		time.sleep(0.3)
		motors[direction].run(Adafruit_MotorHAT.BACKWARD)

def setNewMotorSpeed(motorSpeed):
	if motorStarted['left']:
		if motorSpeed > 0:
			print('Left Going forward')
			motors['left'].run(Adafruit_MotorHAT.FORWARD)
		else:
			print('Left Going backward')
			motors['left'].run(Adafruit_MotorHAT.BACKWARD)

		motors['left'].setSpeed(abs(motorSpeed))

	if motorStarted['right']:
            if motorSpeed > 0:
				print('Right Going forward')
				motors['right'].run(Adafruit_MotorHAT.FORWARD)
            else:
				print('Right Going backward')
				motors['right'].run(Adafruit_MotorHAT.BACKWARD)

			motors['right'].setSpeed(abs(motorSpeed))

def rumbleWii():
	wii.rumble = 1 # NOTE: This is how you RUMBLE the Wiimote
	time.sleep(1)
	wii.rumble = 0

def closeWiiConnection():
	rumbleWii()
	wii.close()

def spinTruck(on):
	if on = True:
		motors['left'].run(Adafruit_MotorHAT.BACKWARD)
		motors['right'].run(Adafruit_MotorHAT.FORWARD)
		motors['left'].setSpeed(topSpeed)
		motors['right'].setSpeed(topSpeed)
	else:
		motors['left'].run(Adafruit_MotorHAT.FORWARD)
		motors['right'].run(Adafruit_MotorHAT.FORWARD)
		motors['left'].setSpeed(0)
		motors['right'].setSpeed(0)
		motorSpeed = 0


def startStopMotor(motor):
	if not motorStarted[motor]:
		print('Starting %s engine' & motor)
		motors[motor].setSpeed(startSpeed)
		motors[motor].run(Adafruit_MotorHAT.FORWARD);
		motorStarted[motor] = True
	else:
		print('Stopping %s engine' & motor)
		motors[motor].run(Adafruit_MotorHAT.RELEASE);
		motorStarted[motor] = False

def main():
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
	motorStarted = { 'left': False, 'right' : False}

	# turn on left and right motors
	motors['left'].run(Adafruit_MotorHAT.RELEASE)
	motors['right'].run(Adafruit_MotorHAT.RELEASE)

	time.sleep(1)

	wii.rpt_mode = cwiid.RPT_BTN

	motorSpeed = startSpeed
	truckSpinning = False

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
			motorSpeed -= 50
			print('New speed: %i' % motorSpeed)

			setNewMotorSpeed(motorSpeed)
			time.sleep(button_delay)

		if(buttons & cwiid.BTN_RIGHT):
			print('Speeding up!')
			motorSpeed += 50
			print('New speed: %i' % motorSpeed)

			setNewMotorSpeed(motorSpeed)
			time.sleep(button_delay)

		# Go Left by switching left engine in backup for 1 second
		if (buttons & cwiid.BTN_UP):
			print 'Turning left'
			turn('left')
			time.sleep(button_delay)

		# Go Right by switching right engine in backup for 1 second
		if (buttons & cwiid.BTN_DOWN):
			print 'Turning right'
			turn('right')
			time.sleep(button_delay)

		# Start or stop the left engine
		if (buttons & cwiid.BTN_1):
			startStopMotor('left')
			time.sleep(button_delay)

		# Start or stop the right engine
		if (buttons & cwiid.BTN_2):
			startStopMotor('right')
			time.sleep(button_delay)

		if (buttons & cwiid.BTN_A):
			if truckSpinning = True:
				print 'Stopping spinning!'
				spinTruck(False)
				truckSpinning = False
			else:
				print 'Start spinning!'
				spinTruck(True)
				truckSpinning = True

			time.sleep(button_delay)

		if (buttons & cwiid.BTN_B):
			rumbleWii()
			time.sleep(button_delay)

		if (buttons & cwiid.BTN_HOME):
			wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
			homeButtonStillPressed = 0
			while homeButtonStillPressed == 0:
				print(wii.state['acc'])
				time.sleep(0.01)
				homeButtonStillPressed = (buttons & cwiid.BTN_HOME)
			time.sleep(button_delay)

		if (buttons & cwiid.BTN_MINUS):
			#print 'Left pressed'
			time.sleep(button_delay)

		if (buttons & cwiid.BTN_PLUS):
			#  print 'Right pressed'
			time.sleep(button_delay)


if __name__ == "__main__":
    main()
