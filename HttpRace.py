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

import threading
import socket
import ssl
import time
from pprint import pprint as p, pformat as pf
import urllib.parse as parse

import socks
from xtermcolor import colorize


def log(msg):
	print(colorize(msg, rgb=0xFFFFFF, bg=0x309200))


def ready(msg):
	print(colorize(msg, rgb=0xCCCCCC, bg=0x309200))


def warn(msg):
	print(colorize(msg, rgb=0xCCCCCC, bg=0x000000))


def debug(msg):
	print(colorize(pf(msg), rgb=0x309200, bg=0x000000))


def error(msg):
	print(colorize(pf(msg), rgb=0xFF0000, bg=0x000000))


class HttpRace:
	races = []
	laps = 1
	_proxy = None
	_debug = False

	def __init__(self, laps=1, debug=False):
		self._debug = debug
		self._laps = laps

	def proxy(self, proxy='localhost:8080'):
		# Supports SOCK5 Proxies, Format 'address:port'

		# Setup Proxy Information
		self._proxy = proxy.strip("'").split(':')

	class __Request:
		name = None
		__timeout = 5
		__CRLF = "\r\n"
		_proxy = None
		__debug = False
		__proxy = None
		__socket = None
		__promise = None
		response = None
		_method = 'GET'
		_scheme = 'http'
		_body = []
		_host = None
		_port = 80
		_uri = None
		_headers = {}

		def __init__(self, debug=False):
			self.__debug = debug
			self.__promise = self.__Promise()

		def har(self, request):

			# Parse GET/POST
			self._method = request['method']

			# Parse URL
			self.url(request['url'])

			# Parse Headers
			for header in request['headers']:
				self.header(header['name'], header['value'])

			# Parse Post Data
			if 'postData' in request:
				mime = request['postData']['mimeType']
				for data in request['postData']['params']:
					self.body(mime, data['name'], data['value'])

		def host(self, host):
			self._host = host

		def url(self, this_url):
			__parse = parse.urlparse(this_url)

			# Set Host
			self.host(__parse.netloc)

			# Set Schema / Port
			if __parse.scheme == 'https':
				self._scheme = 'https'
				self._port = 443

			# Set URI Path
			if __parse.path != '':
				self._uri = "%s" % __parse.path
			else:
				self._uri = '/'

			# Append Query to Path
			if __parse.query:
				self._uri += "?%s" % __parse.query

			return self

		def uri(self, uri):
			self._uri = uri
			return self

		def header(self, name, value):
			if name == 'Host':
				return
			self._headers[name] = value

		def body(self, mime, key, value):
			self.header('Content-Type', mime)
			self._body.append((key, value))

		def prepare_run(self, proxy=None):
			name = threading.current_thread().getName()

			log('Thread: %s, Prepare Run: %s%s:%i, @ %f' % (name, self._host, self._uri, self._port, time.perf_counter()))

			# Setup Socket
			self.__socket = socket.socket()

			# Use Proxy # TODO: Make Work with SSL Wrapper below.
			if proxy:
				self.__socket = socks.socksocket()
				self.__socket.set_proxy(socks.SOCKS5, proxy[0], int(proxy[1]))

			self.__socket.settimeout(self.__timeout)

			# p(self.__socket)

			self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

			# Bind SSL
			if self._scheme == 'https':
				self.__socket = ssl.wrap_socket(self.__socket)

			# p(self.__socket)

			# Open Connection To Server
			self.__socket.connect((self._host, self._port))

			# Send Initial Header
			self.__socket.send(
				str.encode("%s %s HTTP/1.1 %s" % (self._method, self._uri, self.__CRLF)))

			# Send Host Name
			self.__socket.send(str.encode("Host: %s %s" % (self._host, self.__CRLF)))

			# Send Headers
			for header in self._headers:
				self.__socket.send(str.encode("%s: %s %s" % (header, self._headers[header], self.__CRLF)))

			# Send GET/POST Body (If any)
			if len(self._body) > 0:
				self.__socket.send(str.encode("%s%s" % (self.__CRLF, self.__CRLF)))
				self.__socket.send(str.encode("%s%s" % (parse.urlencode(self._body), self.__CRLF)))

			# Tell HttpRace We're Ready To Execute
			self.__promise.status = True

			ready('Thread: %s, Ready! @ %f' % (name, time.perf_counter()))

		def execute_run(self):

			name = threading.current_thread().getName()

			log('Thread: %s, Executing:  %s%s:%i @ %f' % (name, self._host, self._uri, self._port, time.perf_counter()))

			if self.__debug:
				self.debug()

			# Send Termination Line Endings
			self.__socket.send(str.encode("%s%s" % (self.__CRLF, self.__CRLF)))

			# Start Receiving ... some.
			self.response = (self.__socket.recv(187))

			# Close The Socket
			self.__socket.shutdown(1)
			self.__socket.close()

			ready('Thread: %s, Executed! %f' % (name, time.perf_counter()))

		def status(self):
			return self.__promise.status

		class __Promise:
			status = False

			def __init__(self):
				pass

		# Helper Functions
		def debug(self):
			name = threading.current_thread().getName()
			debug("Debug of Thread: %s" % name)
			# import inspect as i
			# p(i.getmembers(self))
			# p(i.getmembers(self.__socket))
			# print(self.__socket._check_connected())
			debug(self.__dict__)

	def execute(self):

		n = 0
		for request in self.races:
			n += 1
			thread = threading.Thread(target=request.prepare_run, args=[self._proxy])
			thread.setName(n)
			thread.start()
			thread.join()

		ready = False
		while not ready:
			check = True
			for request in self.races:
				if not request.status:
					check = False
			if check:
				ready = True
			time.sleep(0.1)

		warn("All Threads Ready. Executing")

		n = 0
		threads = []
		start = time.perf_counter()
		for request in self.races:
			n += 1
			thread = threading.Thread(target=request.execute_run)
			thread.setName(n)
			thread.start()
			if self._debug:
				thread.join()
				time.sleep(1)
			threads.append(thread)

		for thread in threads:
			thread.join()
		end = time.perf_counter()

		log("All Threads Executed: %f" % (end - start))

	# Helper Functions
	def build_request(self):
		self.races.append(self.__Request(debug=self._debug))

		return self.races[-1]

	def har(self, har):
		ret = []

		import json

		raw = json.load(har)

		if 'log' in raw and 'entries' in raw['log']:
			for n in range(0, len(raw['log']['entries']) - 1):
				race = self.__Request(debug=self._debug)
				request = raw['log']['entries'][n]['request']  # Silly Python.
				race.har(request)
				ret.append(race)
				self.races.append(race)
		return ret


# Keep p import, Remove on release
log('HttpRace %s by %s' % (__version__, __author__))
