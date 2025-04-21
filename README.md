
# EXAMPLE REVISED STRUCTURE
FarmSmart/
│
├── src/                  # For the main data collection script
│   ├── moisture_temp.py  # Reads moisture and temperature and posts to MongoDB and IoT
│   └── weather_api.py    # Fetches weather data (you’ll implement this next)
│
├── app/                  # For the Flask app (front-end and back-end combined)
│   ├── static/           # Static files (CSS, images, etc.)
│   ├── templates/        # HTML templates (dashboard UI)
│   ├── routes.py         # Flask routes to serve the dashboard and interact with the DB
│   ├── gpt_summary.py    # Handles GPT API interaction for summaries
│   └── regression.py     # Contains the logic for your regression model
│
├── config/               # Configuration files (API keys, environment variables)
│   └── config.py         # Stores your configurations (DB credentials, API keys)
│
└── requirements.txt      # Dependencies

# THINGS TO DO 

1. Figure out best way to package moisture data and weather api data into one 
    object to post to database 
    - Moisture data is gathered on a loop, while weather data is collected for each
      hour for the next 7 days, all at once
    - Are we training a model on the weather data? 
2. Implement GPT api for AI summary dashboard
    - What will the model be fed and what will we want it to produce? 
    - Recs on future watering habits? Maybe weather information to let the user
      know what to do in the coming week? 
3. Dynamic dashboard updates
    - Will have to do a bit of research on how to implement this in the easiest fashion 
    