__author__ = 'Andy Hawkins'
__email__ = 'andy@a904guy.com'
__company__ = '''
  _______   ___ __ __    _______   ______   ______    ______
/_______/\ /__//_//_/\ /_______/\ /_____/\ /_____/\  /_____/\
\::: _  \ \\::\| \| \ \\::: _  \ \\::::_\/_\:::_ \ \ \:::_ \ \
 \::(_)  \/_\:.      \ \\::(_)  \/_\:\/___/\\:\ \ \ \_\:\ \ \ \
  \::  _  \ \\:.\-/\  \ \\::  _  \ \\_::._\:\\:\ \ /_ \\:\ \ \ \
   \::(_)  \ \\. \  \  \ \\::(_)  \ \ /____\:\\:\_-  \ \\:\/.:| |
    \_______\/ \__\/ \__\/ \_______\/ \_____\/ \___|\_\_/\____/_/
'''

import threading
import urlparse
import socket
import time


class HttpRace:

    races = []
    laps = 1

    def __init__(self):
        pass

    def build_request(self):

        class Request:

            __timeout = 100
            __CRLF = "\r\n\r\n"
            __socket = None
            __promise = None
            response = None
            _method = 'GET'
            _scheme = 'http'
            _host = None
            _port = 80
            _uri = None
            _headers = {}

            def __init__(self, promise):
                self.__promise = promise
                pass

            def host(self, host):
                self._host = host

            def url(self, this_url):
                parse = urlparse.urlparse(this_url)
                self._host = parse.netloc
                self._uri = parse.path + parse.params
                return self

            def uri(self, uri):
                self._uri = uri
                return self

            def prepare_run(self):
                self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__socket.settimeout(self.__timeout)
                self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.__socket.connect((self._host, self._port))
                self.__socket.send("%s %s HTTP/1.0" % (self._method, self._uri))
                self.__socket.send("Host: %s" % self._host)
                for context, data in enumerate(self._headers):
                    self.__socket.send("%s: %s" % (context, data))
                self.__promise.status = True

            def execute_run(self):
                self.__socket.send("%s" % self.__CRLF)
                self.response = (self.__socket.recv(100000000))
                self.__socket.shutdown(1)
                self.__socket.close()

            def status(self):
                return self.__promise.status

        class Promise:
            status = False

            def __init__(self):
                pass

        self.races.append(Request(Promise()))

        return self.races[-1]

    def execute(self):

        for request in self.races:
            threading.Thread(target=request.prepare_run).start()

        ready = False
        while not ready:
            check = True
            for request in self.races:
                if not request.status:
                    check = False
            if check:
                ready = True
            time.sleep(0.1)

        for request in self.races:
            threading.Thread(target=request.execute_run).start()
