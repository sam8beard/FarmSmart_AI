from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient
from azure.mgmt.monitor import MonitorManagementClient
import os
import datetime
from datetime import timedelta

def retrieve_azure_metrics(): 

    sub_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    
    credential = DefaultAzureCredential() 
    metrics_client = MetricsQueryClient(credential) 
    
    # create client using azure.mgmt.monitor
    # metrics_client = MonitorManagementClient(credential=DefaultAzureCredential(), subscription_id=)

    resource_id = "/subscriptions/08a00de4-716b-46cf-a5c4-3acdb317590a/" \
    "resourceGroups/Farmsmart/providers/Microsoft.Devices/IotHubs/FarmsmartAI"

    # For testing
    # for metric in metrics_client.list_metric_definitions(resource_id, namespace="PublishSuccessCount"): 
    #     print(metric)
    
    try:
        metrics_data_response = metrics_client.query_resource (
        resource_id, 
        metric_names=["d2c.telemetry.ingress.success"], 
        timespan=datetime.timedelta(days=30)
        )
        print("Success")
    except Exception as e:
        print()
        print()
        print()
        print(e) 
        print()
        print()
    
    print(type(metrics_data_response))
    
retrieve_azure_metrics()