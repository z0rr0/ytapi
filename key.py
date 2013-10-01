#!/usr/bin/env python

DEBUG = False
# to get own key see http://api.yandex.ru/key/keyslist.xml
api_key = ""

try:
    from local_key import *
except ImportError:
    pass
