from DbClass import Dbclass
import RPi.GPIO as GPIO
import spidev
import smbus
import time

# bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

class BattleShipGame:
	rows = [5, 6, 12]
	collumns = [13, 16, 17]

	boats = [1, 1, 2]

	delay = 0.005

	GPIO.setmode(GPIO.BCM)

	ROW1 = 0x20  # Device address (A0-A2)
	ROW2 = 0x21
	ROW3 = 0x22
	ROW4 = 0x23
	ROW5 = 0x24
	ROW6 = 0x25
	ROW7 = 0x26
	ROW8 = 0x27
	IODIRA = 0x00  # Pin direction register
	IODIRB = 0x01  # Pin direction register
	OLATA = 0x14  # Register for outputs
	OLATB = 0x15  # Register for outputs
	GPIOA = 0x12  # Register for inputs

	HP = 0
	LengthMap = 3
	coords = [0, 0]

	swt_channel = 0
	vrx_channel = 1
	vry_channel = 2

	spi = spidev.SpiDev()
	spi.open(0, 0)

	def __init__(self):
		bus.write_byte_data(self.ROW1, self.IODIRA, 0x00)
		bus.write_byte_data(self.ROW1, self.IODIRB, 0x00)

		# bus.write_byte_data(self.ROW2, self.IODIRA, 0x00)
		# bus.write_byte_data(self.ROW3, self.IODIRA, 0x00)
		# bus.write_byte_data(self.ROW4, self.IODIRA, 0x00)
		# bus.write_byte_data(self.ROW5, self.IODIRA, 0x00)
		# bus.write_byte_data(self.ROW6, self.IODIRA, 0x00)
		# bus.write_byte_data(self.ROW7, self.IODIRA, 0x00)
		# bus.write_byte_data(self.ROW8, self.IODIRA, 0x00)

		# Set output all 7 output bits to 0
		bus.write_byte_data(self.ROW1, self.OLATA, 0)
		bus.write_byte_data(self.ROW1, self.OLATB, 0)

		# bus.write_byte_data(self.ROW2, self.OLATA, 0)
		# bus.write_byte_data(self.ROW3, self.OLATA, 0)
		# bus.write_byte_data(self.ROW4, self.OLATA, 0)
		# bus.write_byte_data(self.ROW5, self.OLATA, 0)
		# bus.write_byte_data(self.ROW6, self.OLATA, 0)
		# bus.write_byte_data(self.ROW7, self.OLATA, 0)
		# bus.write_byte_data(self.ROW8, self.OLATA, 0)

	def StartGame(self):
		db = Dbclass()
		db.ClearMap()
		self.ClearScreen(self.LengthMap)

		self.HP = 0

		for i in self.boats:
			self.HP += self.boats[i]

		for boat in self.boats:
			self.ClearCoord()
			self.ClearScreen(self.LengthMap)

			coord = self.GetCoords()
			self.SetBoat(coord[0], coord[1], boat)

		try:
			while self.HP > 0:
				coord = self.GetCoords()
				self.shootCell(coord[0], coord[1])
		except KeyboardInterrupt:
			GPIO.cleanup()

		if self.HP == 0:
			print("alles is dood")
			return 1


	def GetCoords(self):
		XY = self.StartShot(self.LengthMap)
		return XY
	def ClearCoord(self):
		self.coords[0] = 0
		self.coords[1] = 0

	def changeCollumnOn(self, selectedRow):
		GPIO.output(self.rows[selectedRow], True)
	def changeCollumnOff(self, selectedRow):
		GPIO.output(self.rows[selectedRow], False)
	def changeRowOn(self, selectedRow):
		GPIO.output(self.collumns[selectedRow], False)
	def changeRowOff(self, selectedRow):
		GPIO.output(self.collumns[selectedRow], True)

	def ClearScreen(self, Length):
		for i in range(Length):
			self.changeRowOff(i)
			self.changeCollumnOff(i)

	def SetBoat(self, x, y, boatLength):
		db = Dbclass()

		for l in range(boatLength):
			IsSpotUsed = self.CheckMapInfo(x + l, y)
			if IsSpotUsed == 0:
				db.Connect()
				db.SetBoatOnMap(x + l, y)

				self.changeRowOn(x + l)
				self.changeCollumnOn(y)
			else:
				print("spot is used")
		self.ClearCoord()

	def shootCell(self, x, y):
		db = Dbclass()
		isSpotUsed = self.CheckMapInfo(x, y)

		if isSpotUsed == 0:
			print("spot  empty, you missed!")
			db.SetMissOnMap(x, y)
		elif isSpotUsed == 1:
			print("You hit a boat!")
			self.HP -= 1
			db.SetHitOnMap(x, y)

	def CheckMapInfo(self, x, y):
		db = Dbclass()
		Used = db.GetMapInfo(x, y)

		return Used

	def ColorMap(self, MapLength):
		for x in range(MapLength):
			for y in range(MapLength):
				print("x : {}, Y : {}".format(x, y))
				info = self.CheckMapInfo(x, y)
				print("INFO : {}".format(info))
				if y == 0 or y == 4:
					if info == 0:
						totalSend += 1
					elif info == 1:
						totalSend += 3
					elif info == 2:
						totalSend += 2
				else:
					if y == 1 or y == 5:
						maal = 4
					elif y == 2 or y == 6:
						maal = 16
					elif y == 3 or y == 7:
						maal = 64

					print("MAAL : {}".format(maal))
					if info == 0:
						totalSend = totalSend + maal
					elif info == 1:
						color = 3
						totalSend = totalSend + (color * maal)
					elif info == 2:
						color = 2
						totalSend = totalSend + (color * maal)
				print(totalSend)

				if y < 4:
					self.ColorRowTop(x, totalSend)
				else:
					self.ColorRowBot(x, totalSend)

				# self.changeRowOn(x)
				# self.changeCollumnOn(y)
				# time.sleep(self.delay)
				# self.changeRowOff(x)
				# self.changeCollumnOff(y)

	def ColorRowTop(self, row, sendVal):
		if row == 0:
			bus.write_byte_data(self.ROW1, self.OLATA, sendVal)
		elif row == 1:
			bus.write_byte_data(self.ROW2, self.OLATA, sendVal)
		elif row == 2:
			bus.write_byte_data(self.ROW3, self.OLATA, sendVal)
		elif row == 3:
			bus.write_byte_data(self.ROW4, self.OLATA, sendVal)
		elif row == 4:
			bus.write_byte_data(self.ROW5, self.OLATA, sendVal)
		elif row == 5:
			bus.write_byte_data(self.ROW6, self.OLATA, sendVal)
		elif row == 6:
			bus.write_byte_data(self.ROW7, self.OLATA, sendVal)
		elif row == 7:
			bus.write_byte_data(self.ROW8, self.OLATA, sendVal)

	def ColorRowBot(self, row, sendVal):
		if row == 0:
			bus.write_byte_data(self.ROW1, self.OLATB, sendVal)
		elif row == 1:
			bus.write_byte_data(self.ROW2, self.OLATA, sendVal)
		elif row == 2:
			bus.write_byte_data(self.ROW3, self.OLATA, sendVal)
		elif row == 3:
			bus.write_byte_data(self.ROW4, self.OLATA, sendVal)
		elif row == 4:
			bus.write_byte_data(self.ROW5, self.OLATA, sendVal)
		elif row == 5:
			bus.write_byte_data(self.ROW6, self.OLATA, sendVal)
		elif row == 6:
			bus.write_byte_data(self.ROW7, self.OLATA, sendVal)
		elif row == 7:
			bus.write_byte_data(self.ROW8, self.OLATA, sendVal)

	def ReadChannel(self, channel):
		adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
		data = ((adc[1] & 3) << 8) + adc[2]
		return data

	def StartShot(self, map):
			self.changeCollumnOn(self.coords[0])
			self.changeRowOn(self.coords[1])

			IsSelected = False

			while IsSelected == False:
				# Read the joystick position data
				vrx_pos = self.ReadChannel(self.vrx_channel)
				vry_pos = self.ReadChannel(self.vry_channel)

				self.ColorMap(map)

				if IsSelected == False:
					if vrx_pos < 50:
						self.coords[0] -= 1

					if vrx_pos > 1000:
						self.coords[0]+= 1

					if self.coords[0] > 2:
						self.coords[0] = 0
					elif self.coords[0] < 0:
						self.coords[0] = 2

					if vry_pos < 50:
						self.changeCollumnOff(self.coords[1])
						self.coords[1] -= 1


					if vry_pos > 1000:
						self.changeCollumnOff(self.coords[1])
						self.coords[1] += 1

					if self.coords[1] > 2:
						self.coords[1] = 0
					elif self.coords[1] < 0:
						self.coords[1] = 2
					else:
						self.changeCollumnOn(self.coords[1])

				self.changeRowOn(self.coords[0])
				self.changeCollumnOn(self.coords[1])
				time.sleep(self.delay)
				self.changeRowOff(self.coords[0])
				self.changeCollumnOff(self.coords[1])

				# Read switch state
				swt_val = self.ReadChannel(self.swt_channel)

				if swt_val < 50:
					return(self.coords)

				# Print out results
				print("--------------------------------------------")
				print("X : {}  Y : {}  Switch : {}".format(vrx_pos, vry_pos, swt_val))

spel = BattleShipGame()
print("color")

# Set all GPA pins as outputs by setting
# all bits of IODIRA register to 0

spel.ColorRowTop(0, 255)
spel.ColorRowBot(0, 255)