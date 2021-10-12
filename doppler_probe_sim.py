#!/usr/bin/env python3
# A simulation of a Doppler Probe checking blood pressure

import RPi.GPIO as GPIO
from enum import Enum

import config
from pressure_sensor import PressureSensor
from animal import Animal
from sound_player import SoundPlayer
import sim_io

pressure_sensor = None
sound_player    = None
gpio_setup      = None
stop_button     = None

class DopplerProbeSim:
	'A class to run the Doppler Probe Simulation'

	# simulation_status is: 'run'; 'stop' (exit program); 'shutdown' (shutdown Raspberry Pi)
	class Status(Enum):
		run      = 1
		stop     = 0
		shutdown = -1

	simulation_status = None

	def __init__(self, sensor_addr):
		print ("Initialising DopplerProbeSim instance")
		# Set up GPIO
		self.gpio_setup      = sim_io.IOSetup()
		self.stop_button     = sim_io.StopButton()
		self.doppler_probe   = sim_io.DopplerProbe()
		self.animal_selector = sim_io.AnimalSelector()

		# Start the simulation
		self.simulation_status = DopplerProbeSim.Status.run

		# Create our PressureSensor object
		self.pressure_sensor = PressureSensor(sensor_addr)

		# Create our Sound Player instance (wrapper for Pygame.mixer)
		self.sound_player = SoundPlayer()

		# Load in all the animal data from the 'config.py' file
		self.animals = {}
		for animal_num, (name, systolic, diastolic, sound_folder) in config.animals.items():
			self.animals[animal_num] = Animal(name, systolic, diastolic, sound_folder)

	def __del__(self):
		print ("Destructing DopplerProbeSim instance")
		self.simulation_status = DopplerProbeSim.Status.stop

	def play_pressure_sound(self):
		# Check whether Stop button has been pressed
		stop_mode = self.stop_button.is_pressed()
		if stop_mode:
			if stop_mode is 1:
				self.simulation_status = DopplerProbeSim.Status.shutdown
			elif stop_mode is 2:
				self.simulation_status = DopplerProbeSim.Status.stop
			return
        
		# Find out which animal we are dealing with
		current_animal_num = self.animal_selector.get_selected_animal_num()

        # Encode a safety mechanism. If selected_animal_num is 10,
        #    then do not require the probe to be placed correctly,
        #    and also set the current_animal_num to 1
        ignore_probe_location = False
        if current_animal_num > 9:
            current_animal_num -= 9; # E.g. if the selector is at '10', select Animal 1
            ignore_probe_location = True
        
        
		# Check current_animal_num actually exists, otherwise set to animal num 1
		if current_animal_num not in self.animals:
			current_animal_num = 1

		current_animal = self.animals[current_animal_num]

		if ignore_probe_location or self.doppler_probe.is_in_position():
			# Discover the current pressure in mmHg
			pressure_mmhg = self.pressure_sensor.read_pressure_sensor_mmhg()

			if pressure_mmhg is not None:
				print (str(current_animal_num) + ": " + str(pressure_mmhg))

				if pressure_mmhg < current_animal.diastolic:
					# Pressure is less than diastolic (lower) threshold
					self.sound_player.play_sound(current_animal.normal_sound)

				elif pressure_mmhg < current_animal.systolic:
					# Pressure is between diastolic (lower) and systolic (higher) threshold
					self.sound_player.play_sound(current_animal.diastolic_sound)

				else:
					# Pressure is above systolic (higher) threshold
					self.sound_player.play_sound(current_animal.systolic_sound)
		else:
			# Doppler probe is not in the correct position
			self.sound_player.play_sound(current_animal.probe_not_in_position_sound)




