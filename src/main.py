import snscrape.modules.twitter as twitter
from datetime import datetime
from datetime import date
import csv
import stringOps
from geopy.distance import distance
import yaml

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

hashtags = config['hashtags']
tweet_limit = config['tweet_limit']
bboxCenter = [12.971421, 77.5946]
searchRadius = config['search_radius']
date_since = 'since:' + config['since_date']
fileName = "data/tweet_data" + "_" + str(date.today()) + ".csv"
geo_search_enabled = config['geo_search_enabled']

# Create a new TwitterScraper object
search_term = hashtags + ' ' + date_since
print(search_term)
tweets_search = twitter.TwitterSearchScraper( search_term, maxEmptyPages=100).get_items()
raw_tweet_list = []
final_tweet_list = []

# # Limiting the tweets to the specified limit
# for count, tweet in enumerate(tweets_search):
#     if count >= tweet_limit:
#         break # reached max
#     raw_tweet_list.append(tweet)

raw_tweet_list = list(tweets_search)
print(hashtags + " tweets scraped")

# Filtering the tweets based on the loc ation
if geo_search_enabled:
    for tweet in raw_tweet_list:
        if tweet.coordinates:
            if distance(bboxCenter, [tweet.coordinates.latitude, tweet.coordinates.longitude]).km <= searchRadius:
                final_tweet_list.append(tweet)
    print(hashtags + " tweets filtered by location")

# Open a CSV file to write the data 
with open(fileName, mode='w', encoding="utf-8") as file:

    file.truncate() #clear file
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
        writer.writerow([hashtags, location, content, post_date, post_year])
print(hashtags + " data saved to file")


