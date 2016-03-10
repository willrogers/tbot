#!/usr/bin/env python

from distutils.core import setup

setup(name='ParksTweets',
      version='1.0',
      author='Will Rogers',
      scripts=['parks.py'],
      install_requires=['tweepy', 'beautifulsoup4']
     )
