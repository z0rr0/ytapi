#!/usr/bin/env python3

DEBUG = False
# to get own key see http://api.yandex.ru/key/keyslist.xml
api_key = ""

try:
    from local_key import *
except ImportError:
    pass
