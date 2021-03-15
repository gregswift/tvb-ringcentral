#!/usr/bin/env python

import datetime
import os
import pprint
import sys
import ringcentral

STANDARD_SCHEDULE={'schedule': {'weeklyRanges': {
    'monday':    [{'from': '08:30', 'to': '17:30'}],
    'tuesday':   [{'from': '09:30', 'to': '18:30'}],
    'wednesday': [{'from': '08:30', 'to': '17:30'}],
    'thursday':  [{'from': '09:30', 'to': '18:30'}],
    'friday':    [{'from': '08:30', 'to': '17:30'}]
}}}

SATURDAY_SCHEDULE={'schedule': {'weeklyRanges': {
    'monday':    [{'from': '08:30', 'to': '17:30'}],
    'tuesday':   [{'from': '09:30', 'to': '18:30'}],
    'wednesday': [{'from': '08:30', 'to': '17:30'}],
    'thursday':  [{'from': '09:30', 'to': '18:30'}],
    'friday':    [{'from': '08:30', 'to': '17:30'}],
    'saturday':  [{'from': '08:30', 'to': '17:30'}]
}}}

# List of which saturday of the month to enable
WHICH_SATURDAYS=[3]

SATURDAY=5 # datetime.date().weekday for Saturday

def this_saturday(now=None):
    """ Return integer representing which saturday of the month
        the upcoming saturday is
    """
    if now is None:
        now = datetime.datetime.now()
    day = datetime.date(now.year, now.month, now.day)
    weekday = day.weekday()
    if weekday > SATURDAY:
        # Sunday is the only day larger than Saturday from datetime.date().weekday
        # and its also the number to add to timeshift us to the next
        # Saturday
        timeshift = weekday
        #print(f'Days till next Saturday: {timeshift}')
    else:
        # The difference is how many days till saturday
        timeshift = SATURDAY - weekday
        #print(f'Days till next Saturday ({SATURDAY} - {weekday}): {timeshift}')
    saturday = day + datetime.timedelta(days=timeshift)
    #print(saturday)
    if saturday.day >= 1 and saturday.day <= 7:
        return 1
    if saturday.day >= 8 and saturday.day <= 14:
        return 2
    if saturday.day >= 15 and saturday.day <= 21:
        return 3
    if saturday.day >= 22 and saturday.day <= 28:
        return 4
    if saturday.day >= 29 and saturday.day <= 31:
        return 5

def get_config():
    return {
        'clientid': os.environ.get('RINGCENTRAL_CLIENT_ID', None),
        'clientsecret': os.environ.get('RINGCENTRAL_CLIENT_SECRET', None),
        'server': os.environ.get('RINGCENTRAL_SERVER', None),
        'extension': os.environ.get('RINGCENTRAL_EXTENSION', None),
        'username': os.environ.get('RINGCENTRAL_USERNAME', None),
        'password': os.environ.get('RINGCENTRAL_PASSWORD', None),
        'accountid': '~',
        'extensionid': '~'
    }

def get_schedule(api, config):
    #path = f'/restapi/v1.0/account/{config["accountid"]}/extension/{config["extensionid"]}/business-hours'
    path = f'/restapi/v1.0/account/{config["accountid"]}/business-hours'
    print(f'Calling {path}')
    r = api.get(path)
    return r.json_dict()

def set_schedule(api, config, schedule):
    path = f'/restapi/v1.0/account/{config["accountid"]}/business-hours'
    print(f'Calling {path}')
    r = api.put(path, schedule)
    return r.json_dict()

def init_api(config):
    rcsdk = ringcentral.SDK(config["clientid"], config["clientsecret"], config["server"])
    platform = rcsdk.platform()
    platform.login(config["username"], config["extension"], config["password"])
    return platform

if __name__ == '__main__':
    config = get_config()
    #pprint.pprint(config)
    api = init_api(config)
    if len(sys.argv) > 1:
        x = 0
        while True:
            if x > 0:
                break
            if sys.argv[1] == 'get':
                pprint.pprint(get_schedule(api,config))
            if sys.argv[1] == 'enable-saturdays':
                if this_saturday() not in WHICH_SATURDAYS:
                    break
                pprint.pprint(set_schedule(api,config,SATURDAY_SCHEDULE))
            if sys.argv[1] in ['standard', 'disable-saturdays']:
                pprint.pprint(set_schedule(api,config,STANDARD_SCHEDULE))
            x += 1
        if 'help' in sys.argv[1]:
            print(f'Usage: {sys.argv[0]} get|standard|enable-saturdays|disable-saturdays|help')
