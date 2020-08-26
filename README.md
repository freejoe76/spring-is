# Spring Is Here bot

For tweeting out something every so often for as long as your server lasts.

## Usage

### How to set up a dev environment

Install python 3.

1. To create a virtual environment using python3, run something like `python3 -m venv SPRING`.
1. cd to the project root
1. `pip3 install -r requirements.txt`

If you don't have python 3 set up:

1. `brew install python3`

Once you're there, you'll need to hook up twitter to this. With the twitter account you intend to use this on:

1. Go to https://developer.twitter.com/en/apps
1. Create a new app
1. Click the Keys and Access Tokens tab, create an Access Token.
1. Get that access token and its secret, as well as the consumer key and secret.
1. Take those variables listed above and make them available to your environment, maybe like this:
```bash
export ACCESS_TOKEN='blah-blah'
export ACCESS_SECRET='blah'
export CONSUMER_KEY='blah'
export CONSUMER_SECRET='blah'
```

And once you've done that you'll need to run the initial setup: `python here.py --initial`. This creates the text files and puts the defaults in them.

## How to run the script

Once a day, run `python3 here.py`

[comment]: <> ('add_list_member', 'add_list_members', 'api_root', 'auth', 'blocks', 'blocks_ids', 'cache', 'compression', 'configuration', 'create_block', 'create_favorite', 'create_friendship', 'create_list', 'create_saved_search', 'destroy_block', 'destroy_direct_message', 'destroy_favorite', 'destroy_friendship', 'destroy_list', 'destroy_saved_search', 'destroy_status', 'direct_messages', 'favorites', 'followers', 'followers_ids', 'friends', 'friends_ids', 'friendships_incoming', 'friendships_outgoing', 'geo_id', 'geo_search', 'geo_similar_places', 'get_direct_message', 'get_list', 'get_oembed', 'get_saved_search', 'get_settings', 'get_status', 'get_user', 'home_timeline', 'host', 'list_members', 'list_subscribers', 'list_timeline', 'lists_all', 'lists_memberships', 'lists_subscriptions', 'lookup_friendships', 'lookup_users', 'me', 'media_upload', 'mentions_timeline', 'parser', 'proxy', 'rate_limit_status', 'related_results', 'remove_list_member', 'remove_list_members', 'report_spam', 'retry_count', 'retry_delay', 'retry_errors', 'retweet', 'retweeters', 'retweets', 'retweets_of_me', 'reverse_geocode', 'saved_searches', 'search', 'search_host', 'search_root', 'search_users', 'send_direct_message', 'sent_direct_messages', 'set_delivery_device', 'set_settings', 'show_friendship', 'show_list_member', 'show_list_subscriber', 'statuses_lookup', 'subscribe_list', 'suggested_categories', 'suggested_users', 'suggested_users_tweets', 'supported_languages', 'timeout', 'trends_available', 'trends_closest', 'trends_place', 'unretweet', 'unsubscribe_list', 'update_list', 'update_profile', 'update_profile_background_image', 'update_profile_banner', 'update_profile_image', 'update_status', 'update_with_media', 'upload_host', 'upload_root', 'user_timeline', 'verify_credentials', 'wait_on_rate_limit', 'wait_on_rate_limit_notify')

