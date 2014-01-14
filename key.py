#!/usr/bin/env python3

DEBUG = False
# to get own key see http://api.yandex.ru/key/form.xml?service=trnsl
api_key = ""
# to get own key see http://api.yandex.ru/key/form.xml?service=dict
api_key_dict = ""
# for example {'http': 'http://myproxy.com:8080/'}
proxies = {}

try:
    from local_key import *
except ImportError:
    pass
