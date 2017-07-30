import tbot
from selenium import webdriver
import time
import parse


class Tweeter(tbot.Tweeter):

    def __init__(self, api, url, msg, opt1, opt2):
        super(Tweeter, self).__init__(api)
        self._url = url
        self._opt1 = opt1
        self._opt2 = opt2
        self._msg = msg

    def _parse_odds(self, string):
        return float(string.split()[0].strip())

    def get_last_tweet(self):
        tweets = self._api.user_timeline(id=self._api.me().id, count=1)
        return tweets[0].text

    def parse_tweet(self, tweet):
        p = parse.parse(self._msg, tweet)
        return float(p[0])

    def tweet(self):
        last_tweet = self.get_last_tweet()
        last = self.parse_tweet(last_tweet)
        driver = webdriver.PhantomJS()
        try:
            driver.get(self._url)
            time.sleep(2)
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
            self._tweet(self._msg.format(pc, pc - last))
        finally:
            driver.quit()
