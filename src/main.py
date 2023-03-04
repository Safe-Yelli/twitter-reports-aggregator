import snscrape.modules.twitter as twitter
from datetime import datetime, date

import yaml
import pandas as pd

import stringOps
import geocoder

# Load config file
with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
# Twitter advanced search format
search_term = config['searchTerm']
# Date range to search from
date_since = 'since:' + config['since_date']
# Add date range to search term
search_term = search_term + ' ' + date_since
# For bounding tweets to a bbox
bboxCenter = [12.971421, 77.5946]
geo_search_enabled = config['geo_search_enabled']
searchRadius = config['search_radius']
# File name to save to
file_name = "data/tweet_data" + "_" + str(date.today()) + ".csv"

# list to store tweets
raw_tweet_list = []
final_tweet_list = []

def twitterGeoSearch(raw_tweet_list):
    from geopy.distance import distance
    for tweet in raw_tweet_list:
        if tweet.coordinates:
            if distance(bboxCenter, [tweet.coordinates.latitude, tweet.coordinates.longitude]).km <= searchRadius:
                final_tweet_list.append(tweet)
    print(search_term + " tweets filtered by location")
    return final_tweet_list

def main():
    raw_tweet_list = twitter.TwitterSearchScraper( search_term, maxEmptyPages=100).get_items()
    print(search_term + " tweets scraped")
    
    if geo_search_enabled:
        raw_tweet_list = twitterGeoSearch(raw_tweet_list)

    # Create an empty DataFrame to store the data
    df = pd.DataFrame(columns=['searchTerm', 'Location', 'Content', 'Post Date', 'Post Year'])

    # Iterate through the tweets and add the data for each tweet to the DataFrame
    for tweet in raw_tweet_list:
        # if tweet.coordinates:
        #     location = [tweet.coordinates.latitude, tweet.coordinates.longitude]
        # else:
        location = geocoder.geocode(tweet)
        content = tweet.rawContent
        content = stringOps.removeEmojis(content) #remove emojis
        post_date = tweet.date
        # post_day = post_date.strftime("%A")
        # post_week = post_date.strftime("%U")
        post_year = post_date.strftime("%Y")
        df = df.append({'searchTerm': search_term, 'Location': location, 'Content': content, 'Post Date': post_date, 'Post Year': post_year}, ignore_index=True)

    # Write the DataFrame to a CSV file
    df.to_csv(file_name, index=True)
    print(search_term + " data saved to file")

if __name__ == "__main__":
    main()

    
    






