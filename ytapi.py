#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys, json, key
from urllib import request, parse

YANDEX_TRANSLATE_JSON = "https://translate.yandex.net/api/v1.5/tr.json/translate?"
YANDEX_DICT_JSON = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup?"
YANDEX_SPELL_JSON = "http://speller.yandex.net/services/spellservice.json/checkText?"
FORMAT = ('plain', 'html')

def get_dict(for_dict, dict_type):
    global YANDEX_DICT_JSON
    result = None
    params = {
        'key': key.api_key_dict,
        'lang': dict_type,
        'text': for_dict,
    }
    prepate_url = parse.urlencode(params, encoding="utf-8")
    if key.DEBUG: print(YANDEX_DICT_JSON + prepate_url)
    try:
        conn = request.urlopen(YANDEX_DICT_JSON + prepate_url, None, 1)
        if conn.status == 200:
            from_url = conn.read().decode('utf-8')
            result = json.loads(from_url)
            # prepare result
            all_result = []
            for d in result['def']:
                ts = " [{0}] ".format(d['ts']) if 'ts' in d.keys() else " "
                txt_result = u"{0}{1}({2})\n".format(d['text'], ts, d['pos'])
                ar_result = []
                for res in d['tr']:
                    keys = res.keys()
                    syn, mean, ex = "", "", ""
                    if 'syn' in keys:
                        syn = "\n\tsyn: " + ", ".join([s['text'] for s in res['syn']])
                    if 'mean' in keys:
                        mean = "\n\tmean: " + ", ".join([s['text'] for s in res['mean']])
                    if 'ex' in keys:
                        ex = "\n\texamples:\n\t\t" + "\n\t\t".join(["{0}: {1}".format(s['text'], ", ".join([t["text"] for t in s['tr']])) for s in res['ex']])
                    ar_result.append("\t{0} ({1}){2}{3}{4}".format(res['text'], res['pos'], syn, mean, ex))
                all_result.append(txt_result + "\n".join(ar_result))
            result = "\n".join(all_result)
        else:
            print("ERROR: connection answer code - {0}".format(conn.status))
    except ValueError as e:
        print("ERROR: {0}".format(e))
        return result
    else:
        if key.DEBUG: print(from_url)
    # finally:
    #     conn.close()
    return result

def get_translate(for_translate, trans_type='en'):
    global YANDEX_TRANSLATE_JSON, FORMAT
    trans_types = {'en': 'en-ru', 'ru': 'ru-en'}
    if len(for_translate.split()) == 1:
        if key.DEBUG: print("DICT: len={0}, using dictionary api".format(len(for_translate)))
        return get_dict(for_translate, trans_types[trans_type])
    result = None
    params = {
        'key': key.api_key,
        'lang': trans_types[trans_type],
        'text': for_translate,
        'format': FORMAT[0]
    }
    prepate_url = parse.urlencode(params, encoding="utf-8")
    if key.DEBUG: print(YANDEX_TRANSLATE_JSON + prepate_url)
    try:
        conn = request.urlopen(YANDEX_TRANSLATE_JSON + prepate_url, None, 1)
        if conn.status == 200:
            from_url = conn.read().decode('utf-8')
            result = json.loads(from_url)
        else:
            print("ERROR: connection answer code - {0}".format(conn.status))
    except Exception as e:
        print("ERROR: {0}".format(e))
        return result
    else:
        if key.DEBUG: print(from_url)
    # finally:
    #     conn.close()
    return result["text"]

def check_spell(for_spelling, spell_type='en'):
    global YANDEX_SPELL_JSON
    result = None
    # options = IGNORE_DIGITS(2) + IGNORE_DIGITS(4) + IGNORE_CAPITALIZATION(512) + [BY_WORDS(256)]
    # params = {'lang': spell_type, 'text': for_spelling, 'format': 'plain', 'options': 518}
    params = {
        'lang': spell_type,
        'text': for_spelling,
        'format': 'plain',
        'options': 518}
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
        else:
            print("ERROR: connection answer code - {0}".format(conn.status))
    except Exception as e:
        print("ERROR: {0}".format(e))
        return 1
    else:
        if key.DEBUG: print(from_url)
    # finally:
    #     conn.close()
    if len(result) > 0:
        print("Spelling: ", end="")
        for_result = []
        for res in result:
            for_result.append("{0} -> {1}".format(res['word'], res['s']))
        print("; ".join(for_result))
    return 0

def main():
    if len(sys.argv) > 1 and (sys.argv[1] in ('en', 'ru')):
        args = sys.argv[2:]
        ttype = sys.argv[1]
    else:
        args = sys.argv[1:]
        ttype = 'en'
    if check_spell(" ".join(args), ttype):
        print("WARNING: spelling check error")
    arg = get_translate(" ".join(args), ttype)
    if arg:
        print(arg)
    else:
        print("ERROR: no result")
    return 0

if __name__ == "__main__":
    main()
