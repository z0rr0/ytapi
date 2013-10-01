# Yatapi

It is easy Python script to translate and check spelling using the console, it based on [Yandex Translate API](http://api.yandex.ru/translate/). By default the script uses **en-ru** direction and UTF-8 encoding.

### Examples

* Translation from English to Russian

```
python3 ytapi.py London is the capital of Great Britain
['Лондон-столица Великобритании']
```

If your phrase contains qoutes then you can use single qoutes or back slash:

```
python3 ytapi.py \"Yandex\" is a Russian Internet company
['"Яндекс" - Российская Интернет-компания']
```

* To use another language direction, you can choose needed ones (en=en-ru, ru=ru-en) and use it as the first word in your request. The script can be simple modified to use other languages from [Yandex API documetation](http://api.yandex.ru/translate/langs.xml)

```
python3 ytapi.py en hi, you can use translation from your console
['Привет, вы можете использовать перевод с консоли']

python3 ytapi.py ru Привет, вы можете использовать перевод из консоли
['Hi, you can use the translation from the console']
```

The variable **api_key** in file key.py should contain your API KEY, you can get it for free on [Yandex web page](http://api.yandex.ru/key/form.xml?service=trnsl).

<small>*Dependences: Python (default Python3, version for Python2 in 'python2' branch), urllib, json*</small>