# -*- coding: utf-8 -*-
__author__ = 'Matthias Uschok <dev@uschok.de>'

import irc.bot
import irc.strings
from jsonserver import JsonServer, callbacks
import status

class StratumsphereStatusBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel):
        irc.bot.SingleServerIRCBot.__init__(self, [('chat.freenode.net', 6667)], 'fyrebot', 'fyrebot2.0')
        self.channel = channel
        self.guardian = dict()
        self.guardian['present'] = False
        self.guardian['name'] = 'StratumGuardian'

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + 'I')

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_join(self, c, e):
        if irc.strings.lower(self.guardian['name']) in irc.strings.lower(e.source.nick):
            print 'Guardian joined'
            self.guardian['present'] = True
        elif irc.strings.lower(e.source.nick) == irc.strings.lower(c.get_nickname()):
            print 'Joined ' + e.target

    def on_quit(self, c, e):
        if irc.strings.lower(self.guardian['name']) in irc.strings.lower(e.source.nick):
            print 'Guardian quit'
            self.guardian['present'] = False

    def on_currenttopic(self, c, e):
        self.topic = e.arguments[1].split(' || ')
        status.parse_and_update(e.arguments[1])

    def on_topic(self, c, e):
        self.topic = e.arguments[0].split(' || ')
        status.parse_and_update(e.arguments[0])

    def on_namreply(self, c, e):
        names = e.arguments[2].split(' ')
        for name in names:
            if irc.strings.lower(self.guardian['name']) in irc.strings.lower(name):
                self.guardian['present'] = True
        if self.guardian['present']:
            print 'Guardian is present'
        else:
            print 'Guardian is absent'

    def on_pubmsg(self, c, e):
        if e.arguments[0].startswith('sudo ') and not self.guardian['present']:
            self.do_sudo_command(e, e.arguments[0].replace('sudo ', ''))
        # else:
        #     parts = e.arguments[0].split(':',1)
        #     if len(parts) > 1 and irc.strings.lower(parts[0].strip()) == irc.strings.lower(self.connection.get_nickname()):
        #         self.do_command(e, parts[1].strip())


    def on_privmsg(self, c, e):
        c.privmsg(self.channel, 'I\'m being harassed by ' + e.source.nick)

    def do_sudo_command(self, e, command):
        if command == 'open':
            status.update(True, e.source.nick)
            self.send_status()
        elif command == 'close':
            status.update(False, '')
            self.send_status()

    # def do_command(self, e, command):
    #     pass

    def send_status(self):
        if self.guardian['present']:
            self.connection.privmsg(self.channel, status.compose_openclose_msg())
        else:
            new_topic = []

            if len(self.topic) > 0:
                new_topic.append(self.topic[0])
            new_topic.append(status.compose_topic())

            for part in self.topic[2:]:
                new_topic.append(part)

            new_topic_str = new_topic.pop(0)
            for part in new_topic:
                new_topic_str += ' || ' + part

            self.connection.topic(self.channel, new_topic_str)

def main():
    try:
        bot = StratumsphereStatusBot('#stratum0')
        callbacks['send_status'] = bot.send_status
        jsonserver = JsonServer(('134.169.175.96', 8766))

        status.init()
        jsonserver.start()
        bot.start()
    except KeyboardInterrupt:
        bot.connection.quit("I'm meeeltiiiiiiing!")
        jsonserver.stop()
        jsonserver.join()

if __name__ == "__main__":
    main()