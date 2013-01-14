#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys, json
from urllib import request, parse

YANDEX_TRANSLATE_JSON = "http://translate.yandex.net/api/v1/tr.json/translate?"
YANDEX_SPELL_JSON = "http://speller.yandex.net/services/spellservice.json/checkText?"

def get_translate(for_translate, trans_type='en'):
    global YANDEX_TRANSLATE_JSON
    trans_types = {'en': 'en-ru', 'ru': 'ru-en'}
    result = False
    params = {'lang': trans_types[trans_type], 'text': for_translate}
    prepate_url = parse.urlencode(params, encoding="utf-8")
    try:
        conn = request.urlopen(YANDEX_TRANSLATE_JSON + prepate_url, None, 1)
        if conn.status == 200:
            from_url = conn.read().decode('utf-8')
            result = json.loads(from_url)
    except Exception as e:
        print("Not connection\nError: ".format(e))
        return result
    else:
        conn.close()
    return result
 
def check_spell(for_spelling, spell_type='en'):
    global YANDEX_SPELL_JSON
    result = False
    # options = IGNORE_DIGITS(2) + IGNORE_DIGITS(4) + IGNORE_CAPITALIZATION(512) + [BY_WORDS(256)]
    # params = {'lang': spell_type, 'text': for_spelling, 'format': 'plain', 'options': 518}
    params = {'lang': spell_type, 'text': for_spelling, 'format': 'html', 'options': 518}
    prepate_url = parse.urlencode(params, encoding="utf-8")
    erro_codes = ("ERROR_UNKNOWN_WORD",
        "ERROR_REPEAT_WORD",
        "ERROR_CAPITALIZATION",
        "ERROR_TOO_MANY_ERRORS")
    try:
        conn = request.urlopen(YANDEX_SPELL_JSON + prepate_url, None, 1)
        if conn.status == 200:
            from_url = conn.read().decode('utf-8')
            result = json.loads(from_url)
    except Exception as e:
        print("Not connection\nError: ".format(e))
        return result
    else:
        conn.close()
    if len(result) > 0:
        print("Spelling: ", end="")
        for_result = []
        for res in result:
            for_result.append("{0} -> {1}".format(res['word'], res['s']))
        print("; ".join(for_result))
    return 0

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ('en', 'ru'):
        args = sys.argv[2:]
        ttype = sys.argv[1]
    else:
        args = sys.argv[1:]
        ttype = 'en'
    check_spell(" ".join(args), ttype)
    arg = get_translate(" ".join(args), ttype)
    if arg:
        print(arg['text'])
    else:
        print("Error")
    return 0

if __name__ == "__main__":
    main()
