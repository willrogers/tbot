import tweepy
import os

# set up logging
import logging as log
log.basicConfig(level=log.INFO,
                format='%(asctime)s - %(message)s',
                datefmt='%d %b %Y %H:%M:%S')
CONFIG_FILE = 'config'

# Fetch config from same directory as script.
script_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(script_dir, CONFIG_FILE)


def load_api(config_file):
    with open(config_file) as f:
        lines = [l for l in f.readlines() if not l.isspace()]

    cfg = {}
    for line in lines:
        parts = line.split(':')
        cfg[parts[0].strip()] = parts[1].strip()
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['key'], cfg['secret'])
    api = tweepy.API(auth)
    return api


def tweet(api, text):
    try:
        api.update_status(text)
        return True
    except tweepy.TweepError as e:
        log.warn('Failed to tweet: %s' % e)
        return False
