import smbus
import time

# bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

DEVICE = 0x20  # Device address (A0-A2)
IODIRA = 0x00  # Pin direction register
IODIRB = 0x01  # Pin direction register
OLATA = 0x14  # Register for outputs
OLATB = 0x15  # Register for outputs
GPIOA = 0x12  # Register for inputs

# Set all GPA pins as outputs by setting
# all bits of IODIRA register to 0
bus.write_byte_data(DEVICE, IODIRA, 0x00)

bus.write_byte_data(DEVICE, IODIRB, 0x00)


# Set output all 7 output bits to 0

bus.write_byte_data(DEVICE, OLATA, 192)
bus.write_byte_data(DEVICE, OLATB, 192)
time.sleep(10)

# Set all bits to zero
bus.write_byte_data(DEVICE, OLATA, 0)
bus.write_byte_data(DEVICE, OLATB, 0)