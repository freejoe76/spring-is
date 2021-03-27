#!/usr/bin/env python3
# Example use:
# python3 here.py --story spring-is
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
from pdb import set_trace

class Spring:
    ''' A class for managing a set of tweets that are supposed to be tweeted on
        specific days, year after year.
        '''

    def __init__(self, story):
        ''' Make a new Spring object.
            >>> s = Spring('test')
            >>> print(s.lines_list[0]['date'])
            ['2020-03-22']
            '''
        try:
            self.volume = self.file_get_contents('_volume')
        except:
            self.setup()
            return None
        self.base_year = int(self.file_get_contents('_year'))
        self.count = int(self.file_get_contents('_count'))
        with open('story/%s.json' % story) as fh:
            self.lines_list = json.load(fh)

        # Loop through the lines. We store the next line we have to publish
        # in a var called next_line, this var is crucial in the publishing logic.
        next_year = str(self.base_year + 1)
        # Go through the items in the json
        for i, item in enumerate(self.lines_list):
            # For each item in the json, go through the date(s) in the record
            # Example:
            # { "date": ["YYYY-03-28", "YYYY-03-30", "YYYY-03-31"], "line": "Spring is here."},
            for ii, d in enumerate(self.lines_list[i]['date']):
                self.lines_list[i]['date'][ii] = self.lines_list[i]['date'][ii].replace('YYYY', str(self.base_year)).replace('YYY1', next_year)

            if i == ( self.count + 1 ):
                self.next_line = self.lines_list[i]
                if args.verbose == True:
                    print("UP NEXT: ", i, self.next_line)

        # If we've made it through all the items in the json and
        # still haven't set the self.next_line var, that means
        # we're on the last line and are starting over again.
        if not hasattr(self, 'next_line'):
            # If this is what we're doing, the year on the first record will be last year.
            # That means, if we're going to have a date match that we need to swap out the
            # previous year for the current year.
            for ii, d in enumerate(self.lines_list[0]['date']):
                self.lines_list[0]['date'][ii] = self.lines_list[0]['date'][ii].replace(str(self.base_year), next_year)
            self.next_line = self.lines_list[0]


    def setup(self):
        ''' Initial file creation. Makes sure we don't overwrite existing work.
            >>> s = Spring('test')
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
            self.file_put_contents('_count', '0')
            self.file_put_contents('_test', 'test')
            return True
        return False

    def file_put_contents(self, fn, contents):
        ''' As described.
            >>> s = Spring('test')
            >>> s.file_put_contents('_test', 'test')
            True
            '''
        with open(fn, 'w') as fh:
            data = fh.write(contents)
        return True

    def file_get_contents(self, fn):
        ''' As described.
            >>> s = Spring('test')
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
            >>> s = Spring('test')
            ... # we're not testing this because it writes actual files
            '''
        self.volume = str(int(self.volume) + 1)
        self.file_put_contents('_volume', str(self.volume))
        self.file_put_contents('_year', str(date.today().year))
        self.count = 0
        self.file_put_contents('_count', '0')
        return tweet.replace('volume X', 'volume %s' % str(self.volume))

    def check_for_tweet(self, date_str):
        ''' Check and see if we're tweeting today.
            >>> s = Spring('test')
            >>> d_str = '2010-07-12'
            >>> s.check_for_tweet(d_str)
            False
            '''
        for i, item in enumerate(self.lines_list):
            # This logic lets us mix up the dates a little bit.
            # One of the line dictionaries looks like this, for reference
            # { 'date': ['YYYY-04-17', 'YYYY-04-19', 'YYYY-04-21'], 'line': 'The earth is fresh.'},
            l = len(self.next_line['date'])
            for ii, d in enumerate(self.next_line['date']):
                if self.next_line['date'][ii] == date_str:

                    # If we're on the new year.
                    # We're assuming the string "\nvolume" is in the first tweet
                    # of every year.
                    if '\nvolume' in self.next_line['line']:
                        return self.the_next_year(self.lines_list[i]['line'])

                    # If we've passed on the previous items and we're on
                    # the last one, we've gotta tweet it.
                    if l == (ii + 1):
                        return self.next_line['line']
                    
                    # If it's not the last item in the list then we
                    # roll the dice to see if we should send tweet.
                    if random.randint(0, l) == 0:
                        return self.next_line['line']

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
    s = Spring(args.story)
    s.args = args

    if args.initial == True:
        return s.setup()

    if args.verbose == True:
        print(args)

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
    parser.add_argument("--initial", dest="initial", default=False, action="store_true")
    parser.add_argument("-s", "--story", dest="story", default=None)
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    parser.add_argument("-t", "--test", dest="test", default=False, action="store_true")
    args = parser.parse_args(args)
    return args

if __name__ == '__main__':
    args = build_parser(sys.argv[1:])

    if args.test == True:
        doctest.testmod(verbose=args.verbose)
    main(args)
