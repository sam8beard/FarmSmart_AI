from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo
from random_forest import random_forest
import matplotlib.pyplot as plt
import io
import base64
from summary import gpt_summary
from retrieve_azure_metrics import retrieve_azure_metrics
import pandas as pd
import os
from pymongo import MongoClient
import math
app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb+srv://farmsmarttest2025:ruCfjHmv3zNw29H@farmsmart.mongocluster.cosmos.azure.com/farmsmart-test-1?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
connection_string = "mongodb+srv://farmsmarttest2025:ruCfjHmv3zNw29H@farmsmart.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256…"
client = MongoClient(connection_string)
db = client["farmsmart-ai"]
collection = db["moisture-data"]

mongo = PyMongo(app)

def truncate_float(num, dec): 
    factor = 10.0 ** dec
    return math.trunc(num * factor) / factor

def generate_dehydration_plot(csv_filename='dehydration_pings.csv'):
    # Resolve path relative to this file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, csv_filename)

    # Load CSV from same folder as this script
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])

    # (rest of your plotting code…)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['Date'], df['Dehydration Pings'], marker='o')
    ax.set_title('Daily Dehydration Pings (Last 30 Days)')
    ax.set_xlabel('Date')
    ax.set_ylabel('Count')
    ax.grid(True)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    encoded = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close(fig)

    return encoded

@app.route('/')
def index(): 

    # retrieve latest moisture level
    latest_doc = collection.find_one(sort=[('_id', -1)])
    current_moisture = latest_doc.get('moisture')
    current_moisture = truncate_float(current_moisture, 2)
    

    df_table = random_forest()
    ai_summary = gpt_summary()
    # matplotlib generation from dataframe

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_table['timestamp'], df_table['y_test'], label='Actual Moisture', marker='o')
    ax.plot(df_table['timestamp'], df_table['y_pred'], label='Predicted Moisture', marker='x')
    ax.set_title('Actual vs Predicted Moisture Levels')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Moisture')
    ax.grid(True)
    ax.legend()
    plt.tight_layout()

    # Save plot to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    encoded_plot = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close(fig)  # Avoid memory leaks

    # finds and retrieves a single document from the specified collection 
    test_data = mongo.db['test-info'].find_one()
    
    dehydration_plot = generate_dehydration_plot('dehydration_pings.csv')
    return render_template('index.html', plot_url=encoded_plot, ai_summary=ai_summary, moisture=current_moisture, dehy_plot=dehydration_plot)


# For dynamically updating the page with sensor data - implement later 
# @app.route('/api/data')
# def get_data():
#     # Retrieve all documents from the collection
#     data = list(mongo.db['your_collection_name'].find())
#     # Convert ObjectId to string for JSON serialization
#     for d in data:
#         d['_id'] = str(d['_id'])
#     return jsonify(data)

if __name__ == '__main__': 
    app.run(debug=True)