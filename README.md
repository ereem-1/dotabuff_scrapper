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
На домашней странице кликнуть на <h3>Посмотреть список героев<h3/>.
Далее открывается список ссылок на героев Dota2 с ссылкой на героев, которые хороши против выбранного.
Кликнув на ссылку с названием героя, на новой странице отображается его статистика по порядку 
<h2>Lane, Presence, Win Rate, KDA Ratio, GPM, XPM<h2/>
Кликнув на ссылку контрпика:
<h2>Hero, Disadvantage, Win Rate, Matches<h2/>
