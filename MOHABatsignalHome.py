 #!/bin/bash

import json
from threading import Thread
from gpiozero import LED, Button # Import GPIO library: https://gpiozero.readthedocs.io/en/stable/
from time import sleep
from losantmqtt import Device # Import Losant library: https://github.com/Losant/losant-mqtt-python

led_gpio = 23
button_gpio = 21

led = LED(led_gpio)
button = Button(button_gpio, pull_up=False)
active = False

#def ledBlink():
#	led.toggle()
#	sleep(1)

# Construct Losant device
device = Device("5aff0adc1255b000068e852d","6c89c988-179b-4d8c-90c8-3d7039f8524d", "4247fc92b4b2fadfa6e66b9084b747464b5d8d40732fa79efd61dcc1690d6517")

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
        global active
        if active == False:
            active = True
            print(active)
        else:
            active = False
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