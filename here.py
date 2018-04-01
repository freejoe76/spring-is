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

    def __init__(self):
        self.volume = self.file_get_contents('_volume')
        self.base_year = 2018 + int(self.volume)
        lines = {
            'YYYY-03-22': '''Spring Is Here
  Taro Gomi''',
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
        next_year = self.base_year + 1
        for key in lines:
            new_key = key.replace('YYYY', str(self.base_year)).replace('YYY1', str(next_year))
            self.lines[new_key] = lines[key]

    def file_get_contents(self, fn):
        ''' As described.
            '''
        with open(fn) as fh:
            data = fh.read()
        return data

    def file_put_contents(self, fn, contents):
        ''' As described.
            '''
        with open(fn, 'w') as fh:
            data = fh.write(contents)
        return True

    def check_volume(self):
        ''' Check the current volume for whether we've tweeted a particular twet.
            '''
        pass

def main(args):
    """ 
        """
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
    api = tweepy.API(auth)
    #api.update_status('Spring is here.')
    s = Spring()
    s.file_put_contents('_volume', '0')
    t = date.today()
    y = t.year
    d_str = t.strftime('%Y-%m-%d')
    
    #print(s.lines)
    #print(dir(api))
    #'add_list_member', 'add_list_members', 'api_root', 'auth', 'blocks', 'blocks_ids', 'cache', 'compression', 'configuration', 'create_block', 'create_favorite', 'create_friendship', 'create_list', 'create_saved_search', 'destroy_block', 'destroy_direct_message', 'destroy_favorite', 'destroy_friendship', 'destroy_list', 'destroy_saved_search', 'destroy_status', 'direct_messages', 'favorites', 'followers', 'followers_ids', 'friends', 'friends_ids', 'friendships_incoming', 'friendships_outgoing', 'geo_id', 'geo_search', 'geo_similar_places', 'get_direct_message', 'get_list', 'get_oembed', 'get_saved_search', 'get_settings', 'get_status', 'get_user', 'home_timeline', 'host', 'list_members', 'list_subscribers', 'list_timeline', 'lists_all', 'lists_memberships', 'lists_subscriptions', 'lookup_friendships', 'lookup_users', 'me', 'media_upload', 'mentions_timeline', 'parser', 'proxy', 'rate_limit_status', 'related_results', 'remove_list_member', 'remove_list_members', 'report_spam', 'retry_count', 'retry_delay', 'retry_errors', 'retweet', 'retweeters', 'retweets', 'retweets_of_me', 'reverse_geocode', 'saved_searches', 'search', 'search_host', 'search_root', 'search_users', 'send_direct_message', 'sent_direct_messages', 'set_delivery_device', 'set_settings', 'show_friendship', 'show_list_member', 'show_list_subscriber', 'statuses_lookup', 'subscribe_list', 'suggested_categories', 'suggested_users', 'suggested_users_tweets', 'supported_languages', 'timeout', 'trends_available', 'trends_closest', 'trends_place', 'unretweet', 'unsubscribe_list', 'update_list', 'update_profile', 'update_profile_background_image', 'update_profile_banner', 'update_profile_image', 'update_status', 'update_with_media', 'upload_host', 'upload_root', 'user_timeline', 'verify_credentials', 'wait_on_rate_limit', 'wait_on_rate_limit_notify'
    
  

def build_parser(args):
    """ This method allows us to test the args.
        >>> args = build_parser(['--verbose'])
        >>> print args.verbose
        True
        """
    parser = argparse.ArgumentParser(usage='$ python project.py',
                                     description='What this file does.',
                                     epilog='Example use: python project.py')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    args = parser.parse_args(args)
    return args

if __name__ == '__main__':
    args = build_parser(sys.argv[1:])

    if args.verbose == True:
        doctest.testmod(verbose=args.verbose)
    main(args)
