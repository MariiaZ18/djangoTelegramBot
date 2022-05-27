import os
import emoji
from django.db.backends import mysql
from telegram.ext import *
from telegram import *
from dotenv import load_dotenv
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from ugc.models import *

load_dotenv()

with open('info.txt', 'r', encoding="utf-8") as f:
    bot_info = f.read()

buttons = [[KeyboardButton("Додати файл ➕")], [ KeyboardButton("Переглянути завантажені файли 📂")],[KeyboardButton("Інфо 📃")]]
info_butt = [[KeyboardButton("Повернутися назад 🔙")]]
def markup_inline():
    m_l = []
    for x in University.objects.all():
        k = InlineKeyboardButton(text=f'{x.name} 🏢', callback_data=f"choose_university:{x.id}")
        m_l.append([k])
    return m_l
markup_university = InlineKeyboardMarkup(markup_inline())

def markup_inline_for_adding_files():
    markup_for_choose_uni_to_add_file = []
    for x in University.objects.all():
        k = InlineKeyboardButton(text=f'{x.name}  🏢', callback_data=f"choose_univ_file:{x.id}")
        markup_for_choose_uni_to_add_file.append([k])
    return markup_for_choose_uni_to_add_file
markup_university_to_add_file = InlineKeyboardMarkup(markup_inline_for_adding_files())

def start(update, context):
    context.bot.send_sticker(chat_id=update.message.chat_id,
                        sticker='CAACAgIAAxkBAAEE1Dxij-FcvGjthG8Njz_DOutCkyTTrwACBQADwDZPE_lqX5qCa011JAQ')
    mes = f"<code>Привіт, {update.message.from_user.first_name} {update.message.from_user.last_name}.\nБудь ласка, вибери що ти хочеш зробити.</code>"
    context.bot.send_message(chat_id=update.effective_chat.id, text=mes,parse_mode='html',reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True))

def mess_handler(update, context):
    if update.message.text == "Інфо 📃":
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode='html',text=f'<code>{bot_info}</code>',reply_markup=ReplyKeyboardMarkup(info_butt, resize_keyboard=True, one_time_keyboard=True))
    elif update.message.text == "Повернутися назад 🔙":
        context.bot.send_message(chat_id=update.effective_chat.id,parse_mode='html',text = "<code>Будь ласка, вибери що ти хочеш зробити.</code>", reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True,row_width=1, one_time_keyboard=True))
    elif update.message.text == "Переглянути завантажені файли 📂":
        context.bot.send_message(chat_id=update.effective_chat.id,parse_mode='html', text="<code>Вибери університет</code>",reply_markup=markup_university)
    elif update.message.text == "Додати файл ➕":
        context.bot.send_message(chat_id=update.effective_chat.id,parse_mode='html', text="<code>Вибери куди ти хочеш завантажити файл</code>",reply_markup=markup_university_to_add_file)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,parse_mode='html',text="<code>Вибач, але я тебе не розумію, спробуй ще раз</code>")

def downloader(update, context):
    file_n = update.message.document.file_name
    if context.user_data.get('sub_id'):
        sub_id = context.user_data['sub_id']
        file = context.bot.getFile(update.message.document.file_id)
        file.download(file_n)
        new_file = Files(name=f"{file_n}", upload=f"{file_n}", subject_id=sub_id)
        new_file.save()
        context.bot.send_message(chat_id=update.effective_chat.id,parse_mode='html', text="<code>Твій файл було успішно додано</code>")


def all_callback(update, context):
    query = update.callback_query
    query.answer()
    if 'choose_university' in query.data:
        university_id = query.data.split(':')[-1]
        context.bot.send_message(chat_id=update.effective_chat.id,
                                text="<code>Виберіть кафедру</code>",parse_mode="html",
                                reply_markup=InlineKeyboardMarkup([list(
                                    InlineKeyboardButton(text=k.name, callback_data=f"choose_katedra:{k.id}")
                                    for k in Katedra.objects.filter(university_id=university_id))]))
    if "choose_katedra" in query.data:
        katedra__id = query.data.split(':')[-1]
        context.bot.send_message(chat_id=update.effective_chat.id,
                                text="<code>Виберіть предмет</code>",parse_mode='html',
                                reply_markup=InlineKeyboardMarkup([list(
                                    InlineKeyboardButton(text=f'{s.name} 📚', callback_data=f"choose_subject:{s.id}")
                                    for s in Subject.objects.filter(katedra_id=katedra__id))]))
    if "choose_subject" in query.data:
        subject_id = query.data.split(':')[-1]
        context.bot.send_message(chat_id=update.effective_chat.id,
                                text="<code>Ось список всіх завантажених файлів по даному предмету, вибери файл, який хочеш завантажити</code>",
                                parse_mode='html',
                                reply_markup=InlineKeyboardMarkup([list(
                                InlineKeyboardButton(text=str(f.upload), callback_data=f"choose_file:{f.id}")
                                for f in Files.objects.filter(subject_id=subject_id))]))
    if "choose_file" in query.data:
        file_id = query.data.split(':')[-1]
        file_name = [str(i.upload) for i in Files.objects.filter(id=file_id)]
        file_name=file_name[0]
        sending_file = open(f'{file_name}', 'rb')
        context.bot.send_document(chat_id=update.effective_chat.id, document=sending_file)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                parse_mode='html',
                                text="<code>⬆ Ocь твій файл ⬆</code>", reply_markup=ReplyKeyboardMarkup(info_butt, resize_keyboard=True, one_time_keyboard=True))
    if "choose_univ_file" in query.data:
        kat_id = query.data.split(':')[-1]
        context.bot.send_message(chat_id=update.effective_chat.id,
                                text="<code>Вибери кафедру</code>",
                                parse_mode='html',
                                reply_markup=InlineKeyboardMarkup([list(
                                    InlineKeyboardButton(text=str(ka.name), callback_data=f"choose_kat_file:{ka.id}")
                                    for ka in Katedra.objects.filter(university_id=kat_id))]))
    if "choose_kat_file" in query.data:
        katedra__id = query.data.split(':')[-1]
        context.bot.send_message(chat_id=update.effective_chat.id,
                                text="<code>Виберіть предмет</code>",
                                parse_mode='html',
                                reply_markup=InlineKeyboardMarkup([list(
                                    InlineKeyboardButton(text=f'{s.name} 📚', callback_data=f"choose_sub_file:{s.id}")
                                    for s in Subject.objects.filter(katedra_id=katedra__id))]))
    if "choose_sub_file" in query.data:
        sub_id = query.data.split(':')[-1]
        context.bot.send_message(chat_id=update.effective_chat.id,
                                parse_mode='html',
                                text="<code>Відправ файл у чат</code>")
        context.user_data['sub_id']=sub_id









