#!/usr/bin/python
#tw-woeid.py

import yweather

def getWOEID(location):
    return yweather.Client().fetch_woeid(location)
