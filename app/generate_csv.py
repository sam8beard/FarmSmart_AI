import pymongo
import csv
import os
    
def create_csv():
    client = pymongo.MongoClient('mongodb+srv://farmsmarttest2025:ruCfjHmv3zNw29H@farmsmart.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000')
    db = client['farmsmart-ai']
    coll = db['moisture-data']
    # returns an object that iterates throgh the collection
    mongo_client = next(coll.find(), None)
    docs = coll.find()
    # need to specify the name of the fields that I want from the CSV
    fieldnames = list(mongo_client.keys())
    fieldnames.remove('_id')
    # print(str(fieldnames))

    #retireve the absolute path of this file so that moisture_csv will always be added to the same folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "moisture_data.csv")

    with open(file_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for doc in docs:
            writer.writerow({k: doc.get(k, "") for k in fieldnames})