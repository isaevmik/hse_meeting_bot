from decouple import config
from dotenv import load_dotenv
import logging
import os
import telebot


from captcha_generator import get_captcha
from database.models import bot_users, meetings
from messages import captcha_messages, meetings_messages, welcome


print(logging.__file__)
load_dotenv()

API_TOKEN: str = config("TELEGRAM_BOT_TOKEN")

CAPTCHA_TRYOUTS: int = 5

_LOGGER = logging.basicConfig(
    filename=f"{os.path.dirname(os.path.abspath(__file__))}/bot.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)

_LOGGER = logging.getLogger(__name__)
_LOGGER.info("Logger-1 started successfully")

bot = telebot.TeleBot(API_TOKEN)


def captcha_checker(
    message: telebot.types.Message, captcha_txt: str, cnt: int = 0
) -> None:

    _LOGGER.info(f"Captcha {message.text} by {message.from_user.id} / {captcha_txt}")

    bot.send_message(message.chat.id, captcha_messages.CHECK_MESSAGE)

    if message.text.lower() == captcha_txt:
        bot.send_message(message.chat.id, captcha_messages.CAPTCHA_CORRECT)

        bot_users.insert(
            {
                bot_users.telegram_id: message.from_user.id,
                bot_users.chat_id: message.chat.id,
                bot_users.first_name: message.from_user.first_name,
                bot_users.last_name: message.from_user.last_name,
                bot_users.tg_username: message.from_user.username,
            }
        ).execute()

        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row("Да", "Нет")

        bot.send_message(
            message.chat.id, welcome.WELCOME_MESSAGE, reply_markup=keyboard
        )

    else:

        if cnt + 1 > CAPTCHA_TRYOUTS:
            bot.send_message(
                message.chat.id,
                captcha_messages.CAPTCHA_LIMIT,
            )
            _LOGGER.info(f"Captcha Limit by {message.from_user.id}")

            return False

        bot.send_message(message.chat.id, captcha_messages.CAPTCHA_BAD)

        return_message = bot.send_message(
            message.chat.id, captcha_messages.CAPTCHA_INFO
        )

        cnt += 1

        bot.register_next_step_handler(
            return_message, captcha_checker, captcha_txt, cnt
        )


def send_captcha(message: telebot.types.Message):
    captcha = get_captcha(5)
    bot.send_photo(message.chat.id, captcha[0])
    return_message = bot.send_message(message.chat.id, captcha_messages.CAPTCHA_INFO)
    bot.register_next_step_handler(return_message, captcha_checker, captcha[1])


@bot.message_handler(commands=["start"])
def send_welcome(message: telebot.types.Message) -> None:
    _LOGGER.info(f"Start by {message.from_user.id}")

    if bot_users.select().where(bot_users.telegram_id == message.from_user.id).exists():

        (
            bot_users.update(
                {
                    bot_users.first_name: message.from_user.first_name,
                    bot_users.last_name: message.from_user.last_name,
                    bot_users.tg_username: message.from_user.username,
                    bot_users.chat_id: message.chat.id,
                }
            )
            .where(bot_users.telegram_id == message.from_user.id)
            .execute()
        )

        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row("Да", "Нет")

        bot.send_message(
            message.chat.id,
            meetings_messages.WELCOME_MEETING,
            disable_web_page_preview=True,
            reply_markup=keyboard,
        )

    else:

        _LOGGER.info(f"Attempting to register {message.from_user.id}")
        bot.send_message(message.chat.id, "Давай зарегестрируем тебя.")

        send_captcha(message)


@bot.message_handler(commands=["help"])
def send_welcome(message: telebot.types.Message) -> None:
    pass


@bot.message_handler(func=lambda message: True)
def echo_message(message: telebot.types.Message) -> None:
    if bot_users.select().where(bot_users.telegram_id == message.from_user.id).exists():
        if message.text == "Да":

            bot_users.update({bot_users.status: "WAITING_FOR_MEETING"}).where(
                bot_users.telegram_id == message.from_user.id
            ).execute()

            bot.send_message(message.chat.id, "Мы сообщим тебе, когда подберём пару!")

            query = (
                bot_users.select()
                .where(
                    bot_users.status == "WAITING_FOR_MEETING"
                    and bot_users.telegram_id != message.from_user.id
                )
                .get()
            )

            if query:
                bot_users.update({bot_users.status: "MEETING_SCHEDULED"}).where(
                    bot_users.telegram_id == message.from_user.id
                ).execute()

                bot_users.update({bot_users.status: "MEETING_SCHEDULED"}).where(
                    bot_users.telegram_id == query.telegram_id
                ).execute()

                bot.send_message(
                    message.chat.id,
                    f"Ваш партнёр @{query.tg_username}",
                    reply_markup=telebot.types.ReplyKeyboardRemove(),
                )

                bot.send_message(
                    query.chat_id,
                    f"Ваш партнёр @{message.from_user.username},",
                    reply_markup=telebot.types.ReplyKeyboardRemove(),
                )

                meetings.insert(
                    {
                        meetings.telegram_id_1: message.from_user.id,
                        meetings.chat_id_1: message.from_user.id,
                        meetings.telegram_id_2: query.telegram_id,
                        meetings.chat_id_2: query.chat_id,
                        meetings.status: "SCHEDULED",
                    }
                ).execute()
            else:
                bot.send_message(
                    message.chat.id,
                    "Пока не удалось найти вам партнёра. Попробуйте попозже!",
                )

        if message.text == "Нет":
            bot.send_message(message.chat.id, "До встречи на следующей неделе!")

            bot_users.update({bot_users.status: "POSTPONED"}).where(
                bot_users.telegram_id == message.from_user.id
            ).execute()


bot.infinity_polling()
