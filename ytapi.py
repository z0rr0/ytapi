#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys, json
import urllib2 as request
from urllib import pathname2url

YANDEX_TRANSLATE_JSON = "http://translate.yandex.net/api/v1/tr.json/translate?lang="

def get_translate(for_translate, trans_type='en'):
    global YANDEX_TRANSLATE_JSON
    result = False
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
    args = sys.argv[1:]
    arg = get_translate(" ".join(args))
    if arg:
        print(arg['text'][0])
    else:
        print("Error")
    return 0

if __name__ == "__main__":
    main()
