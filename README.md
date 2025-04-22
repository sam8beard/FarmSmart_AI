# FarmSmart AI

An end‑to‑end IoT and ML platform for soil monitoring.

## Hardware
- **Raspberry Pi 4** with capacitive soil moisture sensor for live moisture readings

## Data Storage
- Aggregates readings in a **MongoDB** cluster

## Telemetry
- Sends moisture‑based recommendation messages to **Azure IoT Hub**

## Machine Learning
- Trains a **Random Forest** regression on historical soil moisture data

## AI Summaries
- Uses a **Weather API** and **OpenAI GPT** to generate plain‑language insights

## Dashboard
- **Flask** app displaying live readings, regression charts, AI summaries, and Azure telemetry data

## Startup
### Install virtual environment
``[py/python3] -m venv .venv``

### Activate virtual envrionment 
``source .venv/bin/activate``

### Install dependencies
``pip install -r requirements.txt``

### Run application
``[py/python3] app/app.py``

