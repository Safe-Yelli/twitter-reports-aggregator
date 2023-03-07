import spacy 
import geopandas as gpd 
import geopy 
import re
import requests

import spacy.cli 

# Download the English language model for efficiency (small size)
spacy.cli.download("en_core_web_sm")
# For find named locations in tweets
nlp = spacy.load('en_core_web_sm')

geolocator = geopy.geocoders.Nominatim(user_agent="tweetLocator")

# Find all URLs in the GMaps HTML
htmlCoordRegex = r"@((?:[0-9]{1,2}|1[0-7][0-9]|180)(?:\.[0-9]{2,10})),((?:[0-9]{1,2}|1[0-7][0-9]|180)(?:\.[0-9]{2,10}))"

# URLs with coordinates come with a `!3d` preceding and `!4d` as the delimiter in the URL
urlCoordRegex = r"!3d((?:[0-9]{1,2}|1[0-7][0-9]|180)(?:\.[0-9]{2,16}))!4d((?:[0-9]{1,2}|1[0-7][0-9]|180)(?:\.[0-9]{2,16}))"

# Find all URLs in a tweet
urlRegex = r"(?i)\b((?:https?:\/\/|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}\/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"



def getRedirectURL(url):
    response = requests.get(url, allow_redirects=False)

    # If the response is a redirect, get the final URL
    if response.status_code == 301:
        finalURL =  response.headers['Location']
        # If the response is a Google Maps link, get the redirected URL
        if "goo.gl" or "google.com" in finalURL:
            return followURL(finalURL)
        else:
            return finalURL
    else:
        return url

def followURL(url):
    response = requests.get(url, allow_redirects=True)
    return response.url
    
def geocode(tweet):
    # Check if the tweet has a Google Maps link
    urls = re.findall(urlRegex, tweet.rawContent)
    # print("Attempting to geocode tweet: " + tweet.rawContent)
    for url in urls:
        
        # Get the final URL after redirects
        finalURL = getRedirectURL(url[0])
        print("OG link: " + url[0])
        print("Final link: " + finalURL)

        # Get the coordinates from the final URL OR
        # Search the HTML for the coordinates
        if "google.com/maps/" in finalURL:
            # Extract the latitude and longitude from the final URL
            print("\n finalURL for regexing: " + finalURL)
            match = re.search(urlCoordRegex, finalURL)

            if not match:
                print("URL not matching, attempting to search HTML")
                # If no match found, search through the HTML for the final coords
                finalHTML = requests.get(finalURL).text

                # This regex validates for coordinate formats
                match = re.search(htmlCoordRegex, finalHTML)

            if match:
                # match.group(1) is the first match, match.group(2) is the second match
                lat, lng = match.group(1, 2) 
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
