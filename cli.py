#!/usr/bin/env python3
__project__ = 'HttpRace'
__author__ = 'Andy Hawkins'
__email__ = 'andy@a940guy.com'
__date__ = '6/21/15 10:54 AM'
__company__ = '''
      ___ ___ ___
  ___| . |   | | |___ _ _ _ _
 | .'|_  | | |_  | . | | | | |
 |__,|___|___| |_|_  |___|_  |
                 |___|   |___|
ANDY@A904GUY.COM - A904GUY.COM
'''
__website__ = "http://a904guy.com/"
__version__ = "0.0.1"
__license__ = "CC-BY-SA"
__maintainer__ = __author__
__contact__ = __email__

import argparse

import HttpRace

parser = argparse.ArgumentParser(description="HttpRace, HTTP Race Condition Tool")
harGroup = parser.add_argument_group('HAR', 'Import HAR file(s) to rune')
harGroup.add_argument('--har', '-ha', help='Specify HAR File(s)', type=argparse.FileType(), action='append')
defaultGroup = parser.add_argument_group('CLI', 'Construct Request From CLI')
defaultGroup.add_argument('--url', '-u', help='Complete URL', action='append')
parser.add_argument('--proxy', '-py', help='Use this proxy. (http://localhost:7777)')

args = parser.parse_args()
race = HttpRace.HttpRace()

if args.proxy:
	race.proxy(args.proxy)

if args.har is not None and len(args.har) > 0:
	for file in args.har:
		race.har(file)
if args.url is not None and len(args.url) > 0:
	for url in args.url:
		request = race.build_request()
		request.url(url)

if len(race.races) > 0:
	race.execute()
