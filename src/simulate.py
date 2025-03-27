import random
import time

def simulate_adc_reading():
    """
    Simulate a 10-bit ADC reading (0-1023).
    In a real scenario, this would be replaced with actual ADC data.
    """
    return random.randint(0, 1023)

def convert_to_voltage(adc_value, vref=3.3):
    """
    Convert the ADC value to a voltage.
    
    Parameters:
      adc_value (int): The ADC reading (0-1023)
      vref (float): The reference voltage, default is 3.3V.
    
    Returns:
      float: The calculated voltage.
    """
    voltage = (adc_value * vref) / 1023.0
    return voltage

if __name__ == "__main__":
    try:
        while True:
            adc_value = simulate_adc_reading()
            voltage = convert_to_voltage(adc_value)
            print(f"Simulated ADC Reading: {adc_value}, Voltage: {voltage:.2f} V")
            time.sleep(1)  # Delay between readings for demonstration purposes
    except KeyboardInterrupt:
        print("Exiting simulation...")
