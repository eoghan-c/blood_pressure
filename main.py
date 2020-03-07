#!/usr/bin/env python3
# A simulation of a Doppler Probe checking blood pressure

import os
import signal
import time

from doppler_probe_sim import DopplerProbeSim

doppler_probe_sim = None

def CatchInterrupt(signalnum, frame):
	if doppler_probe_sim is not None:
		doppler_probe_sim.simulation_status = DopplerProbeSim.Status.stop

# React if the user interrupts the script with Ctrl-C
signal.signal(signal.SIGINT, CatchInterrupt)
# React if our service is stopped
signal.signal(signal.SIGTERM, CatchInterrupt)

try:
	# Set our Activity LED to always on
	#os.system("echo default-on | sudo tee /sys/class/leds/led0/trigger >/dev/null")

	# Create our PressureSensor object, sensor sitting at address 0x28
	doppler_probe_sim = DopplerProbeSim(0x28)

	if doppler_probe_sim is not None:
		# Now run the simulation (for as long as Status is 'run')
		while doppler_probe_sim.simulation_status is DopplerProbeSim.Status.run:
			time.sleep(0.01)
			doppler_probe_sim.play_pressure_sound()

finally:
	shutdown = False

	if doppler_probe_sim is not None:
		shutdown = (doppler_probe_sim.simulation_status is DopplerProbeSim.Status.shutdown)
		del doppler_probe_sim
		doppler_probe_sim = None

	if shutdown:
		# Set our Activity LED back to heartbeat
		#os.system("echo heartbeat | sudo tee /sys/class/leds/led0/trigger >/dev/null")
		#time.sleep(0.1)
		os.system("sudo poweroff")
		
