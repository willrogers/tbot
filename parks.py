#!/usr/bin/env python

from bs4 import BeautifulSoup
import tweepy
import urllib2
import calendar
import datetime
import os

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


# Fetch the webpage
doc = urllib2.urlopen(URL).read()
soup = BeautifulSoup(doc)

rows = [r.p.text for r in soup.find_all('td') if not r.p.text.isspace()]


current_month = None
current_day = None
current_year = None
dates = {}
current_date = None

def get_datetime(datestring):
    '''
    Some custom parsing.  Must accept:
        - 2 January 2014
        - 4 October
        - 23
    '''
    global current_month
    global current_year
    parts = datestring.split()
    day = int(parts[0])
    try:
        month = parts[1]
        if month in ['BST', 'GMT']:
            raise IndexError()
        for i, cal_month in enumerate(calendar.month_name[1:]):
            if month == cal_month:
                current_month = i + 1
                break

    except IndexError:
        month = current_month
    try:
        current_year = int(parts[2])
        year = current_year
    except (IndexError, ValueError):
        year = current_year

    return datetime.datetime(year, current_month, day)


i = 0
for row in rows:
    if i % 3 == 0:
        current_date = get_datetime(row)
    elif i % 3 == 1:
        dates[current_date] = [get_time(row)]
    elif i % 3 == 2:
        dates[current_date].append(get_time(row))
    i += 1

# Connect to Twitter.
api = load_api(config_path)


tweeted = False

for d in sorted(dates):
    if d.date() == datetime.datetime.now().date():
        datestring = d.strftime("%a, %b %d %Y")
        sunset_time = dates[d][0].strftime("%H:%M")
        close_time = dates[d][1].strftime("%H:%M")
        text = ("%s: this week the parks close at %s (sunset %s)"
                % (datestring, close_time, sunset_time))
        print("Tweeting: %s" % text)
        try:
            api.update_status(text)
            tweeted = True
            break
        except tweepy.TweepError as e:
            print("Failed to tweet: %s" % e)

if not tweeted:
    print("No tweet today.")


