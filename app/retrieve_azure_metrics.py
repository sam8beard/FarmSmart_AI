from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient
from azure.mgmt.monitor import MonitorManagementClient
import os
import datetime
from datetime import timedelta
import pandas as pd 
import matplotlib.pyplot as plt 

def retrieve_azure_metrics(): 

    sub_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    
    credential = DefaultAzureCredential() 
    metrics_client = MetricsQueryClient(credential) 
    

    resource_id = "/subscriptions/08a00de4-716b-46cf-a5c4-3acdb317590a/" \
    "resourceGroups/Farmsmart/providers/Microsoft.Devices/IotHubs/FarmsmartAI"

    
    # Retrieve telemetry messages sent in the past 30 days 
    try:
        metrics_data_response = metrics_client.query_resource (
        resource_id, 
        metric_names=["d2c.telemetry.ingress.success"], 
        timespan=datetime.timedelta(days=30),
        aggregations=["Count"],
        granularity=timedelta(days=1)
        )
        print("Success")
    except Exception as e:
        
        print(e) 
       
   

    # retrieve the chosen metric
    telemetry_metric = metrics_data_response.metrics[0]

    # extract all 30 entries 
    days = telemetry_metric.timeseries[0].data

    # create data frame
    df = pd.DataFrame(columns=['Date','Dehydration Pings'])

    # iterate through the past 30 days, create row of each instance, and add row to df
    for day in days: 
        timestamp = day.timestamp
        num_messages = day.count
        truncated_date = datetime.date(timestamp.year, timestamp.month, timestamp.day)
        new_row = pd.DataFrame({'Date': [truncated_date], 'Dehydration Pings': [num_messages]})
        df = pd.concat([df, new_row], ignore_index=True)

    df.to_csv(os.path.join(os.path.dirname(__file__), 'dehydration_pings.csv'), index=False)
    # drop the first column, whatever its name
    df = df.drop(df.columns[0], axis=1)
    # print(df)
    return df        
    
retrieve_azure_metrics()