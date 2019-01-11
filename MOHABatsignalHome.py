#!/bin/bash

import json
from threading import Thread
from gpiozero import LED, Button # Import GPIO library: https://gpiozero.readthedocs.io/en/stable/
from time import sleep
from losantmqtt import Device # Import Losant library: https://github.com/Losant/losant-mqtt-python

led_gpio = 23
#spot_gpio = 24
button_gpio = 21

led = LED(led_gpio)
spot = LED(spot_gpio)
button = Button(button_gpio, pull_up=False)
active = False

# Construct Losant device
device = Device("5aff0adc1255b000068e852d","6c89c988-179b-4d8c-90c8-3d7039f8524d", "4247fc92b4b2fadfa6e66b9084b747464b5d8d40732fa79efd61dcc1690d6517")

def on_command(device, command):
	print(command["name"] + " command received.")

    # Listen for the gpioControl. This name configured in Losant
	global active
	global led
#	global spot

	if command["name"] == "deactivateLight":
		active = False
		led.off()
#		spot.off()
		print(active)
	if command["name"] == "activateLight":
		active = True
		led.on()
#		spot.on()
		print(active)

	if command["name"] == "sendLight":
		sendLight()

def sendDeviceState():
    print("Sending Device State")
    device.send_state({"button": True})

def sendLight():
    sleep(1)
    print("Sending Light State")
    device.send_state({"light":active})

# Listen for commands.
device.add_event_observer("command", on_command)

print("Listening for device commands")

button.when_pressed = sendDeviceState # Send device state when button is pressed

# Connect to Losant and leave the connection open
device.connect(blocking=True)
