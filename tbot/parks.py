import tbot
from bs4 import BeautifulSoup
import urllib2
import calendar
import datetime
import logging as log


URL = 'http://www.parks.ox.ac.uk/closing/'


def get_time(timestring):
    formats = ['%H:%M', '%H.%M']
    t = None
    for f in formats:
        try:
            t = datetime.datetime.strptime(timestring, f).time()
            break
        except ValueError:
            continue
    return t


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

    print(year, month, day)
    return datetime.datetime(year, month, day)


def parse_rows(rows):
    dates = {}
    current_date = None
    current_month = None
    current_year = datetime.datetime.now().year

    for i, row in enumerate(rows):
        try:
            print('\n{}'.format(row))
            cells = [cell.p.text.strip() for cell in row.find_all('td')]
            if not len(cells) == 4:
                print('invalid row {}'.format(row))
                continue
            current_date = get_datetime(cells[0], current_month, current_year)
            current_year = current_date.year
            current_month = current_date.month
            dates[current_date] = [get_time(cells[1])]
            dates[current_date].append(get_time(cells[2]))
        except (ValueError, IndexError, AttributeError):
            # Skip any rows that aren't understood.
            continue

    return dates


class Tweeter(tbot.Tweeter):

    def tweet_update(self, dates):
        for d in sorted(dates):
            if d.date() == datetime.datetime.now().date():
                datestring = d.strftime('%a, %b %d %Y')
                sunset_time = dates[d][0].strftime('%H:%M')
                close_time = dates[d][1].strftime('%H:%M')
                text = ('%s: this week the parks close at %s (sunset %s)'
                        % (datestring, close_time, sunset_time))
                log.info('Tweeting: %s', text)
                return self._tweet(text)

    def tweet(self):
        # Fetch the webpage
        doc = urllib2.urlopen(URL).read()
        # Remove any non-breaking spaces.
        doc = doc.replace("\xc2\xa0", " ")
        soup = BeautifulSoup(doc)
        rows = soup.find_all('tr')

        # Parse the rows
        dates = parse_rows(rows)

        if not self.tweet_update(dates):
            log.info('No tweet today.')
