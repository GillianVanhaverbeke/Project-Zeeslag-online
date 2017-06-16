import spidev
import time
import RPi.GPIO as GPIO
import os


class Joystick():
	# Define sensor channels
	# (channels 3 to 7 unused)
	swt_channel = 0
	vrx_channel = 1
	vry_channel = 2

	ActiveRow = 0
	ActiveCollumn = 0

	# Define delay between readings (s)
	delay = 0.2

	# Open SPI bus
	GPIO.setmode(GPIO.BCM)

	spi = spidev.SpiDev()
	spi.open(0, 0)

	LengthMap = 3

	rows = [5, 6, 12]
	collumns = [13, 16, 17]

	def __init__(self):
		for row in self.rows:
			GPIO.setup(row, GPIO.OUT)
			GPIO.output(row, False)

		for collumn in self.collumns:
			GPIO.setup(collumn, GPIO.OUT)
			GPIO.output(collumn, True)

	# Function to read SPI data from MCP3008 chip
	# Channel must be an integer 0-7
	def ReadChannel(self, channel):
		adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
		data = ((adc[1] & 3) << 8) + adc[2]
		return data

	def ClearScreen(self, Length):
		for i in range(Length):
			self.changeRowOff(i)
			self.changeCollumnOff(i)

	def ActivateSelected(self, row, col):
		for i in range(5):
			self.changeRowOn(row)
			self.changeCollumnOn(col)
			print("test")
			time.sleep(self.delay)
			self.changeRowOff(row)
			self.changeCollumnOff(col)
			time.sleep(self.delay)

	def changeCollumnOn(self, selectedRow):
		GPIO.output(self.rows[selectedRow], True)

	def changeCollumnOff(self, selectedRow):
		GPIO.output(self.rows[selectedRow], False)

	def changeRowOn(self, selectedRow):
		GPIO.output(self.collumns[selectedRow], False)

	def changeRowOff(self, selectedRow):
		GPIO.output(self.collumns[selectedRow], True)

	def CheckMapInfo(self, x, y):
		from DbClass import Dbclass
		db = Dbclass()
		db.Connect()
		Used = db.GetMapInfo(x, y)

		return Used

	def ColorMap(self, MapLength):
		for x in range(MapLength):
			for y in range(MapLength):
				info = self.CheckMapInfo(x, y)

				if info == 1:
					self.changeRowOn(x)
					self.changeCollumnOn(y)
					time.sleep(0.005)
					self.changeRowOff(x)
					self.changeCollumnOff(y)

	def StartShot(self, map):
			self.changeCollumnOn(self.ActiveCollumn)
			self.changeRowOn(self.ActiveRow)

			IsSelected = False
			coords = [0,0]

			while IsSelected == False:
				# Read the joystick position data
				vrx_pos = self.ReadChannel(self.vrx_channel)
				vry_pos = self.ReadChannel(self.vry_channel)

				self.ColorMap(map)

				if IsSelected == False:
					if vrx_pos < 50:
						self.changeRowOff(self.ActiveRow)
						self.ActiveRow -= 1

					if vrx_pos > 1000:
						self.changeRowOff(self.ActiveRow)
						self.ActiveRow += 1

					if self.ActiveRow > 2:
						self.ActiveRow = 0
					elif self.ActiveRow < 0:
						self.ActiveRow = 2
					else:
						self.changeRowOn(self.ActiveRow)
					time.sleep(self.delay)

					if vry_pos < 50:
						self.changeCollumnOff(self.ActiveCollumn)
						self.ActiveCollumn -= 1

					if vry_pos > 1000:
						self.changeCollumnOff(self.ActiveCollumn)
						self.ActiveCollumn += 1

					if self.ActiveCollumn > 2:
						self.ActiveCollumn = 0
					elif self.ActiveCollumn < 0:
						self.ActiveCollumn = 2
					else:
						self.changeCollumnOn(self.ActiveCollumn)

					time.sleep(self.delay)

				# Read switch state
				swt_val = self.ReadChannel(self.swt_channel)

				if swt_val < 50:
					coords[0] = self.ActiveRow
					coords[1] = self.ActiveCollumn
					IsSelected = True
					return(coords)

				# Print out results
				print("--------------------------------------------")
				print("X : {}  Y : {}  Switch : {}".format(vrx_pos, vry_pos, swt_val))
