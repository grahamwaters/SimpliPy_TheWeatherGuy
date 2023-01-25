import requests
import json
import openai

# load the secrets file
with open("secrets.json") as f:
    secrets = json.load(f)

# Set up OpenAI API key
openai.api_key = secrets["openai_api_key"]
openai_engine = secrets["openai_engine"]

# # Make request to National Weather Service website
# https://api.weather.gov/points/{latitude},{longitude}
# For example: https://api.weather.gov/points/39.7456,-97.0892
# This returns a URL to the nearest weather station

# Get Latitude and Longitude from user's secrets file
latitude = secrets["latitude"]
longitude = secrets["longitude"]
state = secrets["state"]

# Get URL to nearest weather station (beta)
#url = f"https://api.weather.gov/points/{latitude},{longitude}"
#response = requests.get(url)

url = "https://api.weather.gov/alerts/active/area/{}".format(state)
response = requests.get(url)
data = json.loads(response.text)

# Get most recent severe weather report
most_recent_report = data["features"][0]["properties"]

# Use OpenAI to explain report in simple terms
prompt = f"Explain the following severe weather report in simple terms: {most_recent_report['description']}"
response = openai.Completion.create(engine=openai_engine, prompt=prompt)
explained_report = response["choices"][0]["text"]

print(explained_report)
