# hse_meeting_bot
Телеграмм бот аля RandomCoffee для ФКН НИУ ВШЭ

Из текущего функционала:

1) Регистрация с капчей
2) По нажатию на кнопку - получить контакт для встречи.

Из планируемого:

1) Добавить возможноть откладывать встречи.
1) Добавить возможность отменять встречи.
3) Подбор встреч по интересам.
4) Оставить отзыв о встрече.

Для запуска необходимо установить зависимости из файла requirements.txt:

```
pip3 install -r requrements.txt
```

Сгенерировать БД:
```
python3 build_database.py
```

И запустить бота:

```
python3 main.py
```