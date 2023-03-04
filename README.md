# twitter-report-aggregator
 Collects reports from hashtags and aggregates them into a single CSV file. 

## How to
Change the parameters in the `config.json` file and run the script.
- `hashtags`: The search query to use. See [Twitter's documentation](https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators) for more information.
- `geo_search_enabled`: Whether to search for tweets in a specific area.
- `search_radius`: The radius of the search area in kilometers.
- `since_date`: The date to start searching from. Format: `YYYY-MM-DD`.

## Geocoding
- Gmaps links in the tweet content are parsed and the coordinates are extracted.
- Attempts to geocode with NLP are present, but not complete.

## Regularly scheduled searches
Github Actions runs a workflow at 00:00 UTC every day. It commits a new CSV file to the `data` folder. The file is named after the date it was created.