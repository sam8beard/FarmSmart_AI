import spidev
import time

# Set up SPI communication
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI port 0, device 0 (CE0 pin)
spi.max_speed_hz = 1350000  # Max speed for MCP3008 (can vary)

# Function to read the analog value from a channel
def read_channel(channel):
    if channel < 0 or channel > 7:
        raise ValueError("Channel must be between 0 and 7")
    
    # MCP3008 uses a 3-byte message to request data
    # 1st byte: Start bit, Single-ended mode, and channel selection (3 bits)
    # 2nd byte: Data (8 bits), don't care about the MSB, just the 8th bit is used
    # 3rd byte: Data (8 bits), the MSB is the result of the ADC
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    print(f"Raw response for channel {channel}: {r}")
    # The result is in the 10th and 11th bits of the 2nd and 3rd bytes
    adc_value = ((r[1] & 3) << 8) + r[2]
    
    return adc_value

try:
    while True:
        for channel in range(4):  # Test channels 0-3
            value = read_channel(channel)
            print(f"Channel {channel}: {value}")
        time.sleep(1)  # Wait for 1 second before next reading

except KeyboardInterrupt:
    print("Exiting...")
    spi.close()
