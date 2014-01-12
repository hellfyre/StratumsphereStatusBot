# -*- coding: utf-8 -*-
__author__ = 'Matthias Uschok <dev@uschok.de>'

import json
import BaseHTTPServer
import threading
from urlparse import parse_qs, urlparse

import status

callbacks = dict()

class JsonHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        print("path:", self.path)
        if self.path == '/status.json':
            data = {
                'api' : '0.13',
                'space' : 'Stratum 0',
                'logo' : 'https:\/\/stratum0.org\/mediawiki\/images\/thumb\/c\/c6\/Sanduhr-twitter-avatar-black.svg\/240px-Sanduhr-twitter-avatar-black.svg.png',
                'url': 'https:\/\/stratum0.org',
                'location' : {
                    'address': 'Hamburger Strasse 273a, 38114 Braunschweig, Germany',
                    'lon' : 10.5211247,
                    'lat' : 52.2785658
                },
                'state' : {
                    'open' : status.space['open'],
                    'lastchange' : status.space['last_change'],
                    'trigger_person' : status.space['by'],
                    'icon' : {
                        'open' : 'http:\/\/status.stratum0.org\/open_square.png',
                        'closed' : 'http:\/\/status.stratum0.org\/closed_square.png'
                    },
                    'ext_since' : status.space['since']
                },
                'contact' : {
                    'phone' : '+4953128769245',
                    'twitter' : '@stratum0',
                    'ml' : 'normalverteiler@stratum0.org',
                    'issue-mail' : 'cm9oaWViK3NwYWNlYXBpLWlzc3Vlc0Byb2hpZWIubmFtZQ==',
                    'irc' : 'irc:\/\/irc.freenode.net\/#stratum0'
                },
                'issue_report_channels' : [
                    'issue-mail'
                ]
            }
            data_string = json.dumps(data)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(data_string)
            self.wfile.write('\n')
        elif self.path.startswith('/update?'):
            queryurl = urlparse(self.path)
            params = parse_qs(queryurl.query)

            if len(params) > 0:
                by = ''
                if 'by' in params:
                    by = params['by'][0]

                status.update(params['open'][0]=='true', by)
                callbacks['send_status']()

                self.send_response(200)
            else:
                self.send_response(400)

        else:
            self.send_response(404)

class JsonServer(threading.Thread):

    def __init__(self, address):
        super(JsonServer, self).__init__()
        self.address = address
        self.stop_requested = False

    def run(self):
        self.httpd = BaseHTTPServer.HTTPServer(self.address, JsonHandler)
        while not self.stop_requested:
            self.httpd.handle_request()

    def stop(self):
        self.stop_requested = True
