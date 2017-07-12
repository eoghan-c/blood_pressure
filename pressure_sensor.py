#!/usr/bin/env python3
# A class to handle the Honeywell SSCDANN015PG2A3 I2C digital pressure sensor
#   http://uk.farnell.com/honeywell/sscdann015pg2a3/sensor-trustability-15psi-3-3v/dp/1823259
#
# Tips from http://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/

import smbus
import time

# i2c bus (0 -- original Pi, 1 -- Rev 2 Pi)
I2CBUS = 1

# Bit masks
status_bit_1_mask       = int(0b1000000000000000)
status_bit_0_mask       = int(0b0100000000000000)
remove_status_bits_mask = int(0b0011111111111111)

class PressureSensor:
	'A class to handle the Honeywell SSCDANN015PG2A3 I2C digital pressure sensor'

	def __init__(self, addr, port=I2CBUS):
		print ("Initialising PressureSensor instance")
		self.addr = addr

		try:
			self.bus  = smbus.SMBus(port)

			# Initialise sensor (necessary?)
			void = self.bus.write_quick(self.addr)

		except:
			raise IOError("Could not find i2c device")

	def __del__(self):
		print ("Destructing PressureSensor instance")

	# Read pressure
	def read_pressure_sensor_count(self):
		# Send read bit '1' as the command
		# https://sensing.honeywell.com/index.php?ci_id=45841
		#self.bus.write_quick(self.addr)

		time.sleep(0.01)

		# Read the 'Two Byte Data Readout'
		try:
			# Tip from Adafruit_GPIO/I2C.py
			# https://github.com/adafruit/Adafruit_Python_GPIO/
			self._buffer = self.bus.read_word_data(self.addr, 0) & 0xFFFF
			self._buffer = ((self._buffer << 8) & 0xFF00) + (self._buffer >> 8)

		except:
			raise IOError("Could not read from i2c device located at %s." % self.addr)

		# Get status bits
		status_bit_1 = (self._buffer & status_bit_1_mask) >> 15
		status_bit_0 = (self._buffer & status_bit_0_mask) >> 14

		# If Status Bits indicate 'normal operation, valid data' (S1=0 & S0=0) then process the value
		if (status_bit_1 is 0) and (status_bit_0 is 0):
			# Remove the status bits from data
			output_count = self._buffer & remove_status_bits_mask
		else:
			output_count = None

		return output_count

	def read_pressure_sensor_psi(self):
		output_count = self.read_pressure_sensor_count()

		if output_count is not None:
			pressure_psi = float((output_count - 1638) * 15) / 13108
		else:
			pressure_psi = None

		return pressure_psi

	def read_pressure_sensor_mmhg(self):
		# Convert PSI to mmHg (pounds per square inch to millimeters of mercury)
		# http://www.sensorsone.com/convert-psi-to-mmhg-barometric-blood/
		pressure_psi  = self.read_pressure_sensor_psi()

		if (pressure_psi == None):
			pressure_mmhg = None
		else:
			pressure_mmhg = pressure_psi * 51.7149241024

		return pressure_mmhg

