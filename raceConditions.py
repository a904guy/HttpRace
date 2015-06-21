import HttpRace

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

race = HttpRace.HttpRace()

for n in xrange(0, 5):
    request = race.build_request()
    request.url('http://localhost/precisionCheck')

race.execute()

for request in race.races:
    print(request.response)

# millisecond    exec  isoTime
# 1433177761.574 0.100 2015-06-01T09:56:01-07:00 400
# 1433177761.574 0.100 2015-06-01T09:56:01-07:00 400
# 1433177761.575 0.101 2015-06-01T09:56:01-07:00 400
# 1433177761.575 0.101 2015-06-01T09:56:01-07:00 400
# 1433177761.575 0.101 2015-06-01T09:56:01-07:00 400
