# ****************************************
# profesor/author: Mauricio Matamoros
# student/editor: F.R., G.M.
# date: 2024-04-09
# description: Leer la temperatura por I2C y graficarla desde el archivo de logs.
# ****************************************

import smbus2
import struct
import time

# Arduino's I2C device address
SLAVE_ADDR = 0x0A # I2C Address of Arduino 1

# Initialize the I2C bus;
# RPI version 1 requires smbus.SMBus(0)
i2c = smbus2.SMBus(1)

def readTemperature():
	try:
		msg = smbus2.i2c_msg.read(SLAVE_ADDR, 4)
		i2c.i2c_rdwr(msg)  # Performs write (read request)
		data = list(msg)   # Converts stream to list
		# list to array of bytes (required to decode)
		ba = bytearray()
		for c in data:
			ba.append(int(c))
		# Módificaciones
		temp = struct.unpack('<f', ba)[0] #Obtenemos sólo el valor de la temperatura
		print('Temperatura: ', temp,' °C') #Imprimimos la temperatura
		#
		return temp
	except:
		return None

def main():
	while True:
		try:
			cTemp = readTemperature()
			time.sleep(1)
		except KeyboardInterrupt:
			return

if __name__ == '__main__':
	main()
