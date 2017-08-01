import tbot
import os
import sys

try:
    name = sys.argv[1]
except IndexError:
    print('Usage: python go.py <name>')
    sys.exit()

config_file = 'config-' + name

# Fetch config from same directory as script.
script_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(script_dir, config_file)



# Connect to Twitter.
api = tbot.load_api(config_path)

module = getattr(tbot, name)
tweeter = module.Tweeter(api)

tweeter.tweet()
