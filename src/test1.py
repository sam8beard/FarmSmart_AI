import time
import smbus2

# Initialize I2C bus (1 is for /dev/i2c-1 on Raspberry Pi)
bus = smbus2.SMBus(1)

# PCF8591 I2C address (default address)
pcf_address = 0x48

def read_moisture():
    # # Send control byte to read AIN1
    # bus.write_byte(pcf_address, 0x01)  # 0x01 for AIN1
    # time.sleep(0.1)  # Delay for the conversion to finish
    
    # # Read two bytes of data (for the 8-bit resolution)
    # data = bus.read_i2c_block_data(pcf_address, 0x00, 2)  # Read 2 bytes from the sensor
    
    # # Combine the bytes into a single value
    # moisture_value = (data[0] << 8) + data[1]  # Combine bytes into a single value
    # return moisture_value
    # Send control byte to read AIN1
    bus.write_byte(pcf_address, 0x01)  # 0x01 for AIN1
    time.sleep(0.1)  # Delay for the conversion to finish
    
    # Read two bytes of data (for the 8-bit resolution)
    data = bus.read_i2c_block_data(pcf_address, 0x00, 2)  # Read 2 bytes from the sensor
    
    # Combine the bytes into a single value (16-bit value)
    moisture_value = (data[0] << 8) + data[1]  # Combine bytes into a single value
    
    # Rescale the value to be within 8-bit range (0-255)
    moisture_value = moisture_value % 256  # This limits the value to the range 0-255
    
    return moisture_value

    

   

try:
    while True:
        moisture = read_moisture()
        print(f"Raw Moisture Sensor value: {moisture}")  # Print raw value to debug
        time.sleep(1)  # Wait 1 second before next reading
except KeyboardInterrupt:
    print("Exiting...")  # Exit on CTRL+C
