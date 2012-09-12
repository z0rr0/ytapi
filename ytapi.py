#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys, json
from urllib import request

YANDEX_TRANSLATE_JSON = "http://translate.yandex.net/api/v1/tr.json/translate?lang="

def get_translate(for_translate, trans_type='en'):
    global YANDEX_TRANSLATE_JSON
    result = False
    prepate_url = request.pathname2url(for_translate)
    trans_types = {'en': 'en-ru', 'ru': 'ru-en'}
    prepate_url = YANDEX_TRANSLATE_JSON + trans_types[trans_type] + "&text=" + prepate_url
    try:
        conn = request.urlopen(prepate_url)
        if conn.status == 200:
            from_url = conn.read().decode('utf-8')
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
        print(arg['text'])
    else:
        print("Error")
    return 0

if __name__ == "__main__":
    main()
