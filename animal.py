#!/usr/bin/env python3
# A class defining each simulated animal (holding their pressure thresholds and sounds)

# Blood pressure given as Systolic / Diastolic, e.g. 130 / 90

import os
from sound_player import PressureSound

import config

class Animal:
	'A class defining each simulated animal (holding their pressure thresholds and sounds)'

	probe_not_in_position_sound = None
	normal_sound                = None
	diastolic_sound             = None
	systolic_sound              = None

	def __init__(self, name, systolic, diastolic, sound_folder):
		# Store the threshold pressures
		self.name      = name      # A human-readable name for this animal, e.g. 'Cat, normal'
		self.systolic  = systolic  # High pressure value
		self.diastolic = diastolic # Lower pressure value

		# Read in the sounds
		self.probe_not_in_position_sound = PressureSound( sound_folder, config.probe_not_in_position_filename )
		self.normal_sound                = PressureSound( sound_folder, config.normal_filename )
		self.diastolic_sound             = PressureSound( sound_folder, config.diastolic_filename )
		self.systolic_sound              = PressureSound( sound_folder, config.systolic_filename )

	def __del__(self):
		pass

