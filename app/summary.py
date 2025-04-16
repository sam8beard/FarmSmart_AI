import openmeteo_requests
import requests_cache
import pandas as pd
import os
import openai
from retry_requests import retry

def gpt_summary():
    # Set OpenAI API key (this is enough to authenticate)
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Define endpoint and params for the Open-Meteo API
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 33.9609,
        "longitude": -83.3779,
        "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation_probability"]
    }

    # Fetch weather data from Open-Meteo
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    # Process hourly data
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()

    # Prepare data in dictionary form
    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ),
        "temperature_2m": hourly_temperature_2m,
        "relative_humidity_2m": hourly_relative_humidity_2m,
        "precipitation_probability": hourly_precipitation_probability
    }

    # Convert to DataFrame
    hourly_dataframe = pd.DataFrame(data=hourly_data)

    # Prepare the data as a JSON string
    hourly_data_json = hourly_dataframe.to_json(orient="records")

    # Generate recommendation using OpenAI (New API version)
    response = openai.ChatCompletion.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are an expert on farming and consulting fellow farmers on best practices."},
            {"role": "user", "content": f"Based on the following weather data for the next 7 days, return a ~100 word recommendation for the best farming/water practices for the crop being monitored:\n{hourly_data_json}"}
        ],
        max_tokens=200
    )

    # Print the response

    print(response['choices'][0]['message']['content'].strip())
    return response['choices'][0]['message']['content'].strip()