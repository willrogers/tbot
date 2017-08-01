import tbot
from selenium import webdriver
import time
import datetime
import parse


class Tweeter(tbot.Tweeter):

    def __init__(self, api, url, msg, opt1, opt2):
        super(Tweeter, self).__init__(api)
        self._url = url
        self._opt1 = opt1
        self._opt2 = opt2
        self._msg = msg
        self._max = 50.1
        self._max_date = datetime.date(2017, 7, 30)
        self._min = 49.9
        self._min_date = datetime.date(2017, 7, 30)
        self._last = None

    def _parse_odds(self, string):
        return float(string.split()[0].strip())

    def get_last_tweet(self):
        tweets = self._api.user_timeline(id=self._api.me().id, count=1)
        return tweets[0].text

    def parse_tweet(self, tweet):
        msg = ''.join([c for c in self._msg if c != '+'])
        p = parse.parse(msg, tweet)
        try:
            self._last = float(p[0])
            self._max = float(p[2])
            self._max_date = datetime.datetime.strptime(p[3], '%b %d %Y')
            self._min = float(p[4])
            self._min_date = datetime.datetime.strptime(p[3], '%b %d %Y')
        except Exception as e:
            print(e)
            self._last = 49.9


    def tweet(self):
        last_tweet = self.get_last_tweet()
        self.parse_tweet(last_tweet)
        driver = webdriver.PhantomJS()
        try:
            driver.get(self._url)
            # Allow plenty of time for page to load in selenium.
            time.sleep(5)
            options = driver.find_elements_by_class_name('runner-line')
            assert len(options) == 2
            for o in options:
                runner_name = o.find_element_by_class_name('runner-name')
                # element.text did not work using phantomjs
                if runner_name.get_attribute('textContent') == self._opt1:
                    runner1 = o
                if runner_name.get_attribute('textContent') == self._opt2:
                    runner2 = o
            r1text = runner1.find_element_by_class_name('last-back-cell').get_attribute('textContent')
            odds1 = self._parse_odds(r1text)
            r2text = runner2.find_element_by_class_name('first-lay-cell').get_attribute('textContent')
            odds2 = self._parse_odds(r2text)
            split = (odds1 + odds2) / 2
            pc = (1 - (1 / split)) * 100
            if pc < self._min: self._min = pc
            if pc > self._max: self._max = pc
            self._tweet(self._msg.format(pc, pc - self._last,
                                         self._max, self._max_date.strftime('%b %d %Y'),
                                         self._min, self._min_date.strftime('%b %d %Y')))
        finally:
            driver.quit()
