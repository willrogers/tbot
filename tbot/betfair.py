import tbot
from selenium import webdriver
import time
import datetime
import parse
import logging as log


class Tweeter(tbot.Tweeter):

    def __init__(self, api, url, msg, opt):
        super(Tweeter, self).__init__(api)
        self._url = url
        self._opt = opt
        self._msg = msg
        self._max = None
        self._max_date = None
        self._min = None
        self._min_date = None
        self._last = None

    def _odds_from_cell(self, runner_element, class_name):
        cell = runner_element.find_element_by_class_name(class_name)
        cell_text = cell.get_attribute('textContent')
        return float(cell_text.split()[0].strip())

    def get_last_tweet(self):
        tweets = self._api.user_timeline(id=self._api.me().id, count=1)
        return tweets[0].text

    def parse_tweet(self, tweet):
        msg = ''.join([c for c in self._msg if c != '+'])
        p = parse.parse(msg, tweet)
        self._last = float(p[0])
        self._max = float(p[2])
        self._max_date = datetime.datetime.strptime(p[3], '%b %d %Y').date()
        self._min = float(p[4])
        self._min_date = datetime.datetime.strptime(p[5], '%b %d %Y').date()

    def _ready_to_tweet(self):
        diff = abs(self.pc - self._last)
        log.info('Difference to last time is {:.1f}%'.format(diff))
        return diff > 0.3

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
                if runner_name.get_attribute('textContent') == self._opt:
                    runner = o
            # Find centre between back and lay odds for the selected option.
            back_odds = self._odds_from_cell(runner, 'last-back-cell')
            lay_odds = self._odds_from_cell(runner, 'first-lay-cell')
            midpoint = (back_odds + lay_odds) / 2
            self.pc = (1 / midpoint) * 100
            if self.pc < self._min:
                self._min = self.pc
                self._min_date = datetime.datetime.now().date()
            if self.pc > self._max:
                self._max = self.pc
                self._max_date = datetime.datetime.now().date()
            if self._ready_to_tweet():
                msg = self._msg.format(self.pc,
                                       self.pc - self._last,
                                       self._max,
                                       self._max_date.strftime('%b %d %Y'),
                                       self._min,
                                       self._min_date.strftime('%b %d %Y'))
                self._tweet(msg)
        finally:
            driver.quit()
