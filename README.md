# Ytapi

It is Python script to translate and check spelling using the console, it based on [Yandex Translate API](http://api.yandex.ru/translate/). By default the script uses **en-ru** direction and UTF-8 encoding.

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

* To use another language direction, you can choose needed one (en=en-ru, ru=ru-en) and use it as the first word in your request. The script can be simple modified to use other languages from [Yandex API documetation](http://api.yandex.ru/translate/langs.xml)

```
python3 ytapi.py en hi, you can use translation from your console
['Привет, вы можете использовать перевод с консоли']

python3 ytapi.py ru Привет, вы можете использовать перевод из консоли
['Hi, you can use the translation from the console']
```

* If your phrase for translation contains only one word then you will get dictionary article:

```
python3 ytapi.py en magazine
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

User should get API KEYs before an using this script, them values have to wrote to variables in file **key.py**:

1. **api_key** - API KEY for [Yandex Translate](http://api.yandex.ru/key/form.xml?service=trnsl)
2. **api\_key\_dict** - API KEY for [Yandex Dictionary](http://api.yandex.ru/key/form.xml?service=dict)


Implemented using the services:

* [Yandex Dictionary](http://api.yandex.ru/dictionary/)
* [Yandex Translate](http://api.yandex.ru/translate/)
* [Yandex Speller](http://api.yandex.ru/speller/)

<small>*Dependences: Python (default Python3, version for Python2 in 'python2' branch), urllib, json*</small>
