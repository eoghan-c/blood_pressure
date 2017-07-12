#!/usr/bin/env python3
# Common global variable configuration file

# Set up the file paths
animals_dir   = 'sounds'

# Set up animal data
# Format:
#    [ 'Human readable name of animal', 'Systolic pressure', 'Diastolic pressure', 'sounds folder name' ]
animals =	{
				1: ['Cat, normal',   100, 80,  'rob_human_normal'],
				2: ['Cat, abnormal', 130, 90, 'rob_human_normal']
			}

# Set up sound file names - these standard names will be used for all sound files
probe_not_in_position_filename = 'probe_not_in_position.wav'
normal_filename                = 'normal.wav'
diastolic_filename             = 'diastolic.wav'
systolic_filename              = 'top_systolic.wav'


##### Switches etc. on GPIO pins ####

# Animal Selector (rotary switch) GPIO pins
animal_selector_pins    = {1: 21, 2: 12, 3: 20, 4: 6, 5: 19, 6: 5, 7: 16, 8: 25, 9: 13, 10: 24}

stop_button_pin   = 22
doppler_probe_pin = 23