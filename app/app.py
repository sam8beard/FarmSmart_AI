from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo
from random_forest import random_forest
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb+srv://farmsmarttest2025:ruCfjHmv3zNw29H@farmsmart.mongocluster.cosmos.azure.com/farmsmart-test-1?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"

mongo = PyMongo(app)

@app.route('/')
def index(): 

    # FOR TESTING 
    dummy_data = {
        "dates": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05"],
        "growth": [2, 3, 5, 7, 9]
    }

    df_table = random_forest()

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
    
    # return f"<h1>Hello</h1>"
    return render_template('index.html', dummy_data=dummy_data, plot_url=encoded_plot)


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