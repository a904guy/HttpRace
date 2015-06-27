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

import threading
import socket
import ssl
import time
from pprint import pprint as p
import urllib.parse as parse

import socks


class HttpRace:
	races = []
	laps = 1
	_proxy = None

	def __init__(self):
		pass

	def proxy(self, proxy='localhost:8080'):
		# Supports SOCK5 Proxies, Format 'address:port'

		# Setup Proxy Information
		self._proxy = proxy.strip("'").split(':')

	class __Request:
		name = None
		__timeout = 5
		__CRLF = "\r\n"
		_proxy = None
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

		def __init__(self):
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
			# p(__parse);
			self.host(__parse.netloc)
			if __parse.scheme == 'https':
				self._scheme = 'https'
				self._port = 443
			self._uri = "%s" % __parse.path
			if __parse.query:
				self._uri += "?%s" % __parse.query

			return self

		def uri(self, uri):
			self._uri = uri
			return self

		def header(self, name, value):
			self._headers[name] = value

		def body(self, mime, key, value):
			self.header('Content-Type', mime)
			self._body.append((key, value))

		def prepare_run(self, proxy=None):
			name = threading.current_thread().getName()

			print('Thread: %s, Prepare Run: %s%s:%i, @ %f' % (
				name, self._host, self._uri, self._port, time.perf_counter()))

			# Setup Socket
			self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			# Use Proxy
			if proxy:
				self.__socket = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
				self.__socket.set_proxy(socks.SOCKS5, proxy[0], int(proxy[1]))

			self.__socket.settimeout(self.__timeout)

			self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

			# Bind SSL
			if self._scheme == 'https':
				self.__socket = ssl.wrap_socket(self.__socket)

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

			print('Thread: %s, Ready! @ %f' % (name, time.perf_counter()))

		def execute_run(self):

			name = threading.current_thread().getName()

			print('Thread: %s, Executing:  %s%s:%i @ %f' % (name, self._host, self._uri, self._port, time.perf_counter()))

			# Send Termination Line Endings
			self.__socket.send(str.encode("%s%s" % (self.__CRLF, self.__CRLF)))

			# Start Receiving ... some.
			self.response = (self.__socket.recv(1))

			# Close The Socket
			self.__socket.shutdown(1)
			self.__socket.close()

			print('Thread: %s, Executed! %f' % (name, time.perf_counter()))

		def status(self):
			return self.__promise.status

		class __Promise:
			status = False

			def __init__(self):
				pass

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

		n = 0
		threads = []
		start = time.perf_counter()
		for request in self.races:
			n += 1
			thread = threading.Thread(target=request.execute_run)
			thread.setName(n)
			thread.start()
			threads.append(thread)
		for thread in threads:
			thread.join()
		end = time.perf_counter()

		print("All Threads Executed: %f" % (end - start))

	# Helper Functions
	def build_request(self):
		self.races.append(self.__Request())

		return self.races[-1]

	def har(self, har):

		ret = []

		import json

		raw = json.load(har)

		if 'log' in raw and 'entries' in raw['log']:
			for n in range(0, len(raw['log']['entries'])):
				race = self.__Request()
				race.har(raw['log']['entries'][n]['request'])
				p(race.__dict__)
				ret.append(race)
				self.races.append(race)

		return ret


# Keep p import, Remove on release
p('HttpRace %s by %s' % (__version__, __author__))
