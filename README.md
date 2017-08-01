parkstweets
===========

The Oxford University Parks close at different times throughout the year.

This script fishes the times from the webpage at http://www.parks.ox.ac.uk/closing/index.htm and tweets the closing times for the week.

I'm using the account @oxparksclosing, and I'm @wrgrs.


Installing on a Raspberry Pi
============================

Prerequisites:

* `sudo apt install python-pip`
* `sudo apt install fontconfig`
* `sudo apt install libjpeg8`
* `sudo pip install --upgrade pip`
* `sudo pip install virtualenv`
* A config file containing the appropriate keys and secrets, named config-trump

Installation:

* `wget https://raw.githubusercontent.com/willrogers/parkstweets/refactor/install-pi.sh && bash install-pi.sh`
