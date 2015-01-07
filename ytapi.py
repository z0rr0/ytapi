#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os, sys, json, logging, asyncio, urllib, re, argparse
from urllib import request, parse

# 0-Spelling, 1-Translation, 2-Dictionary,
# 3-Translation directions, 4-Dictionary directions
YtJsonURLs = (
    "http://speller.yandex.net/services/spellservice.json/checkText?",
    "https://translate.yandex.net/api/v1.5/tr.json/translate?",
    "https://dictionary.yandex.net/api/v1/dicservice.json/lookup?",
    "https://translate.yandex.net/api/v1.5/tr.json/getLangs?",
    "https://dictionary.yandex.net/api/v1/dicservice.json/getLangs?"
)
FORMAT = ('plain', 'html')
# config file in $HOME
CONFIG = ".ytapi.json"
CONFIG_DIR = os.environ["HOME"]
LDPATTERN = re.compile(r'^[a-z]{2}-[a-z]{2}$')
HTTPER = "Network connection problems. Cannot send HTTP request."

def ytrequest(obj, url, params):
    """sends HTTP request and checks its result code"""
    encoding, timeout = "utf-8", 5
    prepare_params = parse.urlencode(params, encoding=encoding)
    proxy_handler = request.ProxyHandler(obj.cfg("proxies")) if obj.cfg("proxies") else request.ProxyHandler()
    try:
        opener = request.build_opener(proxy_handler)
        with opener.open(url, bytes(prepare_params, encoding), timeout) as conn:
            if conn.status != 200:
                raise YtException("Wrong response code={0}".format(conn.status))
            result = conn.read().decode(encoding)
    except (Exception,) as err:
        logging.debug("url={0}, error={1}".format(url, err))
        result = ""
    return result

@asyncio.coroutine
def get_spelling(obj, lang, txt):
    """gets a spell check result"""
    params = {
        'lang': lang,
        'text': txt,
        'format': FORMAT[0],
        'options': 518
    }
    data = ytrequest(obj, YtJsonURLs[0], params)
    if not data:
        logging.error("Cannot check a spelling. {0}".format(HTTPER))
        return
    result = json.loads(data)
    if len(result) > 0:
        obj.spelling
        for_result = []
        for res in result:
            for_result.append("{0} -> {1}".format(res['word'], res['s']))
        obj.spelling = "Spelling:\n\t{0}".format("; ".join(for_result))

@asyncio.coroutine
def get_translation(obj, txt):
    """translates the text"""
    params = {
        'lang': obj.langs,
        'text': txt
    }
    if len(txt.split(" ")) > 1:
        isdict, url = False, YtJsonURLs[1]
        params['key'], params['format'] = obj.cfg("APItr"), FORMAT[0]
    else:
        isdict, url = True, YtJsonURLs[2]
        params['key'] = obj.cfg("APIdict")
    data = ytrequest(obj, url, params)
    if not data:
        logging.error("Cannot get a translation. {0}".format(HTTPER))
        return
    data = json.loads(data)
    obj.translate = (isdict, data)

@asyncio.coroutine
def get_lang_list(obj, isdict):
    """gets available languages"""
    if isdict:
        url, params = YtJsonURLs[4], {"key": obj.cfg("APIdict")}
    else:
        url, params = YtJsonURLs[3], {"key": obj.cfg("APItr"), "ui": "en"}
    data = ytrequest(obj, url, params)
    if not data:
        return
    data = json.loads(data)
    if isdict:
        obj.langslist["dict"] = data
    else:
        obj.langslist["tr"] = data

class YtException(Exception):
    """docstring for YtException"""
    def __init__(self, msg):
        super(YtException, self).__init__()
        self._msg = msg

    def __str__(self):
        return repr(self._msg)

class Translater(object):
    """docstring for Translater"""
    def __init__(self):
        super(Translater, self).__init__()
        self._cfgpath, self._config = None, {}
        self._langs, self._alias = "", False
        self.langslist = {"tr": None, "dict": None}
        self._spelling, self._translate = "", ""

    @property
    def cfgpath(self):
        return self._cfgpath
    @property
    def isalias(self):
        return self._alias
    @property
    def langs(self):
        return self._langs
    @property
    def spelling(self):
        return self._spelling
    @spelling.setter
    def spelling(self, value):
        self._spelling = value
    @property
    def translate(self):
        return self._translate
    @translate.setter
    def translate(self, value):
        isdict, result = value[0], value[1]
        if isdict:
            all_result = []
            for d in result['def']:
                ts = " [{0}] ".format(d['ts']) if 'ts' in d.keys() else " "
                txt_result = "{0}{1}({2})\n".format(d['text'], ts, d['pos'])
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
            self._translate = "\n".join(all_result)
        else:
            self._translate = result.get("text", [""])[0]

    def cfg(self, key):
        return self._config.get(key)

    def read_config(self):
        """load data from configuration file"""
        self._cfgpath = os.path.join(CONFIG_DIR, CONFIG)
        with open(self._cfgpath, 'r') as filename:
            data = json.load(filename)
        self._config = {
            "APItr": data.get("APItr", ""),
            "APIdict": data.get("APIdict", ""),
            "Aliases": data.get("Aliases", {}),
            "Default": data.get("Default", ""),
            "Debug": data.get("Debug", False),
            "proxies": data.get("proxies", {}) # only for backward compatibility
        }
        if self._config["Debug"]:
            logging.basicConfig(format="%(levelname)s %(asctime)s %(funcName)s:%(lineno)d  %(message)s", level=logging.DEBUG)
        else:
            logging.basicConfig(format="ERROR: %(message)s", level=logging.ERROR)
        if (not self._config["APItr"]) or (not self._config["APIdict"]):
            raise YtException("Can not read API keys values from the config file: {0}".format(cfg_path))
        for i, v in self._config["Aliases"].items():
            self._config["Aliases"][i] = set(v)


    def check_direction(self):
        """checks - default direction is available"""
        default = self.cfg("Default")
        if not default:
            return False, False
        loop, tasks = asyncio.get_event_loop(), []
        tasks.append(asyncio.async(get_lang_list(self, True)))
        tasks.append(asyncio.async(get_lang_list(self, False)))
        loop.run_until_complete(asyncio.wait(tasks))
        assert (self.langslist["tr"] is not None) and (self.langslist["dict"] is not None)
        self._langs, self._alias = default, False
        return (default in self.langslist["dict"]), (default in self.langslist["tr"]["dirs"])

    def check_aliasdirection(self, direction):
        if not direction:
            return False, False
        self._langs, self._alias = self.cfg("Default"), False
        alias = direction
        for i, v in self._config["Aliases"].items():
            if i == direction:
                break
            if direction in v:
                alias = i
                break
        loop, tasks = asyncio.get_event_loop(), []
        tasks.append(asyncio.async(get_lang_list(self, True)))
        tasks.append(asyncio.async(get_lang_list(self, False)))
        loop.run_until_complete(asyncio.wait(tasks))
        if LDPATTERN.match(alias):
            logging.debug("Maybe it is a direction - {0}".format(alias))
            lchd_ok, lchtr_ok = (alias in self.langslist["dict"]), (alias in self.langslist["tr"]["dirs"])
            if lchd_ok or lchtr_ok:
                self._langs, self._alias = alias, True
                return lchd_ok, lchtr_ok
        logging.debug("Not found lang for alias \"{0}\", default direction \"{1}\" will be used.".format(alias, self._langs))
        return (self._langs in self.langslist["dict"]), (self._langs in self.langslist["tr"]["dirs"])

    def get_source(self):
        """get source language"""
        langs = self._langs.split("-")
        if len(langs) < 2:
            raise YtException("Cannot detect source language. Please check the config file: {0}".format(self.cfgpath))
        return langs[0]

def get_langs():
    """will print available languages"""
    n = 3
    result, trobj = "", Translater()
    try:
        trobj.read_config()
        ddir_ok, tdir_ok = trobj.check_direction()
        trobj.langslist["dict"].sort()
        trobj.langslist["tr"]["dirs"].sort()
        desc_str = []
        for k, v in trobj.langslist["tr"].get("langs", []).items():
            desc_str.append("{0} - {1}".format(k, v))
        desc_str.sort()
        counter, output = len(desc_str), []
        collen = counter // n + 1 if counter % n else counter // n
        for j in range(collen):
            if j + 2 * collen < counter:
                output.append("{0:<25} {1:<25} {2:<25}".format(desc_str[j], desc_str[j+collen], desc_str[j+2*collen]))
            elif j + collen < counter:
                output.append("{0:<25} {1:<25}".format(desc_str[j], desc_str[j+collen]))
            else:
                output.append("{0:<25}".format(desc_str[j]))
        result = "Dictionary languages:\n{0}\nTranslation languages:\n{1}\n{2}".format(", ".join(trobj.langslist["dict"]), ", ".join(trobj.langslist["tr"]["dirs"]), "\n".join(output))
    except (YtException, AssertionError) as err1:
        logging.error(err1)
    except (IOError) as err2:
        print("ERROR: {0}".format(err2))
    return result

def get_tr(params):
    """main method to get translation results"""
    result = ""
    trobj, lenparams, txt = Translater(), len(params), ""
    try:
        trobj.read_config()
        if lenparams < 1:
            raise YtException("Too few parameters.")
        elif lenparams == 1:
            ddir_ok, tdir_ok = trobj.check_direction()
            if not ddir_ok:
                raise YtException("Cannot verify 'Default' translation direction. Please check a language direction prefix the config file: {0}".format(trobj.cfgpath))
            langs, alias = trobj.cfg("Default"), False
            trobj.isdict, txt = True, params[0]
        else:
            ddir_ok, tdir_ok = trobj.check_aliasdirection(params[0])
            if (not ddir_ok) and (not tdir_ok):
                raise YtException("Cannot verify translation direction. Please check a language direction prefix  the config file: {0}".format(trobj.cfgpath))
            if trobj.isalias:
                if (len(params[1].split(" ")) == 1) and (not ddir_ok):
                    raise YtException("Cannot verify dictionary direction. Please check a language direction prefix the config file: {0}".format(trobj.cfgpath))
                txt = " ".join(params[1:])
            else:
                txt = " ".join(params)
        source = trobj.get_source()
        loop, tasks = asyncio.get_event_loop(), []
        if source in ("en", "uk", "r"):
            tasks.append(asyncio.async(get_spelling(trobj, source, txt)))
        tasks.append(asyncio.async(get_translation(trobj, txt)))
        loop.run_until_complete(asyncio.wait(tasks))
        result = "{0}\n{1}".format(trobj.spelling, trobj.translate)
    except (YtException, AssertionError) as err1:
        logging.error(err1)
    except (IOError) as err2:
        print("ERROR: {0}".format(err2))
    return result

def main():
    """main method"""
    parser = argparse.ArgumentParser(description='It is a program to translate and check spelling using the console, it based on Yandex Translate API ')
     # parser.add_argument('-h', '--help')
    parser.add_argument('-l', '--langs', action='store_true', help="show available translation directions and languages")
    parser.add_argument('params', nargs='*', help="text for translation")
    args = parser.parse_args()
    show_langs, params = args.langs, args.params

    if show_langs:
        print(get_langs())
    else:
        print(get_tr(params))

if __name__ == "__main__":
    main()





