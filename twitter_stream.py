# Code downloaded and modified from user bonzanini in github
# https://gist.github.com/bonzanini/af0463b927433c73784d

# Used to collect tweets with specific query and save them in json format

# Original instructions, although they no longer apply
# ##########################################################################
# To run this code, first edit config.py with your configuration, then:
#
# mkdir data
# python twitter_stream_download.py -q apple -d data
# 
# It will produce the list of tweets for the query "apple" 
# in the file data/stream_apple.json
# ##########################################################################

import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import argparse
import string
import config
import json
from datetime import datetime
import os

# Not currently using the parser
def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='-')
    parser.add_argument("-d",
                        "--data-dir",
                        dest="data_dir",
                        help="Output/Data Directory")
    return parser


# Stream API
class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""

    def __init__(self, data_dir, lim_tweets, time_start, time_limit, db_number, time_flag):
        """

        :param data_dir: name of the data dir
        :param lim_tweets: number of tweets to collect (based on time_flag)
        :param time_start: time to start collecting tweets (date)
        :param time_limit: time to stop collecting tweets (date)
        :param db_number: specify a database number (for filename)
        :param time_flag: if true, stream works with time limits, if false, works with tweet limit
        """

        self._db_number = db_number
        self._data_dir = data_dir
        self.outfile = "{}/stream_database{}.json".format(self._data_dir, self._db_number)
        self._lim_tweets = lim_tweets
        self.num_tweets = 0
        self._time_start = time_start
        self._time_limit = time_limit
        self._time_flag = time_flag

    def on_data(self, data):

        # Don't start before _time_start
        if self._time_flag:
            if datetime.today() < self._time_start:
                return True

        # If it is a RT, skip it
        decoded = json.loads(data)
        if 'retweeted_status' in decoded:
            return True

        # Check if file is > 700MB; try because file might not exist yet
        try:
            file_stats = os.stat(self.outfile)
            # If bigger, then continue on a new file
            if file_stats.st_size > 751619276: #1073741824:
                self.new_file()
        except:
            pass

        try:
            with open(self.outfile, 'a') as f:
                # Append tweet to database file
                f.write(data)

                # Control by time limit
                if self._time_flag:
                    if datetime.today() < self._time_limit:
                        return True
                    else:
                        return False
                # Control by number of tweets
                else:
                    self.num_tweets += 1
                    if self.num_tweets < self._lim_tweets:
                        return True
                    else:
                        return False

        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        print(status)
        return True

    # Create new filename for a new database
    def new_file(self):
        self._db_number += 1
        query_fname = format_filename("database" + str(self._db_number))
        self.outfile = "%s/stream_%s.json" % (self._data_dir, query_fname)


def format_filename(fname):
    """Convert file name into a safe string.

    Arguments:
        fname -- the file name to convert
    Return:
        String -- converted file name
    """
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    """Convert a character into '_' if invalid.

    Arguments:
        one_char -- the char to convert
    Return:
        Character -- converted char
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'


def collect_tweets(data_dir, query, lim_tweets, time_start, time_limit, db_number, time_flag):
    #parser = get_parser()
    #args = parser.parse_args()
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)

    twitter_stream = Stream(auth, MyListener(data_dir, lim_tweets, time_start, time_limit, db_number, time_flag))
    # Track query until tweet/time limit is reached
    twitter_stream.filter(track=[query])
