import tweepy

# set up logging
import logging as log
log.basicConfig(level=log.INFO,
                format='%(asctime)s - %(message)s',
                datefmt='%d %b %Y %H:%M:%S')


ERROR_USER = 'wrgrs'


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


class Tweeter(object):

    def __init__(self, api):
        self._api = api

    def _ready_to_tweet(self):
        return True

    def _get_tweet_text(self):
        raise NotImplementedError()

    def tweet(self):
        try:
            text = self._get_tweet_text()
            if self._ready_to_tweet():
                log.info(u'Tweeting {}'.format(text))
                self._api.update_status(text)
                return True
            else:
                log.info('Not ready to tweet.')
        except Exception as e:
            error_msg = 'Failed to tweet: {}'.format(e)
            log.warn(error_msg)
            self._api.send_direct_message(user=ERROR_USER, text=error_msg)
            return False


from . import parks
from . import trump
