__author__ = 'Matthias Uschok <dev@uschok.de>'

from autobahn.twisted.websocket import WebSocketServerProtocol
import json
import logging

class BotServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        logging.info("Client connecting: %s" % request.peer)

    def onOpen(self):
        logging.info("Connection open")

    def onClose(self, wasClean, code, reason):
        logging.info("Connection closed because: %s" % reason)

    def onMessage(self, payload, isBinary):
        if isBinary:
            return

    def gen_json(self):

            data = {}
            location = {}
            state = {}
            contact = {}

            data['api'] = '0.13'
            data['space'] = 'Stratum 0'
            data['logo'] = 'https:\/\/stratum0.org\/mediawiki\/images\/thumb\/c\/c6\/Sanduhr-twitter-avatar-black.svg\/240px-Sanduhr-twitter-avatar-black.svg.png'
            data['url']= 'https:\/\/stratum0.org'
            data['issue_report_channels'] = ['issue-mail']

            location['address'] = 'Hamburger Strasse 273a, 38114 Braunschweig, Germany'
            location['lon'] = 10.5211247
            location['lat'] = 52.2785658
            data['location'] = location

            contact['phone'] = '+4953128769245'
            contact['twitter'] = '@stratum0'
            contact['ml'] = 'normalverteiler@stratum0.org'
            contact['issue-mail'] = 'cm9oaWViK3NwYWNlYXBpLWlzc3Vlc0Byb2hpZWIubmFtZQ=='
            contact['irc'] = 'irc:\/\/irc.freenode.net\/#stratum0'
            data['contact'] = contact

            icon = {}
            icon['open'] = 'http:\/\/status.stratum0.org\/open_square.png'
            icon['closed'] = 'http:\/\/status.stratum0.org\/closed_square.png'
            state['icon'] = icon

            state['open'] = status.space['open']
            state['lastchange'] = status.space['last_change']
            state['trigger_person'] = status.space['by']
            state['ext_since'] = status.space['since']
            data['state'] = state

            return json.dumps(data)
