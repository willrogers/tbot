
from bs4 import BeautifulSoup
import tweepy
import urllib2
import calendar
import datetime

URL = "http://www.parks.ox.ac.uk/closing/"
CONFIG_FILE = "./config"


doc = urllib2.urlopen(URL).read()

soup = BeautifulSoup(doc)

rows = [r for r in soup.find_all('td') if not r.p.text.isspace()]


current_month = None
current_day = None
current_year = None
dates = {}
current_date = None

def auth_from_file(filename):
    with open(filename) as f:
        lines = f.readlines()
        lines = [l for l in lines if not l.isspace()]

    cfg = {}
    for line in lines:
        parts = line.split(':')
        cfg[parts[0].strip()] = parts[1].strip()
    return cfg

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


def get_time(timestring):
    return datetime.time(*(int(i) for i in content.split('.')))


i = 0
for r in rows:
    content = r.p.text
    if i % 3 == 0:
        current_date = get_datetime(content)
    elif i % 3 == 1:
        dates[current_date] = [get_time(content)]
    elif i % 3 == 2:
        dates[current_date].append(get_time(content))
    i += 1

cfg = auth_from_file(CONFIG_FILE)

auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
auth.set_access_token(cfg['key'], cfg['secret'])
api = tweepy.API(auth)

for d in sorted(dates):
    if d.date() == datetime.datetime.now().date():
        datestring = d.strftime("%a, %b %d %Y")
        sunset_time = dates[d][0].strftime("%H:%M")
        close_time = dates[d][1].strftime("%H:%M")
        text = "%s: this week the parks close at %s (sunset %s)" % (datestring, close_time, sunset_time)
        print "Tweeting", text
        api.update_status(text)
        break


