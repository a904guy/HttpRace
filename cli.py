#!/usr/bin/env python3
__author__ = 'Andy Hawkins'
__email__ = 'andy@bmbsqd.com'
__date__ = '6/21/15 10:54 AM'
__company__ = '''
  _______   ___ __ __    _______   ______   ______    ______
/_______/\ /__//_//_/\ /_______/\ /_____/\ /_____/\  /_____/\
\::: _  \ \\::\| \| \ \\::: _  \ \\::::_\/_\:::_ \ \ \:::_ \ \
 \::(_)  \/_\:.      \ \\::(_)  \/_\:\/___/\\:\ \ \ \_\:\ \ \ \
  \::  _  \ \\:.\-/\  \ \\::  _  \ \\_::._\:\\:\ \ /_ \\:\ \ \ \
   \::(_)  \ \\. \  \  \ \\::(_)  \ \ /____\:\\:\_-  \ \\:\/.:| |
    \_______\/ \__\/ \__\/ \_______\/ \_____\/ \___|\_\_/\____/_/
    ANDY@BMBSQD.COM   -  WWW.BMBSQD.COM
'''
__website__ = "http://bmbsqd.com/"
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
