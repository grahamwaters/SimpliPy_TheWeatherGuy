import requests
import xml.etree.ElementTree as ET

# URLs for RSS feeds
tornados_rss = "https://www.spc.noaa.gov/products/spcwwrss.xml"
tornado_severestorm_mesoscale_convectiveoutlook_fire_rss = "http://www.spc.noaa.gov/products/spcrss.xml"
spcpdswwrss = "https://www.spc.noaa.gov/products/spcpdswwrss.xml"
mesoscalediscs = "https://www.spc.noaa.gov/products/spcmdrss.xml"
convective_outlooks = "http://www.spc.noaa.gov/products/spcacrss.xml"
experimental_public_severe_weather_outlook_multimedia_briefings = "http://www.spc.noaa.gov/products/spcmbrss.xml"

# Make requests to RSS feeds
md_response = requests.get(mesoscalediscs)
tsmcofb_response = requests.get(tornado_severestorm_mesoscale_convectiveoutlook_fire_rss)
eps_response = requests.get(experimental_public_severe_weather_outlook_multimedia_briefings)
#convective_outlooks = requests.get(convective_outlooks)

# Parse XML data
md_root = ET.fromstring(md_response.content)
tsmcofb_root = ET.fromstring(tsmcofb_response.content)
eps_root = ET.fromstring(eps_response.content)
#convect_outlooks_root = ET.fromstring(convective_outlooks.content)

# Get text from items in RSS feeds
md_text = md_root.find("channel").find("item").find("description").text
tsmcofb_text = tsmcofb_root.find("channel").find("item").find("description").text
eps_text = eps_root.find("channel").find("item").find("description").text
#convective_outlooks_text = convect_outlooks_root.find("channel").find("item").find("description").text
# Combine text into report file

with open("report.txt", "w") as report_file:
    report_file.write(md_text)
    report_file.write("\n")
    report_file.write(tsmcofb_text)
    report_file.write("\n")
    report_file.write(eps_text)
    #report_file.write("\n")
    #report_file.write(convective_outlooks_text)


import re

def clean_text(file_path):
    # Open file and read contents
    with open(file_path, "r") as file:
        text = file.read()

    # Remove HTML tags
    text = re.sub(r'<[^>]*>', '', text)

    # Remove ... and replace with a period + newline
    text = re.sub(r'\.\.\.', '\n', text)

    # remove "Read more"
    text = re.sub(r'Read more', '', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove extra empty lines
    text = re.sub(r'\n\s*\n', '\n', text)
    text = text.lower()
    # remove any "*" repeated 3 or more times
    text = re.sub(r'\*{3,}', '', text)
    # remove any "-" repeated 3 or more times
    text = re.sub(r'\-{3,}', '', text)


    # Write cleaned text to file
    with open(file_path, "w") as file:
        file.write(text)

    return text

# Clean the report.txt file
cleaned_text = clean_text("report.txt")
print(cleaned_text)
