# Dota2Counters
A simple Python webscrapper to gather information of heroes' statistic and counters from Dotabuff.

## Instalation
You'll need requests and beautifulsoup4 for it to work.
```bash 
pip install requirements.txt
```

## How to use
Нужно запустить код с помощью команды
```bash 
python3 uvicorn main:app --reload
```
<p>На домашней странице кликнуть на ```bash Посмотреть список героев.```
Далее открывается список ссылок на героев Dota2 с ссылкой на героев, которые хороши против выбранного.<p/>
<p>Кликнув на ссылку с названием героя, на новой странице отображается его статистика по порядку<p/>
```bash Lane, Presence, Win Rate, KDA Ratio, GPM, XPM```
Кликнув на ссылку контрпика:
```bash Hero, Disadvantage, Win Rate, Matches```
