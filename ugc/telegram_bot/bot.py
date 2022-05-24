import os
from telegram.ext import *
from telegram import *
from dotenv import load_dotenv
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from ugc.models import *

load_dotenv()

with open('info.txt', 'r', encoding="utf-8") as f:
    bot_info = f.read()


buttons = [[KeyboardButton("Додати файл")], [ KeyboardButton("Переглянути вже існуючі")],[KeyboardButton("Інфо")],[KeyboardButton("Повернутися назад")]]
info_butt = [[KeyboardButton("Повернутися назад")]]
add_file = [[InlineKeyboardButton("Ввійти",callback_data="login")]]

def markup_inline():
    m_l = []
    for x in University.objects.all():
        k = InlineKeyboardButton(text=x.name, callback_data=f"choose_university:{x.id}")
        m_l.append([k])
    return m_l
markup_university = InlineKeyboardMarkup(markup_inline())

def start(update, context):
    mes = f"Привіт, {update.message.from_user.first_name} {update.message.from_user.last_name}.\nБудь ласка, вибери що ти хочеш зробити."
    context.bot.send_message(chat_id=update.effective_chat.id, text=mes,reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True))

def mess_handler(update, context):
    if update.message.text == "Інфо":
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_info,reply_markup=ReplyKeyboardMarkup(info_butt, resize_keyboard=True, one_time_keyboard=True))
    elif update.message.text == "Повернутися назад":
        context.bot.send_message(chat_id=update.effective_chat.id,text = "Будь ласка, вибери що ти хочеш зробити.", reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True,row_width=1, one_time_keyboard=True))
    elif update.message.text == "Переглянути вже існуючі":
        context.bot.send_message(chat_id=update.effective_chat.id, text="Вибери університет",reply_markup=markup_university)
    elif update.message.text == "Додати файл":
        context.bot.send_message(chat_id=update.effective_chat.id, text="Для того щоб завантажити новий файл спочатку потрібно ввійти в свій обліковий запис",reply_markup=InlineKeyboardMarkup(add_file))

def all_callback(update, context):
    query = update.callback_query
    query.answer()
    if 'choose_university' in query.data:
        university_id = query.data.split(':')[-1]
        context.bot.send_message(chat_id=update.effective_chat.id,
                                text="Виберіть кафедру",
                                reply_markup=InlineKeyboardMarkup([list(InlineKeyboardButton(text=k.name, callback_data=f"choose_katedra:{k.id}") for k in Katedra.objects.filter(university_id=university_id))]))

    if "choose_katedra" in query.data:
        katedra_id = query.data.split(':')[-1]
        context.bot.send_message(chat_id=update.effective_chat.id,
                                text="Виберіть предмет",
                                reply_markup=InlineKeyboardMarkup([list(InlineKeyboardButton(text=s.name, callback_data=f"choose_subject{s.id}") for s in Subject.objects.filter(katedra_id=katedra_id))]))














    # if query.data == "login":
    #     context.bot.send_message(chat_id=update.effective_chat.id, text='Введіть свій username')


# def call_back_sub(update, context):
#     query = update.callback_query
#     sub_but = []
#     for s in get_subject_from_db():
#         if query.data == str(s.id):
#             s = InlineKeyboardButton(text=s.name, callback_data=s.id)
#             sub_but.append([s])
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Виберіть предмет", reply_markup=InlineKeyboardMarkup(sub_but))
#
# def callback_login(update, context):
#     query = update.callback_query

# def call_back_univer(update, context):
#     query = update.callback_query
#     list_of_kated_but = []
#     sub_but = []
#     if query.data in [str(k.university_id) for k in get_katedra_from_db()]:
#         for k in get_katedra_from_db():
#             l = InlineKeyboardButton(text=k.name, callback_data=k.id)
#             list_of_kated_but.append([l])
#         context.bot.send_message(chat_id=update.effective_chat.id, text="Виберіть кафедру", reply_markup=InlineKeyboardMarkup(list_of_kated_but))
#     if query.data in [str(s.id) for s in get_subject_from_db()]:
#         for s in get_subject_from_db():
#             s = InlineKeyboardButton(text=s.name, callback_data=s.id)
#             sub_but.append([s])
#         context.bot.send_message(chat_id=update.effective_chat.id, text="Виберіть предмет", reply_markup=InlineKeyboardMarkup(sub_but))
