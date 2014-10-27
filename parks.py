#!/usr/bin/env python

from bs4 import BeautifulSoup
import tweepy
import urllib2
import calendar
import datetime
import os

# set up logging
import logging as log
log.basicConfig(level=log.INFO,
                format='%(asctime)s - %(message)s',
                datefmt='%d %b %Y %H:%M:%S')

URL = "http://www.parks.ox.ac.uk/closing/"
CONFIG_FILE = "config"


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


def get_time(timestring):
    return datetime.time(*(int(i) for i in timestring.split('.')))


def get_datetime(datestring, last_month, last_year):
    '''
    Some custom parsing of table contents.  Must accept:
        - 2 January 2014
        - 4 October
        - 23
        - 22 GMT Begins
        - 15 BST Begins
    If incomplete information, assume that last_month and / or
    last_year still apply.
    '''
    parts = datestring.split()
    day = int(parts[0])
    if len(parts) > 1 and parts[1] in calendar.month_name:
        mstring = parts[1]
        for i, cal_month in enumerate(calendar.month_name[1:]):
            if mstring == cal_month:
                month = i + 1
                break
    else:
        month = last_month
    try:
        year = int(parts[2])
    except (IndexError, ValueError):
        year = last_year

    return datetime.datetime(year, month, day)


def parse_rows(rows):
    dates = {}
    current_date = None
    current_month = None
    current_day = None
    current_year = None

    for i, row in enumerate(rows):
        if i % 3 == 0:
            current_date = get_datetime(row, current_month, current_year)
            current_year = current_date.year
            current_month = current_date.month
            current_day = current_date.day
        elif i % 3 == 1:
            dates[current_date] = [get_time(row)]
        elif i % 3 == 2:
            dates[current_date].append(get_time(row))

    return dates


def tweet(api, text):
    try:
        api.update_status(text)
        return True
    except tweepy.TweepError as e:
        log.warn("Failed to tweet: %s" % e)
        return False


def tweet_update(api, dates):
    for d in sorted(dates):
        if d.date() == datetime.datetime.now().date():
            datestring = d.strftime("%a, %b %d %Y")
            sunset_time = dates[d][0].strftime("%H:%M")
            close_time = dates[d][1].strftime("%H:%M")
            text = ("%s: this week the parks close at %s (sunset %s)"
                    % (datestring, close_time, sunset_time))
            log.info("Tweeting: %s", text)
            return tweet(api, text)


if __name__ == '__main__':
    # Connect to Twitter.
    api = load_api(config_path)

    # Fetch the webpage
    doc = urllib2.urlopen(URL).read()
    soup = BeautifulSoup(doc)
    rows = [r.p.text for r in soup.find_all('td') if not r.p.text.isspace()]

    # Parse the rows
    dates = parse_rows(rows)

    if not tweet_update(api, dates):
        log.info("No tweet today.")


