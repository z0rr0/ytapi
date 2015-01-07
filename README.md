# Ytapi

It is Python script to translate and check spelling using the console, it based on [Yandex Translate API](http://api.yandex.ru/translate/). By default the script uses UTF-8 encoding.

### Examples

* Translation from English to Russian

```
python3 ytapi.py London is the capital of Great Britain
['Лондон-столица Великобритании']
```

If your phrase contains qoutes then you can use single qoutes for all text or back slash:

```
python3 ytapi.py \"Yandex\" is a Russian Internet company
['"Яндекс" - Российская Интернет-компания']
```

* To use another language direction, you can choose needed one using "--langs" parameter and use it as the first word in your request.

```
python3 ytapi.py en-ru hi, you can use translation from your console
['Привет, вы можете использовать перевод с консоли']

python3 ytapi.py ru-en Привет, вы можете использовать перевод из консоли
['Hi, you can use the translation from the console']
```

* If your phrase for translation contains only one word then you will get dictionary article:

```
python3 ytapi.py en-ru magazine

magazine [mægəˈziːn] (noun)
        журнал (существительное)
        syn: кассета, обойма, журнальчик
        mean: journal, cartridge
        examples: Forbes magazine: журнал Forbes
                China sourcing magazine: кассета Sourcing Китая
                spare magazine: запасная обойма
        магазин (существительное)
        examples: box magazine: коробчатый магазин
magazine [mægəˈziːn] (adjective)
        журнальный (прилагательное)
        mean: journal
        examples: magazine table: журнальный столик
```



### API keys

You should get API KEYs before an using this program, them values have to written to a file **$HOME/.ytapi.json** (see the example `ytapigo_example.json`). **APIlangs** is a set of [available translate directions](https://tech.yandex.ru/translate/doc/dg/concepts/langs-docpage/), each one can have a list of possible user's aliases.

```javascript
{
  "APItr": "some key value",
  "APIdict": "some key value",
  "Aliases": {                      // User's languages aliases
    "en-ru": ["en", "англ"],
    "ru-en": ["ru", "ру"],
  },
  "Default": "en-ru"                // default translation direction
}
```

1. **APItr** - API KEY for [Yandex Translate](https://tech.yandex.ru/keys/get/?service=trnsl)
2. **APIdict** - API KEY for [Yandex Dictionary](https://tech.yandex.ru/keys/get/?service=dict)

It was implemented using the services:

* [Yandex Dictionary](http://api.yandex.com/dictionary/)
* [Yandex Translate](http://api.yandex.com/translate/)
* [Yandex Speller](http://api.yandex.ru/speller/)


<small>*Dependences: Python standart library (default Python3, version for Python2 in 'python2' branch).*</small>
