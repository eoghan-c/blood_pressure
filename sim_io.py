#!/usr/bin/env python3
# Classes to handle the switches and lights

import RPi.GPIO as GPIO
import time

import config

class IOSetup:
	'A basic class to set up the GPIO mode, and clean it up.'
	# Not very elegant, but can't be a base class of the following classes
	#   because then we'll get multiple setmode's?

	def __init__(self):
		print ("Initialising IOSetup instance")
		# Set up GPIO
		GPIO.setmode(GPIO.BCM)

	def __del__(self):
		print ("Destructing IOSetup instance")
		GPIO.cleanup()


class StopButton:
	'A class to handle the Stop button'

	def __init__(self):
		GPIO.setup(config.stop_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	def __del__(self):
		pass

	def is_pressed(self):
		# Button defined as pull_up, so normally at 1, and 0 is pressed
		# Return stop_mode: Long press = 2 (exit program); Short press = 1 (shutdown)
		stop_mode  = 0

		if GPIO.input(config.stop_button_pin) == GPIO.LOW:
			stop_mode  = 1

			start_time = time.time()
			while GPIO.input(config.stop_button_pin) == GPIO.LOW:
				if time.time() - start_time > 3:
					stop_mode = 2
					break

		if stop_mode > 0:
			print( "      Stop button pressed (stop_mode=" + str(stop_mode) + ")" )

		return stop_mode

class DopplerProbe:
	'A class to handle the reed switch "probe"'

	def __init__(self):
		GPIO.setup(config.doppler_probe_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	def __del__(self):
		pass

	def is_in_position(self):
		# If the reed switch is activated, then the doppler probe is in position
		return GPIO.input(config.doppler_probe_pin) == GPIO.LOW

class AnimalSelector:
	'A class to handle the rotary switch that is used to select "Animals"'

	def __init__(self):
		print ("Initialising IOSetup AnimalSelector instance")
		for animal_num, rotary_switch_pin in config.animal_selector_pins.items():
			GPIO.setup(rotary_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	def __del__(self):
		pass

	def get_selected_animal_num(self):
		# Animals are selected using the rotary switch. Animals numbered 1 to 10
		selected_animal = 1

		for animal_num, rotary_switch_pin in config.animal_selector_pins.items():
			if GPIO.input(rotary_switch_pin) == GPIO.LOW:
				# Pin is connected, so animal animal_num is selected
				selected_animal = animal_num
				break

		return selected_animal
