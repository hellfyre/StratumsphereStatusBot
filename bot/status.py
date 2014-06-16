# -*- coding: utf-8 -*-
__author__ = 'Matthias Uschok <dev@uschok.de>'

import time

space = dict()
space['open'] = False
space['by'] = ''
space['last_change'] = 0
space['since'] = 0

def init():
    space['since'] = int(time.time())
    space['last_change'] = space['since']

def compose_openclose_msg():
    topic = 'sudo '

    if space['open']:
        topic += 'open ' + space['by']
    else:
        topic += 'close'

    return topic

def compose_topic():
    topic = 'Space ist '
    time_str = time.strftime('%a, %H:%M', time.localtime(space['last_change']))

    if space['open']:
        topic += 'offen (' + time_str + ', ' + space['by'] + ')'
    else:
        topic += 'zu (' + time_str + ')'

    return topic

def parse_and_update(topic):
    try:
        open, by = parse_topic(topic)
        update(open, by)
    except ParseError, e:
        print e

def update(open, by):
    space['last_change'] = int(time.time())

    if not space['open'] == open:
        space['since'] = space['last_change']
    space['by'] = by
    space['open'] = open


def parse_topic(topic):
    is_open = False
    opened_by = ''

    root_parts = []
    if '||' in topic:
        root_parts = topic.split(' || ')
    else:
        root_parts.append(topic)

    status_part = ''
    for part in root_parts:
        if 'Space' in part and 'ist' in part and '(' in part and ')' in part and ('offen' in part or 'auf' in part or 'zu' in part):
            status_part = part

    if status_part == '':
        remaining_parts = ''
        for part in root_parts:
            remaining_parts += part + '  '
        raise ParseError('divide root parts', remaining_parts)

    global_status, sep, status_details = status_part.partition(' (')
    if global_status == '' or status_details == '':
        raise ParseError('divide status part', status_part)
    status_details = status_details.strip(')').split(',')

    if 'offen' in global_status or 'auf' in global_status:
        is_open = True

        if not len(status_details) == 3:
            errormsg = ''
            for part in status_details:
                errormsg += part + '  '
            raise ParseError('divide status details', errormsg)

        #status_details.pop(0)
        #time = status_details.pop(0).strip()
        #opened_by = status_details[0].strip()
        opened_by = status_details[2].strip()

    return is_open, opened_by

class ParseError(Exception):
    def __init__(self, component, string):
        self.string = '''Error parsing space status:
    component: {comp}
    string   : {string}'''.format(comp=component, string=string)
    def __str__(self):
        return self.string