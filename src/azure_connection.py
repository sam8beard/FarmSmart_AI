from azure.iot.device import IoTHubDeviceClient
CONNECTION_STRING = "HostName=Farmsmart-AI.azure-devices.net;DeviceId=RaspberryPiID;SharedAccessKey=ckZXdDGQQYConKkO/d4P6JMw/Iu5RImblqEl8CFzG3M="

def send_message():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    client.connect()
    
    message = "Hello from Raspberry Pi!"
    client.send_message(message)
    
    print("Message successfully sent")
    client.disconnect()

send_message()
