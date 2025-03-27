import time
import random
import pymongo
from datetime import datetime

# MongoDB Connection Setup
MONGO_URI = "mongodb+srv://farmsmarttest2025:ruCfjHmv3zNw29H@farmsmart.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
client = pymongo.MongoClient(MONGO_URI)
db = client["farm_smart_db"]  # Replace with your actual database name
collection = db["moisture_readings"]  # Replace with your actual collection name

# Simulated moisture level
moisture_level = 30  # Start at a dry soil condition (arbitrary baseline)
max_moisture = 80  # Maximum moisture level to simulate
increment_range = (3, 7)  # How much the value increases per tick

print("Simulated Moisture Sensor Starting...\n")
print("Initial moisture level:", moisture_level, "%\n")

# Function to post data to MongoDB
def post_moisture_reading(level):
    data = {
        "timestamp": datetime.utcnow(),
        "moisture_level": level
    }
    collection.insert_one(data)
    print(f"Posted to MongoDB: {data}")

# Simulating stable dry conditions
dry_period = 10  # Number of cycles before increase starts
for i in range(dry_period):
    print(f"Time: {i+1} sec - Moisture Level: {moisture_level}% (No change)")
    post_moisture_reading(moisture_level)  # Log consistent moisture level
    time.sleep(1)

print("\n--- Sudden Moisture Increase Detected! ---\n")

# Simulating gradual moisture increase
while moisture_level < max_moisture:
    increment = random.randint(*increment_range)
    moisture_level = min(moisture_level + increment, max_moisture)
    print(f"Time: {dry_period+1} sec - Moisture Level: {moisture_level}%")
    post_moisture_reading(moisture_level)
    time.sleep(random.uniform(0.8, 2.5))  # Randomized delay for realism

print("\nFinal moisture level reached. Simulation complete!")
