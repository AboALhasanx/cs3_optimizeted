from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from global_vars import (back_term1,term1_Table_of_lectures, networks1_lab_title, networks1_theo_title, ai_lab_title, ai_theo_title, multimedia_lab_title, multimedia_theo_title, software_engineering_lab_title, software_engineering_theo_title, compilers1_lab_title, compilers1_theo_title, english_title, operations_research_title )

def main_term1_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button0 = KeyboardButton(term1_Table_of_lectures)
    button1 = KeyboardButton(networks1_lab_title)
    button2 = KeyboardButton(networks1_theo_title)
    button3 = KeyboardButton(ai_lab_title)
    button4 = KeyboardButton(ai_theo_title)
    button5 = KeyboardButton(multimedia_lab_title)
    button6 = KeyboardButton(multimedia_theo_title)
    button7 = KeyboardButton(software_engineering_lab_title)
    button8 = KeyboardButton(software_engineering_theo_title)
    button9 = KeyboardButton(compilers1_lab_title)
    button10 = KeyboardButton(compilers1_theo_title)
    button11 = KeyboardButton(english_title)
    button12 = KeyboardButton(operations_research_title)
    button13 = KeyboardButton("القائمة الرئيسية") 
    markup.add(button0)  
    markup.add(button1, button2)
    markup.add(button3, button4)
    markup.add(button5, button6)
    markup.add(button7, button8)
    markup.add(button9, button10)
    markup.add(button11)
    markup.add(button12)
    markup.add(button13)
    return markup


def ai_lab_buttons():
    button_text = [
    "المادة في ملف واحد كاملة 📁🤖"
    , "كل جابتر بملف 🗂 🤖"
    , "ملخصات و توضيحات 📝 🤖"
    , "مادة السنة السابقة 🕐 🤖"
    , "البرنامج الي نطبق عليه Jupyter 💻 🤖"
    , back_term1]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_text:
        button =KeyboardButton(text)
        markup.add(button)
    return markup

def ai_theo_buttons():
    button_text = [
    "المحاضرات في ملف واحد كاملة 📁 🤖"
    , "كل جابتر في ملف 🗂 🤖"
    , "المحاضرات + الترجمة في ملف واحد كاملة 🇮🇶 🤖"
    , "ملخصات وتوضيحات 📝 🤖"
    , "اسئلة وحلول 📝 🤖"
    , "محاضرات السنة السابقة 🕐 🤖"
    , back_term1]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_text:
        button =KeyboardButton(text)
        markup.add(button)
    return markup

def software_eng_lab_buttons():
    button_text = [
        "المادة في ملف واحد كاملة 📁📐"
        , "كل جابتر  بملف 🗂 📐"
        , "ملخصات وتوضيحات 📝 📐"
        , "مادة السنة السابقة 🕐 📐"
        , "البرنامج الي نطبق عليه Jupyter 💻 📐"
        , back_term1]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_text:
        button =KeyboardButton(text)
        markup.add(button)
    return markup

def software_eng_theo_buttons():
    button_text = [
    "المحاضرات في ملف واحد كاملة 📁 📐"
    , "كل جابتر في ملف 🗂 📐"
    , "المحاضرات + الترجمة في ملف واحد كاملة 🇮🇶 📐"
    , "كل جابتر مترجم في ملف 🇮🇶 📐"
    , "ملخصات و توضيحات 📝 📐"
    , "اسئلة وحلول 📝 📐"
    , "محاضرات السنة السابقة 🕐 📐"
    , back_term1]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_text:
        button =KeyboardButton(text)
        markup.add(button)
    return markup

def multimedia_lab_buttons():
    button_text = [
    "المادة في ملف واحد كاملة 📁🖼️"
    , "مادة السنة السابقة 🕐 🖼️"
    , "البرامج الي نطبق عليها 💻 🖼️"
    , back_term1]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_text:
        button =KeyboardButton(text)
        markup.add(button)
    return markup

def multimedia_theo_buttons():
    button_text = [
    "المحاضرات في ملف واحد كاملة 📁 🖼️"
    , "كل جابتر في ملف 🗂 🖼️"
    , "ملخصات وتوضيحات 📝 🖼️"
    , "اسئلة وحلول 📝 🖼️"
    , "محاضرات السنة السابقة 🕐 🖼️"
    , back_term1]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_text:
        button =KeyboardButton(text)
        markup.add(button)
    return markup

def networks1_lab_buttons():
    button_text = [
        "المادة في ملف واحد كاملة 📁🔌"
        , "كل جابتر  بملف 🗂 🔌"
        , "مادة السنة السابقة 🕐 🔌"
        , "البرنامج الي نطبق عليه Cisco Packet Tracer 💻 🔌" 
        , back_term1]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_text:
        button =KeyboardButton(text)
        markup.add(button)
    return markup

def networks1_theo_buttons():
    button_text = [
        "المحاضرات في ملف واحد كاملة 📁 🔌"
        , "كل جابتر في ملف 🗂 🔌"
        , "المحاضرات + الترجمة في ملف واحد كاملة 🇮🇶 🔌"
        , "كل جابتر مترجم في ملف 🇮🇶 🔌"
        , "ملخصات وتوضيحات 📝 🔌"
        , "اسئلة وحلول 📝 🔌"
        , "محاضرات السنة السابقة 🕐 🔌"
        , back_term1]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_text:
        button =KeyboardButton(text)
        markup.add(button)
    return markup

def compilers1_lab_buttons():
    button_text = [
        "المادة في ملف واحد كاملة 📁🧮"
        , "كل جابتر  بملف 🗂 🧮"
        , "مادة السنة السابقة 🕐 🧮"
        , "البرنامج الي نطبق عليه Visual Studio 2010 💻 🧮"
        , back_term1]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_text:
        button =KeyboardButton(text)
        markup.add(button)
    return markup

def compilers1_theo_buttons():
    button_text = [
        "المحاضرات في ملف واحد كاملة 📁 🧮"
        , "كل جابتر في ملف 🗂 🧮"
        , "كل جابتر مترجم في ملف 🇮🇶 🧮"
        , "ملخصات وتوضيحات 📝 🧮"
        , "محاضرات السنة السابقة 🕐 🧮" 
        , back_term1]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_text:
        button =KeyboardButton(text)
        markup.add(button)
    return markup

def english_buttons():
    button_text = [
        "المحاضرات في ملف واحد كاملة 📁 🇬🇧"
        , "كل يونت في ملف 🗂 🇬🇧"
        , "حلول كل يونت  في ملف 🇬🇧"
        , "محاضرات السنة السابقة 🕐 🇬🇧" 
        , back_term1]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_text:
        button =KeyboardButton(text)
        markup.add(button)
    return markup

def operation_research_buttons():
    button_text = [
        "المحاضرات في ملف واحد كاملة 📁 🔎"
        , "اسئلة وحلول 📝 🔎"
        , "محاضرات السنة السابقة 🕐 🔎" 
        , back_term1]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for text in button_text:
        button =KeyboardButton(text)
        markup.add(button)
    return markup