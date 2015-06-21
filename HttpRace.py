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
import time

from pprint import pprint as p
import urllib.parse as parse


class HttpRace:
    races = []
    laps = 1

    def __init__(self):
        pass

    class __Request:
        name = None
        __timeout = 100
        __CRLF = u"\r\n\r\n"
        __socket = None
        __promise = None
        response = None
        _method = 'GET'
        _scheme = 'http'
        _host = None
        _port = 80
        _uri = None
        _headers = {}

        def __init__(self):
            self.__promise = self.__Promise()
            pass

        def har(self, harparse, page):
            # TODO: Finish Implement
            pass

        def host(self, host):
            self._host = host

        def url(self, this_url):
            __parse = parse.urlparse(this_url)
            self._host = __parse.netloc
            if __parse.scheme == 'https':
                self._scheme = 'https'
                self._port = 443
            self._uri = str(parse.urljoin(__parse.netloc, __parse.path))
            return self

        def uri(self, uri):
            self._uri = uri
            return self

        def prepare_run(self):
            # TODO: Implement HTTPS

            print('Thread: %i, Prepare Run: %s, @ %f' % (threading.get_ident(), self._uri, time.perf_counter()))

            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.settimeout(self.__timeout)
            self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.__socket.connect((self._host, self._port))
            self.__socket.send(str.encode("%s %s HTTP/1.0" % (self._method, self._uri)))
            self.__socket.send(str.encode("Host: %s" % self._host))
            for context, data in enumerate(self._headers):
                self.__socket.send(str.encode("%s: %s" % (context, data)))
            self.__promise.status = True

            print('Thread: %i, Ready! @ %f' % (threading.get_ident(), time.perf_counter()))

        def execute_run(self):

            print('Thread: %i, Executing: %s @ %f' % (threading.get_ident(), self._uri, time.perf_counter()))

            self.__socket.send(str.encode("%s" % self.__CRLF))
            self.response = (self.__socket.recv(100000000))
            self.__socket.shutdown(1)
            self.__socket.close()

            print('Thread: %i, Executed! %f' % (threading.get_ident(), time.perf_counter()))

        def status(self):
            return self.__promise.status

        class __Promise:
            status = False

            def __init__(self):
                pass

    def execute(self):
        for request in self.races:
            thread = threading.Thread(target=request.prepare_run)
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

        for request in self.races:
            threading.Thread(target=request.execute_run).start()

    # Helper Functions
    def build_request(self):
        self.races.append(self.__Request())

        return self.races[-1]

    def har(self, har):

        ret = []

        import json
        from haralyzer import HarParser, HarPage

        __har = HarParser(json.load(har))

        for __page in __har.pages:
            assert isinstance(__page, HarPage, None)
            __request = self.__Request()
            __request.har(__har, __page)
            self.races.append(__request)
            ret.appen(__request)

        return ret

# Debug
p('Debug Active')
