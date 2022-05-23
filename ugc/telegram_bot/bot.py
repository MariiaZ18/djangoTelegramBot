import os
from telegram.ext import *
from telegram import *
from dotenv import load_dotenv
from telegram import InlineKeyboardMarkup

load_dotenv()
with open('info.txt', 'r', encoding="utf-8") as f:
    bot_info = f.read()

def university_data(requests):
    university_names = University.objects.all()
    return university_names


buttons = [[KeyboardButton("Додати файл")], [ KeyboardButton("Переглянути вже існуючі")],[KeyboardButton("Інфо")],[KeyboardButton("Повернутися назад")]]
info_butt = [[KeyboardButton("Повернутися назад")]]

# markup_university = InlineKeyboardMarkup()
#
# for x in university_data():
#     markup_university.add(InlineKeyboardButton(x[0]))


def start(update, context):
    mes = f"Привіт, {update.message.from_user.first_name} {update.message.from_user.last_name}.\nБудь ласка, вибери що ти хочеш зробити."
    context.bot.send_message(chat_id=update.effective_chat.id, text=mes,reply_markup=ReplyKeyboardMarkup(buttons,resize_keyboard=True,one_time_keyboard=True))


def mess_handler(update, context):
    if update.message.text == "Інфо":
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_info,reply_markup=ReplyKeyboardMarkup(info_butt,resize_keyboard=True, one_time_keyboard=True))
    elif update.message.text == "Повернутися назад":
        context.bot.send_message(chat_id=update.effective_chat.id,text = "Будь ласка, вибери що ти хочеш зробити.", reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True,row_width=1, one_time_keyboard=True))
    elif update.message.text == "Переглянути вже існуючі":
        context.bot.send_message(chat_id=update.effective_chat.id,text="Вибери університет",reply_markup=InlineKeyboardMarkup(markup_university))


if __name__ == '__main__':
    updater = Updater(os.getenv("TELEGRAM_SECRET"), use_context=True)
    disp = updater.dispatcher
    disp.add_handler(CommandHandler("start", start))
    disp.add_handler(MessageHandler(Filters.text, mess_handler))
    updater.start_polling()
    updater.idle()
