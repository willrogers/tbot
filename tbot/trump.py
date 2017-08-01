from . import betfair


URL = 'https://www.betfair.com/exchange/plus/politics/market/1.129133401'
MSG = u'''Odds of Trump surviving his 4-year term: {:.1f}% ({:+.1f}%)

High {:.1f}%: {}

Low {:.1f}%: {}'''

YES = "Yes"
NO = "No"


class Tweeter(betfair.Tweeter):

    def __init__(self, api):
        super(Tweeter, self).__init__(api, URL, MSG, YES, NO)
