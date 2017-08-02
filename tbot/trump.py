from . import betfair
import datetime


URL = 'https://www.betfair.com/exchange/plus/politics/market/1.129133401'
MSG = u'''Odds of Trump surviving his 4-year term: {:.1f}% ({:+.1f}%)

High {:.1f}%: {}

Low {:.1f}%: {}'''

YES = "Yes"
NO = "No"


class Tweeter(betfair.Tweeter):

    def __init__(self, api):
        super(Tweeter, self).__init__(api, URL, MSG, YES)
        self._max = 50.2
        self._max_date = datetime.date(2017, 8, 2)
        self._min = 49.9
        self._min_date = datetime.date(2017, 7, 30)
