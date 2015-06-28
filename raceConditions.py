__project__ = 'HttpRace'
__author__ = 'Andy Hawkins'
__email__ = 'andy@a940guy.com'
__date__ = '6/21/15 10:54 AM'
__website__ = "http://a904guy.com/"
__version__ = "0.0.1"
__license__ = "CC-BY-SA"
__maintainer__ = __author__
__contact__ = __email__

import HttpRace

race = HttpRace.HttpRace()

for n in range(0, 5):
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
