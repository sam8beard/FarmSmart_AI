import time
import board
from Adafruit_Seesaw.seesaw import Seesaw
from pymongo import MongoClient
from azure.iot.device import IoTHubDeviceClient
import pandas as pd

connection_string = "mongodb+srv://farmsmarttest2025:ruCfjHmv3zNw29H@farmsmart.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
# CONNECTION_STRING = "HostName=Farmsmart-AI.azure-devices.net;DeviceId=RaspberryPi4;SharedAccessKey=ckZXdDGQQYConKkO/d4P6JMw/Iu5RImblqEl8CFzG3M="
CONNECTION_STRING = "HostName=FarmsmartAI.azure-devices.net;DeviceId=farmsmart;SharedAccessKey=ZRdG03Ac45T8AF0UZYb9jYN3yotE7QFk9M+ms3tmxWY="
azure_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
client = MongoClient(connection_string) 
azure_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
azure_client.connect()

db = client["farmsmart-ai"]  
collection = db["moisture-data"] 


i2c_bus = board.I2C()  
ss = Seesaw(i2c_bus, addr=0x36)

while True: 
    touch = ss.moisture_read()
    # Scale value to percentage, 200 (0) = completely dry && 1500 (100) = completely saturated
    scaled_value = ((touch - 200) * 100) / 1300
    touch = scaled_value
    temp = ss.get_temp()

    
    

    if (touch < 30): 
        message = "Moisture level suboptimal: Please water."
        azure_client.send_message(message)
        print("Message successfully sent")
    elif (touch > 70):
        message = "Moisture level subobtimal: Please stop watering."
       
    else:
        message = "Moisture level optimal: No action required." 
    
    
    
    
    
    data = {
        "sensor_id": "RaspberryPi4",
        "temperature": temp,
        "moisture": touch,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "report": message
    }
    
    result = collection.insert_one(data)
    print(f"Document inserted with ID:xx {result.inserted_id}")
    print(f"Moisture Level: {touch}")
    # Collect reading every 5 seconds
    time.sleep(1) 


   