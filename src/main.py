import snscrape.modules.twitter as twitter
from datetime import datetime
import csv
import re # to remove emojis
import stringOps
from geopy.distance import distance
import yaml

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

hashtags = config['hashtags']
tweet_limit = config['tweet_limit']
bboxCenter = [12.971421, 77.5946]
searchRadius = config['search_radius']

for searchTerm in hashtags:
    # Create a new TwitterScraper object
    tweets_search = twitter.TwitterSearchScraper(searchTerm).get_items()
    raw_tweet_list = []
    final_tweet_list = []


    # Limiting the tweets to the specified limit
    for count, tweet in enumerate(tweets_search):
        if count >= tweet_limit:
            break # reached max
        raw_tweet_list.append(tweet)

    # Filtering the tweets based on the location
    for tweet in raw_tweet_list:
        if tweet.coordinates:
            if distance(bboxCenter, [tweet.coordinates.latitude, tweet.coordinates.longitude]).km <= searchRadius:
                final_tweet_list.append(tweet)

    # Open a CSV file to write the data
    with open('tweet_data.csv', mode='w', encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['searchTerm', 'Location', 'Content', 'Post Date', 'Post Year'])
        # Iterate through the tweets and save the data to the CSV file
        for tweet in final_tweet_list:
            location = [tweet.coordinates.latitude, tweet.coordinates.longitude]
            content = tweet.rawContent
            content = stringOps.removeEmojis(content) #remove emojis
            post_date = tweet.date
            post_day = post_date.strftime("%A")
            post_week = post_date.strftime("%U")
            post_year = post_date.strftime("%Y")
            writer.writerow([searchTerm, location, content, post_date, post_year])
    print(searchTerm + "Data saved to tweet_data.csv")


