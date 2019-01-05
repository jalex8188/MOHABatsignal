#!/bin/bash

import json
from threading import Thread
from gpiozero import LED, Button # Import GPIO library: https://gpiozero.readthedocs.io/en/stable/
from time import sleep
from losantmqtt import Device # Import Losant library: https://github.com/Losant/losant-mqtt-python

led_gpio = 23
spot_gpio = 24
button_gpio = 21

led = LED(led_gpio)
spot = LED(spot_gpio)
button = Button(button_gpio, pull_up=False)
active = False

#def ledBlink():
#	led.toggle()
#	sleep(1)

# Construct Losant device
device = Device("5aff0b811255b000068e852e", "1dc7bfa3-60ac-4529-a184-c45d13e08e4e", "aee15624a75f3dc2d36459f33771b6b1f7911c5176e284e9eece22715e7d6aa1")

#def main_loop():
#	mythread = LedThread()
#	mythread.start()

#class LedThread(Thread):
#
#	def _init_(self):
#		super(LedThread, self)._init_()
#		self._keepgoing = True
#	def run(self):
#		while (self._keepgoing):
#			print 'Blink'
#			time.sleep(0.5)
#
#	def stop(self):
#		self._keepgoing = False

def on_command(device, command):
    print(command["name"] + " command received.")

    # Listen for the gpioControl. This name configured in Losant
    if command["name"] == "toggle":
        # toggle the LED
	        led.toggle()
		spot.toggle()
		global active
		if active == True:
			active = False
			print(active)
		else:
			active = True
			print(active)

def sendDeviceState():
    print("Sending Device State")
    device.send_state({"button": True})

# Listen for commands.
device.add_event_observer("command", on_command)

print("Listening for device commands")

button.when_pressed = sendDeviceState # Send device state when button is pressed

# Connect to Losant and leave the connection open
device.connect(blocking=True)

#def led_flash():
#	global active
#	if active == True:
#		led.toggle
#		sleep(1)
#	led.toggle
#	time.sleep(1)

#main_loop()
#ledBlink()
