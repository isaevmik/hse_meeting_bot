# hse_meeting_bot
Телеграмм бот аля RandomCoffee для ФКН НИУ ВШЭ

## Из текущего функционала:

1) Регистрация с капчей
2) По нажатию на кнопку - получить контакт для встречи.

## Из планируемого:

1) Добавить возможноть откладывать встречи.
1) Добавить возможность отменять встречи.
3) Подбор встреч по интересам.
4) Оставить отзыв о встрече.

## Для запуска необходимо установить зависимости pypoetry:

```bash
poetry install
```

Сгенерировать БД:

```bash
poetry run make db
```

И запустить бота:

```bash
poetry run make run
```

## NB:
1) Список доступных команд:

```bash
make help
```

2) Чтобы постоянно не писать poetry run - можно сменить среду окружения через обычынй venv

3) Логи пишутся в bot.log в режиме **+a**