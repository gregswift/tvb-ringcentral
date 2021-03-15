#!/usr/bin/env python

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
                pprint.pprint(set_schedule(api,config,SATURDAY_SCHEDULE))
            if sys.argv[1] in ['standard','disable-saturdays']:
                pprint.pprint(set_schedule(api,config,STANDARD_SCHEDULE))
            x += 1
        if 'help' in sys.argv[1]:
            print(f'Usage: {sys.argv[0]} get|standard|enable-saturdays|disable-saturdays|help')
