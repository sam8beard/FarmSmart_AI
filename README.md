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


## NOTE: A little more info on the nature of a MetricsQueryResult response

Below is the hierarchal structure of a MetricsQueryResult response as well as a description for each object in the hierarchy. I had issues finding the documentation regarding what each of these objects meant, contained, etc. 

Maybe I'm just a little stupid LOL.

- **`granularity: timedelta | None`**  
  The time‑grain (window size) of each data point. For example, if you asked for 5‑minute granularity you’ll get one value per 5‑minute interval. Note that the service may adjust this grain up or down if your requested interval isn’t supported exactly. 

- **`timespan: str`**  
  The overall interval over which metrics were fetched, formatted as `"<start_iso>/<end_iso>"`. This may differ slightly from your request if the service normalizes it. 

- **`cost: int`**  
  A relative “cost unit” indicating how expensive your query was. Higher numbers mean more work was done behind the scenes to satisfy the request. 

- **`namespace: str | None`**  
  The metric namespace queried (e.g. `"Microsoft.Devices/IotHubs"`). Namespaces group related metrics for a given resource provider. 

- **`resource_region: str | None`**  
  The Azure region where the target resource lives (e.g. `"eastus2"`). Helpful for cross‑region diagnostics. 

- **`metrics: List[Metric]`**  
  The actual metric results. Each entry corresponds to one metric name you asked for. 

---

#### The `Metric` object

Each `Metric` in the `metrics` list has:

- **`id: str`**  
  The full Azure resource‑ID for this specific metric definition. 

- **`type: str`**  
  The ARM resource type of the metric (usually `"<namespace>/metricDefinitions"`). 

- **`name: str`**  
  The programmatic name of the metric (e.g. `"d2c.telemetry.ingress.success"`). 

- **`unit: str`**  
  The unit of measure—common values include `"Count"`, `"Bytes"`, `"Seconds"`, `"Percent"`, etc. 

- **`timeseries: List[TimeSeriesElement]`**  
  One or more independent time series. If you split by dimensions (e.g. per device), you get multiple series; otherwise you usually get a single‑element list. 

---

#### The `TimeSeriesElement` object

Each `TimeSeriesElement` represents one distinct series and contains:

- **`metadata_values: Dict[str, str]`**  
  If you applied a filter or split by dimension, this dict maps each dimension name to its value (e.g. `{"DeviceId": "abc123"}`). If you didn’t filter or split, it’s an empty dict. 

- **`data: List[MetricValue]`**  
  A list of data points, one per time‑grain interval, each described by a `MetricValue` object. 

---

#### The `MetricValue` object

Each entry in the `data` list has:

- **`timestamp: datetime`**  
  When the data was sampled.

- **`average: float | None`**  
  The mean over that interval (if you requested `Average` aggregation).

- **`count: float | None`**  
  How many individual values contributed to the average (useful for understanding sparse data).

- **`minimum: float | None`** / **`maximum: float | None`**  
  The min/max values seen in the interval.

- **`total: float | None`**  
  The sum of all values (if you requested `Total` aggregation).

> Not every field is populated on every call—you only get back the aggregations you asked for. 