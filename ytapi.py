#!/usr/bin/env python
#-*- coding: utf-8 -*-

# tested only in Linux

import sys, json
import urllib2 as request
from urllib import pathname2url
from platform import system as osdetect

YANDEX_TRANSLATE_JSON = "http://translate.yandex.net/api/v1/tr.json/translate?lang="

def win_toggle(get_str):
    if osdetect() == 'Windows':
        tmp = bytes(get_str).decode('cp1251')
        get_str = tmp.encode('utf-8')
    return get_str

def get_translate(for_translate, trans_type='en'):
    global YANDEX_TRANSLATE_JSON
    result = False
    for_translate = win_toggle(for_translate)
    prepate_url = pathname2url(for_translate)
    trans_types = {'en': 'en-ru', 'ru': 'ru-en'}
    prepate_url = YANDEX_TRANSLATE_JSON + trans_types[trans_type] + "&text=" + prepate_url
    try:
        conn = request.urlopen(prepate_url)
        if conn.code == 200:
            from_url = conn.read()
            result = json.loads(from_url)
    except Exception as e:
        print("Not connection\nError: ".format(e))
        return result
    else:
        conn.close()
    return result
 
def main():
    if len(sys.argv) > 1 and sys.argv[1] in ('en', 'ru'):
        args = sys.argv[2:]
        ttype = sys.argv[1]
    else:
        args = sys.argv[1:]
        ttype = 'en'
    arg = get_translate(" ".join(args), ttype)
    if arg:
        print(arg['text'][0])
    else:
        print("Error")
    return 0

if __name__ == "__main__":
    main()
