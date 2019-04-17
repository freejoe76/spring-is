#!/usr/bin/env python3
from datetime import date
import os, sys
import time
import random
import doctest
import argparse
import tweepy
from collections import OrderedDict

class Spring:
    ''' A class for managing a set of tweets that are supposed to be tweeted on
        specific days, year after year.
        '''

    def __init__(self):
        ''' Make a new Spring object.
            >>> s = Spring()
            '''
        try:
            self.volume = self.file_get_contents('_volume')
        except:
            self.setup()
            return None
        self.base_year = int(self.file_get_contents('_year')) + int(self.volume)
        lines = {
            'YYYY-03-22': '''Spring Is Here
  Taro Gomi
  volume X''',
            'YYYY-03-25': 'Spring is here.',
            'YYYY-04-03': 'The snow melts.',
            'YYYY-04-09': 'The earth is fresh.',
            'YYYY-05-01': 'The grass sprouts.',
            'YYYY-05-21': 'The flowers bloom.',
            'YYYY-06-04': 'The grass grows.',
            'YYYY-07-12': 'The winds blow.',
            'YYYY-08-19': 'The storms rage.',
            'YYYY-09-20': 'The quiet harvest arrives.',
            'YYYY-12-07': 'The snow falls.',
            'YYYY-12-30': 'The children play.',
            'YYY1-01-01': 'The world is hushed.',
            'YYY1-01-09': 'The world is white.',
            'YYY1-03-02': 'The snow melts.',
            'YYY1-03-14': 'The calf has grown.',
            'YYY1-03-21': 'Spring is here.'
        }
        self.lines = OrderedDict()
        next_year = str(self.base_year + 1)
        for key in lines:
            new_key = key.replace('YYYY', str(self.base_year)).replace('YYY1', next_year)
            self.lines[new_key] = lines[key]

    def setup(self):
        ''' Initial file creation. Makes sure we don't overwrite existing work.
            >>> s = Spring()
            >>> s.setup()
            ... # False, probably, if there are already these files.
            False
            '''
        try:
            self.file_get_contents('_volume')
            self.file_get_contents('_year')
        except:
            self.file_put_contents('_volume', '0')
            self.file_put_contents('_year', str(date.today().year))
            return True
        return False

    def file_put_contents(self, fn, contents):
        ''' As described.
            >>> s = Spring()
            >>> s.file_put_contents('_test', 'test')
            True
            '''
        with open(fn, 'w') as fh:
            data = fh.write(contents)
        return True

    def file_get_contents(self, fn):
        ''' As described.
            >>> s = Spring()
            >>> s.file_get_contents('_test')
            'test'
            '''
        with open(fn) as fh:
            data = fh.read()
        return data

    def the_next_year(self, tweet):
        ''' Update the volume and the volume tweet.
            >>> s = Spring()
            ... # we're not testing this because it writes actual files
            '''
        self.volume += 1
        self.file_put_contents('_volume', str(self.volume))
        self.file_put_contents('_year', str(date.today().year))
        return tweet.replace('volume X', 'volume %s' % str(self.volume))

    def check_for_tweet(self, date_str):
        ''' Check and see if we're tweeting today.
            >>> s = Spring()
            >>> d_str = '2010-07-12'
            >>> s.check_for_tweet(d_str)
            False
            '''
        for key in self.lines:
            if date_str == key:
                if 'Taro Gomi' in self.lines[key]:
                    return self.the_next_year(self.lines[key])
                return self.lines[key]
        return False

def setup_auth():
    access = {
        'token': os.getenv('ACCESS_TOKEN'),
        'secret': os.getenv('ACCESS_SECRET')
    }
    consumer = {
        'key': os.getenv('CONSUMER_KEY'),
        'secret': os.getenv('CONSUMER_SECRET')
    }
    auth = tweepy.OAuthHandler(consumer['key'], consumer['secret'])
    auth.set_access_token(access['token'], access['secret'])
    return auth

def main(args):
    auth = setup_auth()
    api = tweepy.API(auth)
    s = Spring()

    if args.initial == True:
        return s.setup()

    d_str = date.today().strftime('%Y-%m-%d')
    tweet = s.check_for_tweet(d_str)
    if tweet:
        api.update_status(tweet)
        print("WROTE TWEET %s" % tweet)
  

def build_parser(args):
    """ This method allows us to test the args.
        >>> args = build_parser(['--verbose'])
        >>> print(args.verbose)
        True
        """
    parser = argparse.ArgumentParser(usage='$ python here.py',
                                     description='Sees if we should tweet, and if we should, what.',
                                     epilog='Example use: python here.py')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    parser.add_argument("-t", "--test", dest="test", default=False, action="store_true")
    parser.add_argument("--initial", dest="initial", default=False, action="store_true")
    args = parser.parse_args(args)
    return args

if __name__ == '__main__':
    args = build_parser(sys.argv[1:])

    if args.test == True:
        doctest.testmod(verbose=args.verbose)
    main(args)
