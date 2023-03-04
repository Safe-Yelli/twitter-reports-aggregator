import spacy 
import geopandas as gpd 
import geopy 
import re
import requests

import spacy.cli 

# Download the English language model for efficiency (small size)
spacy.cli.download("en_core_web_sm")

geolocator = geopy.geocoders.Nominatim(user_agent="tweetLocator")

# Find all URLs in a tweet
URLregex = r"(?i)\b((?:https?:\/\/|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}\/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

# For find named locations in tweets
nlp = spacy.load('en_core_web_sm')

def getRedirectURL(url):
    response = requests.get(url, allow_redirects=False)

    # If the response is a redirect, get the final URL
    if response.status_code == 301:
        finalURL =  response.headers['Location']
        # If the response is a Google Maps link, get the final URL
        if "goo.gl/maps/" in  finalURL:
            response = requests.get(url, allow_redirects=True)
            return response.url
        else:
            return finalURL
    else:
        return url
        
def geocode(tweet):
    # Check if the tweet has a Google Maps link
    urls = re.findall(URLregex, tweet.rawContent)
    # print("Attempting to geocode tweet: " + tweet.rawContent)
    for url in urls:
        
        # Get the final URL after redirects
        finalURL = getRedirectURL(url[0])
        print("OG link: " + url[0])
        print("Final link: " + finalURL)

        if "google.com/maps/" in finalURL:
            # Extract the latitude and longitude from the final URL
            # The first set of coords in the URL is the map centre, the second set is the marker
            match = re.search(r"d(-?\d+\.\d+)!4d(-?\d+\.\d+)", finalURL)
            if match:
                lat, lng = match.group(1, 2) # match.group(1) is the first match, match.group(2) is the second match
                return float(lat), float(lng)
    
    # Check if the tweet has a place name
    
    doc = nlp(tweet.rawContent)
    
    for ent in doc.ents:
        print("Attempting to geocode tweet: " + str(ent))
        if ent.label_ in ['GPE', 'LOC']:
            print(ent.text)
            location = geolocator.geocode(ent.text, timeout=4)
            if location:
                return location.latitude, location.longitude
    
    return "NA"
