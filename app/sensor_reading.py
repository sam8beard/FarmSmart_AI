import time
import board
import busio
import pymongo
from datetime import datetime
from adafruit_seesaw.seesaw import Seesaw

# MongoDB Connection Setup
MONGO_URI = "mongodb+srv://farmsmarttest2025:ruCfjHmv3zNw29H@farmsmart.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
client = pymongo.MongoClient(MONGO_URI)
db = client["farm_smart_db"]  # Replace with your actual database name
collection = db["moisture_readings"]  # Replace with your actual collection name

# Initialize I2C connection to Seesaw sensor
i2c_bus = busio.I2C(board.D3, board.D2)
ss = Seesaw(i2c_bus, addr=0x36)

print("FarmSmart Moisture Sensor Starting...\n")

# Function to post data to MongoDB
def post_moisture_reading(moisture, temperature):
    data = {
        "timestamp": datetime.utcnow(),
        "moisture_level": moisture,
        "temperature": temperature
    }
    collection.insert_one(data)
    print(f"Posted to MongoDB: {data}")

# Simulating stable dry conditions
dry_period = 10  # Number of cycles before increase starts
for i in range(dry_period):
    moisture = ss.moisture_read()
    temperature = ss.get_temp()

    print(f"Time: {i+1} sec - Temp: {temperature:.2f}°C  Moisture: {moisture} (No change)")
    post_moisture_reading(moisture, temperature)
    time.sleep(1)

print("\n--- Sudden Moisture Increase Detected! ---\n")

# Simulating gradual moisture increase (actual readings from sensor)
while True:  # Runs indefinitely, mimicking continuous monitoring
    moisture = ss.moisture_read()
    temperature = ss.get_temp()

    print(f"Time: {dry_period+1} sec - Temp: {temperature:.2f}°C  Moisture: {moisture}")
    post_moisture_reading(moisture, temperature)

    time.sleep(3)  # Adjust as needed for realistic monitoring intervals
