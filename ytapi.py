#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys, json, key
import urllib2 as request
from urllib import urlencode
from platform import system as osdetect

YANDEX_TRANSLATE_JSON = "https://translate.yandex.net/api/v1.5/tr.json/translate?"
YANDEX_DICT_JSON = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup?"
YANDEX_SPELL_JSON = "http://speller.yandex.net/services/spellservice.json/checkText?"
FORMAT = ('plain', 'html')

def win_toggle(get_str):
    if osdetect() == 'Windows':
        tmp = bytes(get_str).decode('cp1251')
        get_str = tmp.encode('utf-8')
    return get_str

def get_dict(for_dict, dict_type):
    global YANDEX_DICT_JSON
    result = None
    params = {
        'key': key.api_key_dict,
        'lang': dict_type,
        'text': for_dict,
    }
    prepate_url = urlencode(params)
    if key.DEBUG: print(YANDEX_DICT_JSON + prepate_url)
    try:
        conn = request.urlopen(YANDEX_DICT_JSON + prepate_url, None, 1)
        if conn.code == 200:
            from_url = conn.read().decode('utf-8')
            result = json.loads(from_url)
            # prepare result
            all_result = []
            for d in result['def']:
                ts = u" [{0}] ".format(d['ts']) if 'ts' in d.keys() else u" "
                txt_result = u"{0}{1}({2})\n".format(d['text'], ts, d['pos'])
                ar_result = []
                for res in d['tr']:
                    keys = res.keys()
                    syn, mean, ex = u"", u"", u""
                    if 'syn' in keys:
                        syn = u"\n\tsyn: " + u", ".join([s['text'] for s in res['syn']])
                    if 'mean' in keys:
                        mean = u"\n\tmean: " + u", ".join([s['text'] for s in res['mean']])
                    if 'ex' in keys:
                        ex = u"\n\texamples:\n\t\t" + u"\n\t\t".join([u"{0}: {1}".format(s['text'], u", ".join([t["text"] for t in s['tr']])) for s in res['ex']])
                    ar_result.append(u"\t{0} ({1}){2}{3}{4}".format(res['text'], res['pos'], syn, mean, ex))
                all_result.append(txt_result + u"\n".join(ar_result))
            result = "\n".join(all_result)
        else:
            print("ERROR: connection answer code - {0}".format(conn.code))
    except Exception as e:
        print("ERROR: {0}".format(e))
        return result
    else:
        if key.DEBUG: print(from_url)
    finally:
        conn.close()
    return result

def get_translate(for_translate, trans_type='en'):
    global YANDEX_TRANSLATE_JSON
    result = None
    for_translate = win_toggle(for_translate)
    trans_types = {'en': 'en-ru', 'ru': 'ru-en'}
    if len(for_translate.split()) == 1:
        if key.DEBUG: print("DICT: len={0}, using dictionary api".format(len(for_translate.split())))
        return get_dict(for_translate, trans_types[trans_type])
    params = {
        'key': key.api_key,
        'lang': trans_types[trans_type],
        'text': for_translate,
        'format': FORMAT[0]
    }
    prepate_url = urlencode(params)
    if key.DEBUG: print(YANDEX_TRANSLATE_JSON + prepate_url)
    try:
        conn = request.urlopen(YANDEX_TRANSLATE_JSON + prepate_url)
        if conn.code == 200:
            from_url = conn.read().decode('utf-8')
            result = json.loads(from_url)['text'][0]
        else:
            print("ERROR: connection answer code - {0}".format(conn.status))
            return result
    except Exception as e:
        print("Not connection\nError: ".format(e))
    else:
        if key.DEBUG: print("debug mode:", result)
    finally:
        conn.close()
    return result

def check_spell(for_spelling, spell_type='en'):
    global YANDEX_SPELL_JSON
    params = {
        'lang': spell_type,
        'text': for_spelling,
        'format': 'plain',
        'options': 518}
    prepate_url = urlencode(params)
    erro_codes = ("ERROR_UNKNOWN_WORD",
        "ERROR_REPEAT_WORD",
        "ERROR_CAPITALIZATION",
        "ERROR_TOO_MANY_ERRORS")
    try:
        conn = request.urlopen(YANDEX_SPELL_JSON + prepate_url, None, 1)
        if conn.code == 200:
            from_url = conn.read().decode('utf-8')
            result = json.loads(from_url)
        else:
            print("ERROR: connection answer code - {0}".format(conn.status))
            return result
    except Exception as e:
        print("Not connection\nError: ".format(e))
        return 1
    else:
        if key.DEBUG: print(from_url)
    finally:
        conn.close()
    if len(result) > 0:
        print("Spelling: ", end="")
        for_result = []
        for res in result:
            variants = u", ".join(res['s'])
            for_result.append(u"{0} -> {1}".format(res['word'], variants))
        print("; ".join(for_result))
    return 0

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ('en', 'ru'):
        args = sys.argv[2:]
        ttype = sys.argv[1]
    else:
        args = sys.argv[1:]
        ttype = 'en'
    if check_spell(" ".join(args), ttype):
        print("WARNING: spellig error")
    arg = get_translate(" ".join(args), ttype)
    if arg:
        print(arg)
    else:
        print("ERROR: no result.")
    return 0

if __name__ == "__main__":
    main()
