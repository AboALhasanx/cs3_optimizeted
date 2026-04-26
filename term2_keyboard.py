from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from global_vars import (back_term2, term2_Table_of_lectures, networks2_lab_title, networks2_theo_title, compilers2_lab_title, compilers2_theo_title, dis_db_lab_title, dis_db_theo_title, data_enc_lab_title, data_enc_theo_title, data_mining_lab_title, data_mining_theo_title, web_prog_title)

def main_term_select():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("الكورس الاول")
    button2 = KeyboardButton("الكورس الثاني")
    button3 = KeyboardButton("تقييم البوت")
    button4 = KeyboardButton("🪧 عن البوت 🪧")
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    markup.add(button4)
    return markup

def main_term2_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button0 = KeyboardButton(term2_Table_of_lectures)
    button1 = KeyboardButton(networks2_lab_title)
    button2 = KeyboardButton(networks2_theo_title)
    button3 = KeyboardButton(data_mining_lab_title)
    button4 = KeyboardButton(data_mining_theo_title)
    button5 = KeyboardButton(dis_db_lab_title)
    button6 = KeyboardButton(dis_db_theo_title)
    button7 = KeyboardButton(data_enc_lab_title)
    button8 = KeyboardButton(data_enc_theo_title)
    button9 = KeyboardButton(compilers2_lab_title)
    button10 = KeyboardButton(compilers2_theo_title)
    button11 = KeyboardButton(web_prog_title)
    button12 = KeyboardButton("القائمة الرئيسية")
    markup.add(button0)
    markup.add(button1, button2)
    markup.add(button3, button4)
    markup.add(button5, button6)
    markup.add(button7, button8)
    markup.add(button9, button10)
    markup.add(button11)
    markup.add(button12)
    return markup

def give_rating():
    button_text = ["🎖🏆 واحد عراق 😶‍🌫✋🏻",
    "عاش يسطا 👀🔥",
    "الله على الروقان ✨😌",
    "جيد 👍🙂",
    "تحجي صدك 🦦؟",
    "خروج من التقييم"]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_text:
        button =KeyboardButton(text)
        markup.add(button)
    return markup

def webProgramming_buttons():
    button_texts = [
    "مادة السنة السابقة 🕐 🌐"
    , "الجابترات مترجمة + اسئلة وحلول 🇮🇶 🌐"
    , "البرنامج الي نطبق عليه Visual Studio Code 💻 🌐"
    , back_term2]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_texts:
        button =KeyboardButton(text)
        markup.add(button)
    return markup

def networks2_theo_buttons():
    button_texts = [
    "المحاضرات في ملف واحد كاملة 📁 📡"
    , "كل جابتر في ملف 🗂 📡"
    , "المحاضرات + الترجمة في ملف واحد كاملة 🇮🇶 📡"
    , "كل جابتر مترجم في ملف 🇮🇶 📡"
    , "ملخصات وتوضيحات 📝 📡"
    , "اسئلة وحلول 📝 📡"
    , "محاضرات السنة السابقة 🕐 📡"
    , back_term2]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_texts:
        button =KeyboardButton(text)
        markup.add(button)
    return markup

def networks2_lab_buttons():
    button_texts = [
    "المادة في ملف واحد كاملة 📁 📡"
    , "كل جابتر  بملف 🗂 📡"
    , "مادة السنة السابقة 🕐 📡"
    , "البرنامج الي نطبق عليه cisco packet tracer 💻 📡"
    , back_term2]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_texts:
        button =KeyboardButton(text)
        markup.add(button)
    return markup

def data_mining_theo_buttons():
    button_texts = [
    "المحاضرات في ملف واحد كاملة 📁 ⚒"
    , "كل جابتر  في ملف 🗂 ⚒"
    , "المحاضرات + الترجمة في ملف واحد كاملة 🇮🇶 ⚒"
    , "كل جابتر مترجم في ملف 🇮🇶 ⚒"
    , "ملخصات وتوضيحات 📝 ⚒"
    , "محاضرات السنة السابقة 🕐 ⚒"
    , back_term2]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_texts:
        button =KeyboardButton(text)
        markup.add(button)
    return markup

def data_mining_lab_buttons():
    button_texts = [
    "المادة في ملف واحد كاملة 📁 ⚒ "
    , "كل جابتر  بملف 🗂 ⚒"
    , "ملخصات و توضيحات 📝 ⚒"
    , "البرنامج الي نطبق عليه Jupyter 💻 ⚒"
    , "مادة السنة السابقة 🕐 ⚒"
    , back_term2]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_texts:
        button =KeyboardButton(text)
        markup.add(button)
    return markup

def distributed_databases_theo_buttons():
    button_texts = [
    "المحاضرات في ملف واحد كاملة 📁 🛢"
    , "كل جابتر  في ملف 🗂 🛢"
    , "كل جابتر مترجم في ملف 🇮🇶 🛢"
    , "ملخصات وتوضيحات 📝 🛢"
    , "محاضرات السنة السابقة 🕐 🛢"
    , back_term2]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_texts:
        button =KeyboardButton(text)
        markup.add(button)
    return markup

def distributed_databases_lab_buttons():
    button_texts = [
    "المادة في ملف واحد كاملة 📁 🛢"
    , "كل جابتر  بملف 🗂 🛢"
    , "البرنامج الي نطبق عليه Visual Studio 2010 💻 🛢"
    , "مادة السنة السابقة 🕐 🛢"
    , back_term2]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_texts:
        button =KeyboardButton(text)
        markup.add(button)
    return markup

def data_encryption_theo_buttons():
    button_texts = [
    "المحاضرات في ملف واحد كاملة 📁 🔐"
    , "كل جابتر في ملف 🗂 🔐"
    , "المحاضرات + الترجمة في ملف واحد كاملة 🇮🇶 🔐"
    , "كل جابتر مترجم في ملف 🇮🇶 🔐"
    , "ملخصات وتوضيحات 📝 🔐"
    , "اسئلة وحلول 📝 🔐"
    , "محاضرات السنة السابقة 🕐 🔐"
    , back_term2]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_texts:
        button =KeyboardButton(text)
        markup.add(button)
    return markup

def data_encryption_lab_buttons():
    button_texts = [
    "المادة في ملف واحد كاملة 📁 🔐"
    , "كل جابتر  بملف 🗂 🔐"
    , "البرنامج الي نطبق عليه Jupyter 💻 🔐"
    , "مادة السنة السابقة 🕐 🔐"
    , back_term2]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_texts:
        button =KeyboardButton(text)
        markup.add(button)
    return markup

def compilers2_theo_buttons():
    button_texts = [
    "المحاضرات في ملف واحد كاملة 📁 📟"
    , "اسئلة وحلول + ملخصات وتوضيحات 📝 📟"
    , "محاضرات السنة السابقة 🕐 📟"
    , back_term2]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_texts:
        button =KeyboardButton(text)
        markup.add(button)
    return markup

def compilers2_lab_buttons():
    button_texts = [
    "المادة في ملف واحد كاملة 📁 📟"
    , "كل جابتر  بملف 🗂 📟"
    , "البرنامج الي نطبق عليه Dev C++ 💻 📟"
    , "مادة السنة السابقة 🕐 📟"
    , back_term2]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_texts:
        button =KeyboardButton(text)
        markup.add(button)
    return markup