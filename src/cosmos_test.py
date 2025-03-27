from pymongo import MongoClient

# Your connection string from Azure Cosmos DB
connection_string = "mongodb+srv://farmsmarttest2025:ruCfjHmv3zNw29H@farmsmart.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"

# Create a MongoClient using the connection string
client = MongoClient(connection_string)

# Access the database and collection
db = client["farmsmart-test-1"]  # Replace with your database name
collection = db["test-info"]  # Replace with your collection name

# Example data to insert
data = {
    "sensor_id": "RaspberryPi001",
    "temperature": 22.5,
    "humidity": 60,
    "timestamp": "2025-02-03T12:00:00"
}

# Insert data into the collection
result = collection.insert_one(data)

# Print the inserted document's ID
print(f"Document inserted with ID: {result.inserted_id}")

# Close the connection when done
client.close()
