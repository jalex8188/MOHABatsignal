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

# Construct Losant device
device = Device("5aff0b811255b000068e852e", "1dc7bfa3-60ac-4529-a184-c45d13e08e4e", "aee15624a75f3dc2d36459f33771b6b1f7911c5176e284e9eece22715e7d6aa1")

def on_command(device, command):
	print(command["name"] + " command received.")

    # Listen for the gpioControl. This name configured in Losant
	global active
	global led
	global spot

	if command["name"] == "deactivateLight":
		active = False
		led.off()
		spot.off()
		print(active)
	if command["name"] == "activateLight":
		active = True
		led.on()
		spot.on()
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
