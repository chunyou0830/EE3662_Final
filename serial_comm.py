import serial
import time


def serialWriteInt(ser, value):
	'''
	Send value to serial device and delays for buffering of target device.
	Parameters:
		ser - Serial. Target device object.
		value - Interger. Number to be sent.
	'''
	ser.write(str(value).encode('utf-8'))
	print('Serial write: ' + str(value))
	time.sleep(0.002 * len(str(value)))

def main():
	ser = serial.Serial('/dev/ttyACM0', 9600)
	x = 0
	while True:
		# Rising edge
		while x<255:
			x+=5
			serialWriteInt(ser, x)
		
		# Falling edge
		while x>0:
			x-=5
			serialWriteInt(ser, x)

if __name__ == '__main__':
	main()