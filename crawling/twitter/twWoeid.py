#!/usr/bin/python
#twWoeid.py

import yweather

#--------------------------------------------------------------------------
# 지역명에 해당하는 WOEID 반환
#--------------------------------------------------------------------------
def getWOEID(location):
    return yweather.Client().fetch_woeid(location)
