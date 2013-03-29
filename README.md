# Yatapi

It is simple Python script, it based on [Yandex Translate API](http://api.yandex.ru/translate/doc/dg/reference/translate.xml). Default script uses **en-ru** direction.

Examples:

1. `./ytapi.py London is the capital of Great Britain`
<br>'Лондон-столица Великобритании'<br>
OR<br>
`./ytapi.py "London is the capital of Great Britain"`
<br>'Лондон-столица Великобритании'
2. `./ytapi.py en hi`
<br>'привет'
3. `./ytapi.py ru привет всем`
<br>'hi all'

<small>*Dependences: Python (default Python3, version for Python2 in 'python2' branch), urllib, json*</small>