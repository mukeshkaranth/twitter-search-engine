# Crawling movie-related tweets using TweePy and Indexing using PyLucene

**Note:** Please use an online markdown template rendering tool (<https://dillinger.io/>) to render this README correctly!\
Go to the above mentioned webiste and paste the contents of this README file to view it correctly.
\
This project consists of 3 types of files: python files(.py), bash scripts(.sh) and data files(.csv)
The functionality of this project is three-fold:
- It crawls tweets related to movies from twitter and uses twitter APIs from python's tweepy library.
- It processes the crawled tweets to remove duplicate tweets and disregards re-tweets. It also cleans the tweet text to remove hyperlinks and emojis. Finally, the data is stored in the form of rows in .csv files.
- These files are then indexed using PyLucene's Standard Analyser. tweet_id, created_at and tweet_text are the 3 fields that are indexed for each tweet.
- The user can then query the indexed documents to retrieve a ranked list of the top-k results that match the query terms.

## Usage

- Crawling: This bash Script will help crawl twitter data based on the search query term and number of tweets provided.\

./crawler.sh -c <number_of_tweets> -l <query_or_hashtag>

Example execution:
```bash
./crawler.sh -c 1000000 -l movie
```


- Indexing: This bash Script will help index the stored data to the given directory location using standard analyser.\

./indexbuilder.sh -d <index_directory>

Example execution:
```bash
./indexbuilder.sh -d 'movie_tweet_index/'
```


- Ranking: This bash Script will help crawl twitter data based on the search query term and number of tweets provided.\

./rankingresults.sh -d <index_directory> -c <number_of_required_results> -q <query_string>

Example execution:
```bash
./rankingresults.sh -d 'movie_tweet_index/' -c 5 -q 'movie review'
```

## Troubleshooting
- Please note that you would need to replace the Twitter API keys in the TweetCrawler.py for the crawling to work.
- You would need to install nltk library, pandas library and also the stopwords and punctuation words dataset separately before running the program.
```bash
pip3 install nltk
```
```bash
pip install pandas
```
```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
```
- For any other questions or assistance, please don't hesitate to reach out to <mkara022@ucr.edu>

## Copyrights
This project was done as part of the CS242-Information Retrival course in the University of California, Riverside.
The project was developed under the supervision of professor Vagelis Hristidis.
