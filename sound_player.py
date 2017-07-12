#!/usr/bin/env python3
# A class handling loading and playing of sounds (abstract out Pygame mixer a little)

import os
import pygame.mixer
from pygame.mixer import Sound

import config

class SoundPlayer:
	'A class to setup the sound system, and keep track of current sound'

	current_sound = None

	def __init__(self):
		print ("Initialising SoundPlayer instance")
		# Prepare pyGame for playing audio
		pygame.mixer.init()
		pygame.mixer.set_num_channels(1) # Ensure we don't get sounds playing over each other

	def __del__(self):
		print ("Destructing SoundPlayer instance")
		# Tidy up the audio
		pygame.mixer.quit()

	def play_sound(self, sound):
		# Check to see if we are already playing the sound (do not want to stop and restart it if we are)
		if sound is not None:

			if sound is not self.current_sound:
				sound.play_sound()

			self.current_sound = sound

class PressureSound:
	'A class handling loading and playing of each sound'

	sound_object  = None

	def __init__(self, sound_folder, sound_filename):
		sound_file = os.path.abspath( os.path.join(os.curdir, config.animals_dir, sound_folder, sound_filename) )
		if os.path.isfile( sound_file ):
			self.sound_object = Sound( sound_file )

	def __del__(self):
		pass

	def play_sound(self):
		# Stop the currently running sound
		pygame.mixer.stop()

		# Play this object's sound
		self.sound_object.play( loops = -1 )
