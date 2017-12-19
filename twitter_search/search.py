from requests_oauthlib import OAuth1Session, OAuth1
import json
import requests
import urllib
import sys
import io
import os
import re
from bs4 import BeautifulSoup
from IPython import embed

consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_key_secret = os.environ['TWITTER_CONSUMER_KEY_SECRET']
access_token = os.environ['TWITTER_ACCESS_TOKEN']
access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

if __name__ == '__main__':
    arxiv_url = 'https://arxiv.org/abs/1712.04741'

    # fetch article title
    response = requests.get(arxiv_url)
    soup = BeautifulSoup(response.text, "html.parser")
    arxiv_title = soup.find('title').text

    # query search for twitter
    query_word = urllib.parse.quote_plus(arxiv_url + " AND -filter:retweets AND -filter:replies")

    url = "https://api.twitter.com/1.1/search/tweets.json?q=" + query_word
    auth = OAuth1(consumer_key, consumer_key_secret, access_token, access_token_secret)
    response = requests.get(url, auth = auth)
    print('rate-limit-remaining', response.headers['x-rate-limit-remaining'])
    data = response.json()['statuses']

    #データ表示
    for tweet in data:
        text = re.sub('http.+\s?', '', tweet["text"])
        splitted_text = text.split()
        splitted_text_without_title = [x for x in splitted_text if not x in arxiv_title.split()]
        score = len(splitted_text_without_title) / len(splitted_text)
        if score > 0.8 and len(text) > 10:
            print(text, score, len(text))
