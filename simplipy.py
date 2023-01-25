import requests
import json
import openai
import time
import sys # for sys.exit()

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


# get the most recent report from report.txt file
with open("report.txt", "r") as report_file:
    most_recent_report = report_file.read()

# Ask user if they want to hear the report
# ready_to_explain = input("Do you want me to try to explain it in simple terms? (y/n) ")
ready_to_explain = True
image_gen = False
if ready_to_explain:
    print("Let me try to explain it in simple terms.")
    time.sleep(1)
    # Use OpenAI to explain report in simple terms
    #!prompt = f"Summarize this weather report, removing complicated words and replacing them with simple explanations, and return a simple weather report:\n {most_recent_report}" # prompt for OpenAI
    prompt = f'Summarize this weather report with no jargon: {most_recent_report}'
    response = openai.Completion.create(engine=openai_engine, prompt=prompt, max_tokens=1000)
    explained_report = response["choices"][0]["text"]
    # the image from the explanation
    if image_gen:
        response_image = openai.ImageCompletion.create(engine=openai_engine, prompt=prompt, max_tokens=1000)
    # save the explanation to a file
    with open("simplipied_weather_report.txt", "w") as explanation_file:
        explanation_file.write(explained_report)
    print(explained_report)
