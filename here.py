#!/usr/bin/env python3
from datetime import date
import os, sys
import time
import random
import doctest
import argparse
import tweepy
from collections import OrderedDict
import random
import json

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
        self.base_year = int(self.file_get_contents('_year'))
        self.count = int(self.file_get_contents('_count'))
        lines = {
            'YYYY-03-22': '''Spring Is Here
  Taro Gomi
  volume X''',
            'YYYY-03-25': 'Spring is here.',
            'YYYY-04-08': 'The snow melts.',
            'YYYY-04-17': 'The earth is fresh.',
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
        # We also have a list of the lines, which allows us to have a range of dates
        # that the lines get read on.
        lines_list = [
                { 'date': ['YYYY-03-22'], 'line': '''Spring Is Here
  Taro Gomi
  volume X'''},
            { 'date': ['YYYY-03-25', 'YYYY-03-26', 'YYYY-03-27'], 'line': 'Spring is here.'},
            { 'date': ['YYYY-04-08', 'YYYY-04-09'], 'line': 'The snow melts.'},
            { 'date': ['YYYY-04-17', 'YYYY-04-19', 'YYYY-04-21'], 'line': 'The earth is fresh.'},
            { 'date': ['YYYY-05-01', 'YYYY-05-02'], 'line': 'The grass sprouts.'},
            { 'date': ['YYYY-05-21'], 'line': 'The flowers bloom.'},
            { 'date': ['YYYY-06-04'], 'line': 'The grass grows.'},
            { 'date': ['YYYY-07-12'], 'line': 'The winds blow.'},
            { 'date': ['YYYY-08-19', 'YYYY-08-25', 'YYYY-08-26', 'YYYY-08-27'], 'line': 'The storms rage.'},
            { 'date': ['YYYY-09-19', 'YYYY-09-20'], 'line': 'The quiet harvest arrives.'},
            { 'date': ['YYYY-12-07'], 'line': 'The snow falls.'},
            { 'date': ['YYYY-12-30'], 'line': 'The children play.'},
            { 'date': ['YYY1-01-01'], 'line': 'The world is hushed.'},
            { 'date': ['YYY1-01-09'], 'line': 'The world is white.'},
            { 'date': ['YYY1-03-02'], 'line': 'The snow melts.'},
            { 'date': ['YYY1-03-14'], 'line': 'The calf has grown.'},
            { 'date': ['YYY1-03-21'], 'line': 'Spring is here.'}
            ]
        self.lines = OrderedDict()
        next_year = str(self.base_year + 1)
        for i, key in enumerate(lines):
            new_key = key.replace('YYYY', str(self.base_year)).replace('YYY1', next_year)
            self.lines[new_key] = lines[key]
            for ii, d in enumerate(lines_list[i]['date']):
                lines_list[i]['date'][ii] = lines_list[i]['date'][ii].replace('YYYY', str(self.base_year)).replace('YYY1', next_year)

            if i == ( self.count + 1 ):
                self.next_line = lines_list[i]

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
            self.file_get_contents('_count')
        except:
            self.file_put_contents('_volume', '0')
            self.file_put_contents('_year', str(date.today().year))
            self.file_get_contents('_count', '0')
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

    def update_count(self):
        ''' Add one to the count value and save it in its file.
            '''
        self.count += 1
        self.file_put_contents('_count', str(self.count))
        return True

    def the_next_year(self, tweet):
        ''' Update the volume and the volume tweet.
            >>> s = Spring()
            ... # we're not testing this because it writes actual files
            '''
        self.volume = str(int(self.volume) + 1)
        self.file_put_contents('_volume', str(self.volume))
        self.file_put_contents('_year', str(date.today().year))
        self.file_put_contents('_count', '0')
        return tweet.replace('volume X', 'volume %s' % str(self.volume))

    def check_for_tweet(self, date_str):
        ''' Check and see if we're tweeting today.
            >>> s = Spring()
            >>> d_str = '2010-07-12'
            >>> s.check_for_tweet(d_str)
            False
            '''
        for i, key in enumerate(self.lines):
            # This logic lets us mix up the dates a little bit.
            # One of the line dictionaries looks like this, for reference
            # { 'date': ['YYYY-04-17', 'YYYY-04-19', 'YYYY-04-21'], 'line': 'The earth is fresh.'},
            l = len(self.next_line['date'])
            for ii, d in enumerate(self.next_line['date']):
                if self.next_line['date'][ii] == date_str:

                    # If we're on the new year.
                    if 'Taro Gomi' in self.next_line['line']:
                        return self.the_next_year(self.lines[key])

                    # If we've passed on the previous items and we're on
                    # the last one, we've gotta tweet it.
                    if l == (ii + 1):
                        return self.next_line['line']
                    
                    # If it's not the last item in the list then we
                    # roll the dice to see if we should send tweet.
                    if random.randint(0, l) == 0:
                        return self.next_line['line']

            #if date_str == key:
            #    if 'Taro Gomi' in self.lines[key]:
            #        return self.the_next_year(self.lines[key])
            #    return self.lines[key]
        return False

def setup_auth():
    ''' Get the env vars and create and return an object
        that can be handed off to the tweepy API to 
        gain access to the twitter user's account.
        >>> auth = setup_auth()
        >>> print(auth.username)
        None
        '''
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
        print("ABOUT TO WRITE TWEET %s" % tweet)
        api.update_status(tweet)
        s.update_count()
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
