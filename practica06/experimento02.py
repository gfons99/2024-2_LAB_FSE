# ****************************************
# profesor/author: Mauricio Matamoros
# student/editor: F.R., G.M.
# date: 2024-04-09
# description: Leer la temperatura por I2C y graficarla desde el archivo de logs.
# ****************************************

import matplotlib.pyplot as plt
import smbus2
import struct
import time
import threading

# Arduino's I2C device address
SLAVE_ADDR = 0x0A # I2C Address of Arduino 1

# Name of the file in which the log is kept
LOG_FILE = './temp.log'

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
        temp = struct.unpack('<f', ba)
        print('Received temp: {} = {}'.format(data, temp))
        return temp
    except Exception as e:
        print("Error reading temperature:", e)
        return None

def log_temp(temperature):
    try:
        with open(LOG_FILE, 'a') as fp:
            fp.write('{} {}°C\n'.format(
                time.time(),
                temperature
            ))
    except Exception as e:
        print("Error writing to log file:", e)

def plot_temperatures():
    timestamps = []
    temperatures = []
    try:
        with open(LOG_FILE, 'r') as fp:
            for line in fp:
                parts = line.split()
                if len(parts) == 2:
                    timestamp = float(parts[0])
                    temperature = float(parts[1].strip('()°C,'))
                    time_str = time.strftime('%H:%M:%S', time.localtime(timestamp))
                    timestamps.append(time_str)
                    temperatures.append(temperature)
        plt.clf()  # Clear previous plot
        plt.plot(timestamps, temperatures)
        plt.xlabel('Time of Day')
        plt.ylabel('Temperature (°C)')
        plt.title('Historical Temperature')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.pause(0.01)  # Pause to update the plot
    except Exception as e:
        print("Error plotting temperatures:", e)

def temperature_monitor():
    while True:
        try:
            cTemp = readTemperature()
            if cTemp is not None:
                log_temp(cTemp)
                plot_temperatures()  # Plot temperatures after logging
            time.sleep(1)
        except KeyboardInterrupt:
            return

def main():
    # Start temperature monitoring thread
    temp_thread = threading.Thread(target=temperature_monitor)
    temp_thread.daemon = True  # Set as daemon so it will exit when the main thread exits
    temp_thread.start()

    # Plot temperatures
    while True:
        try:
            plot_temperatures()
            time.sleep(10)  # Update plot every 10 seconds
        except KeyboardInterrupt:
            return

if __name__ == '__main__':
    main()
