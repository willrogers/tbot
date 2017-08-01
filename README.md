tbot
====

Some Twitter bots using Python and Tweepy.  I'm @wrgrs.


parkstweets
-----------

The Oxford University Parks close at different times throughout the year.

This script fishes the times from the webpage at http://www.parks.ox.ac.uk/closing/index.htm and tweets the closing times for the week.

I'm using the account @oxparksclosing.


Dump Trump
----------

Tweets the odds of Donald Trump surviving his first four term, from https://www.betfair.com/exchange/plus/politics/market/1.129133401.

I'm using the account @trumpdumpodds.


### Installing on a Raspberry Pi

Prerequisites:

* `sudo apt install python-pip`
* `sudo apt install fontconfig`
* `sudo apt install libjpeg8`
* `sudo pip install --upgrade pip`
* `sudo pip install virtualenv`
* A config file containing the appropriate keys and secrets, named config-trump

Installation:

* `wget https://raw.githubusercontent.com/willrogers/tbot/master/install-pi-trump.sh && bash install-pi-trump.sh`
