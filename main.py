import telebot
import random
import requests
from telebot import apihelper

# =========[ استيراد البيانات من الملفات الأخرى ]=========
from config import (
    ADMIN_ID,
    BOT_TOKEN,
    LOG_CHANNEL_ID,
    TELEGRAM_PROXY_URL,
    cs_stg3,
    cs_stg3_onefile,
    cs_stg3_deleted,
    cs_apps
)

if TELEGRAM_PROXY_URL:
    apihelper.proxy = {"https": TELEGRAM_PROXY_URL}

from global_vars import (
    about_bot_msg,
    back_term1,
    chose_from,
    networks1_lab_title,
    networks1_theo_title,
    ai_lab_title,
    ai_theo_title,
    software_engineering_lab_title,
    software_engineering_theo_title,
    multimedia_lab_title,
    multimedia_theo_title,
    compilers1_lab_title,
    compilers1_theo_title,
    english_title,
    operations_research_title,
    back_term2,
    networks2_lab_title,
    networks2_theo_title,
    data_enc_lab_title,
    data_enc_theo_title,
    data_mining_lab_title,
    data_mining_theo_title,
    dis_db_lab_title,
    dis_db_theo_title,
    compilers2_lab_title,
    compilers2_theo_title,
    web_prog_title
)

from term1_keyboard import (
    main_term1_keyboard,
    ai_lab_buttons,
    ai_theo_buttons,
    software_eng_lab_buttons,
    software_eng_theo_buttons,
    multimedia_lab_buttons,
    multimedia_theo_buttons,
    networks1_lab_buttons,
    networks1_theo_buttons,
    compilers1_lab_buttons,
    compilers1_theo_buttons,
    operation_research_buttons,
    english_buttons
)

from term2_keyboard import (
    give_rating,
    main_term2_keyboard,
    main_term_select,
    webProgramming_buttons,
    networks2_lab_buttons,
    networks2_theo_buttons,
    data_mining_lab_buttons,
    data_mining_theo_buttons,
    distributed_databases_lab_buttons,
    distributed_databases_theo_buttons,
    data_encryption_lab_buttons,
    data_encryption_theo_buttons,
    compilers2_lab_buttons,
    compilers2_theo_buttons
)

from services.content_registry import ContentRegistry


# =========[ تهيئة البوت ]=========
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)
content_registry = ContentRegistry()



# ========== تسجيل بيانات المستخدمين ==========
FIREBASE_URL = "https://csbotproject-60ec6-default-rtdb.firebaseio.com/"

def log_user(message):
    user_id = str(message.from_user.id)
    current_data = {
        "id": user_id,
        "first_name": message.from_user.first_name or "NoName",
        "username": f"@{message.from_user.username}" if message.from_user.username else "NoUsername"
    }

    try:
        response = requests.get(f"{FIREBASE_URL}/users/{user_id}.json")
        if response.status_code == 200:
            existing_data = response.json()
            if not existing_data:
                requests.put(f"{FIREBASE_URL}/users/{user_id}.json", json=current_data)
                bot.send_message(ADMIN_ID, f"🆕 مستخدم جديد:\nID: {user_id}\nUsername: {current_data['username']}")
            else:
                if existing_data.get("first_name") != current_data["first_name"] or \
                  existing_data.get("username") != current_data["username"]:
                    requests.put(f"{FIREBASE_URL}/users/{user_id}.json", json=current_data)
                    bot.send_message(ADMIN_ID, f"🔄 تم تحديث بيانات:\nID: {user_id}\nUsername: {current_data['username']}")
    except Exception as e:
        print(f"خطأ في Firebase: {e}")


def load_users(): # type: ignore
    try:
        response = requests.get(f"{FIREBASE_URL}/users.json")
        if response.status_code == 200:
            return response.json() or {}
    except Exception as e:
        print(f"خطأ في جلب المستخدمين: {e}")
    return {}



# ========== أوامر الإذاعة =============

def deactivate_user(uid):
    """
    تقوم هذه الدالة بتحديث حالة المستخدم في قاعدة البيانات
    لتعتبره غير نشط (active=False) في حال لم يستجب للبوت (مثل حالة Forbidden).
    """
    try:
        url = f"{FIREBASE_URL}/users/{uid}.json"
        # نستخدم patch لتحديث الحقل active فقط
        response = requests.patch(url, json={"active": False})
        if response.status_code == 200:
            print(f"تم تحديث حالة المستخدم {uid} إلى غير نشط.")
        else:
            print(f"فشل تحديث حالة المستخدم {uid}: {response.status_code}")
    except Exception as ex:
        print(f"حدث خطأ أثناء تحديث حالة المستخدم {uid}: {ex}")

@bot.message_handler(commands=['bro'])
def broadcast(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, "🚫 فقط الأدمن يمكنه استخدام هذا الأمر.")
        return

    if not message.reply_to_message:
        bot.reply_to(message, "❗ استخدم الأمر بالرد على الرسالة المراد إرسالها.")
        return

    original = message.reply_to_message
    users = load_users()

    count = 0
    for uid, info in users.items():
        if info.get("banned"):
            continue  # تجاهل المستخدمين المحظورين
        try:
            # محاولة إرسال الرسالة باستخدام copy_message
            bot.copy_message(
                chat_id=int(uid),
                from_chat_id=original.chat.id,
                message_id=original.message_id
            )
            count += 1
        except Exception as e:
            error_message = str(e)
            print(f"فشل الإرسال إلى {uid}: {error_message}")
            # إذا كان الخطأ يتعلق بأن البوت غير قادر على إرسال رسالة (مثل Forbidden)
            if "Forbidden" in error_message:
                deactivate_user(uid)

    bot.reply_to(message, f"✅ تم إرسال البرودكاست إلى {count} مستخدم.")



# =========[ التحقق من عضوية المستخدم في القنوات ]=========
def is_user_member(user_id, chat_id):
    try:
        chat_member = bot.get_chat_member(chat_id, user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False


def check_and_respond(message, response_function, *args):
    """
    دالة وسيطة تتأكد من اشتراك المستخدم في القنوات المطلوبة
    قبل تنفيذ الدالة response_function.
    """
    user = message.from_user
    first_name = user.first_name
    user_id = user.id
    required_channels = ["@cs_stg3"]

    all_membership_valid = all(is_user_member(user_id, channel) for channel in required_channels)

    if all_membership_valid:
        response_function(message, *args)
    else:
        bot.send_message(
            message.chat.id,
            f"⤦ اوكف {first_name} شو ما مشترك بالقناة ⁉️🫣\n"
            "اشترك وارجع اضغط على /start\n"
            "• قناة الملازم: @cs_stg3"
        )


# =========[ أوامر البوت الأساسية ]=========
@bot.message_handler(commands=['start'])
def send_welcome(message):
    log_and_forward(message)
    """
    الأمر /start:
    - يسجل المستخدم في ملف JSON (log_user)
    - يرسل رسالة ترحيبية فيها قائمة المواد.
    """
    log_user(message)  # ← يتم الحفظ هنا فقط
    def respond(msg):
        welcome_text = (
            "<b>• شلونهم ابطالنا 🦾\n\n"
            "• اختار من القائمة المادة 🎛⚡️\n\n"
            "<blockquote>👨🏻‍💻المطور : @ab0_alhasan</blockquote>\n\n"
            "<blockquote>💻 قناة المشاريع البرمجية : @CodeLabIQ</blockquote></b>"
        )
        bot.reply_to(msg, welcome_text, parse_mode='HTML', reply_markup=main_term_select())


    # إذا كان المستخدم مشتركا بكل القنوات، يعرض له القوائم
    check_and_respond(message, respond)


@bot.message_handler(commands=['about'])
@bot.message_handler(func=lambda message: message.text == "🪧 عن البوت 🪧")
def about_bot(message):
    log_and_forward(message)
    bot.reply_to(message, about_bot_msg, parse_mode='HTML')


def chose_from_markup(message, reply_markup):
    bot.reply_to(message, chose_from, reply_markup=reply_markup)


# =========[ تقييم البوت ]=========
@bot.message_handler(func=lambda message: message.text == "تقييم البوت")
def open_rating_menu(message):
    log_and_forward(message)
    def respond(msg):
        bot.reply_to(msg, chose_from, reply_markup=give_rating())
    check_and_respond(message, respond)


@bot.message_handler(commands=['rating'])
def open_rating_menu_cmd(message):
    log_and_forward(message)
    def respond(msg):
        bot.reply_to(msg, chose_from, reply_markup=give_rating())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda message: message.text in [
    "🎖🏆 واحد عراق 😶‍🌫✋🏻",
    "عاش يسطا 👀🔥",
    "الله على الروقان ✨",
    "جيد 👍🙂",
    "تحجي صدك 🦦؟"
])
def handle_rating(message):
    rating = message.text
    good_response = ["حبيب اخوك 😇", "حبيبي نورتني ", "صدك جذب تدلل 😊"]
    veryGood_response = [
        "اخويا ياسطا 😎🤙🏻", "تسلم يالقالي 😴🫶", "نورك هذا لو الشمس؟ عمي منورنا 😔❤️‍🔥",
        "يا هلا وغلا بالعزيز 🫂❤️‍🔥", "شهادة اعتزُ بيها 🤝🏻", "هاي الوردة تستاهلك 🌹🫴"
    ]
    ok_response = ["خوش 🤨", "تمام 🙄", "ماشي 🙃", "اوك 🌚", "شوكران يمحترم 😒", "مثل تقديرك 🫠"]

    if rating == "تحجي صدك 🦦؟":
        response_text = "هاي ليش 💔🗿؟ \nراسلني وكلي اذا اكو مشكلة بالبوت @ab0_alhasan"
    elif rating == "الله على الروقان ✨":
        response_text = random.choice(good_response)
    elif rating == "جيد 👍🙂":
        response_text = random.choice(ok_response)
    else:
        response_text = random.choice(veryGood_response)

    bot.send_message(message.chat.id, response_text, reply_markup=main_term_select())


# =========[ الكورس الأول ]=========
@bot.message_handler(commands=['term1'])
def cmd_term1(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, main_term1_keyboard())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda message: message.text == "الكورس الاول")
def to_term1_menu(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, main_term1_keyboard())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == ai_lab_title)
def ai_lab_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, ai_lab_buttons())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == ai_theo_title)
def ai_theo_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, ai_theo_buttons())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == software_engineering_lab_title)
def sEng_lab_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, software_eng_lab_buttons())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == software_engineering_theo_title)
def sEng_theo_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, software_eng_theo_buttons())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == multimedia_lab_title)
def mm_lab_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, multimedia_lab_buttons())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == multimedia_theo_title)
def mm_theo_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, multimedia_theo_buttons())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == networks1_lab_title)
def net1_lab_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, networks1_lab_buttons())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == networks1_theo_title)
def net1_theo_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, networks1_theo_buttons())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == compilers1_lab_title)
def comp1_lab_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, compilers1_lab_buttons())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == compilers1_theo_title)
def comp1_theo_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, compilers1_theo_buttons())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == english_title)
def english_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, english_buttons())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == operations_research_title)
def operations_research_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, operation_research_buttons())
    check_and_respond(message, respond)


# =========[ الكورس الثاني ]=========
@bot.message_handler(commands=['term2'])
def cmd_term2(message):
    log_and_forward(message)
    def respond(msg):
        bot.reply_to(msg, chose_from, reply_markup=main_term2_keyboard())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == "الكورس الثاني")
def to_term2_menu(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, main_term2_keyboard())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == web_prog_title)
def web_prog_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, webProgramming_buttons())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == compilers2_lab_title)
def comp2_lab_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, compilers2_lab_buttons())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == compilers2_theo_title)
def comp2_theo_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, compilers2_theo_buttons())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == networks2_lab_title)
def net2_lab_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, networks2_lab_buttons())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == networks2_theo_title)
def net2_theo_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, networks2_theo_buttons())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == dis_db_lab_title)
def dist_db_lab_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, distributed_databases_lab_buttons())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == dis_db_theo_title)
def dist_db_theo_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, distributed_databases_theo_buttons())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == data_enc_lab_title)
def data_enc_lab_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, data_encryption_lab_buttons())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == data_enc_theo_title)
def data_enc_theo_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, data_encryption_theo_buttons())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == data_mining_lab_title)
def data_mining_lab_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, data_mining_lab_buttons())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == data_mining_theo_title)
def data_mining_theo_redirect(message):
    log_and_forward(message)
    def respond(msg):
        chose_from_markup(msg, data_mining_theo_buttons())
    check_and_respond(message, respond)


# =========[ أزرار الرجوع و الرئيسية ]=========
@bot.message_handler(func=lambda msg: msg.text == back_term1)
def return_to_term1_menu(message):
    log_and_forward(message)
    def respond(msg):
        bot.reply_to(msg, chose_from, reply_markup=main_term1_keyboard())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text == back_term2)
def return_to_term2_menu(message):
    log_and_forward(message)
    def respond(msg):
        bot.reply_to(msg, chose_from, reply_markup=main_term2_keyboard())
    check_and_respond(message, respond)


@bot.message_handler(func=lambda msg: msg.text in ["القائمة الرئيسية", "خروج من التقييم"])
def return_to_main_menu(message):
    log_and_forward(message)
    def respond(msg):
        bot.reply_to(msg, "القائمة الرئيسية", reply_markup=main_term_select())
    check_and_respond(message, respond)


# =========[ التعامل مع الأزرار التي لها أوامر جاهزة ]=========

@bot.message_handler(func=lambda msg: content_registry.get_command_for_button(msg.text) is not None)
def handle_button(message):
    log_and_forward(message)
    command = content_registry.get_command_for_button(message.text)
    get_file_command(message, command)


def get_file_command(message, command):
    content = content_registry.get_content_for_command(command)
    if content is None:
        bot.reply_to(message, "⏳ماكو حاليا هذا الملف")
        return

    channel_key = content.get("channel_key")
    channel_map = {
        "cs_stg3": cs_stg3,
        "cs_stg3_onefile": cs_stg3_onefile,
        "cs_stg3_deleted": cs_stg3_deleted,
        "cs_apps": cs_apps,
    }
    CHANNEL_ID = channel_map.get(channel_key)

    if CHANNEL_ID is None:
        bot.reply_to(message, "⏳ماكو حاليا هذا الملف")
        return

    message_ids = content.get("message_ids", [])
    if not message_ids:
        bot.reply_to(message, "⏳ماكو حاليا هذا الملف")
        return

    message_text = "⬆️⬆️🫡"
    try:
        for post_id in message_ids:
            bot.forward_message(message.chat.id, CHANNEL_ID, post_id)
        bot.reply_to(message, message_text)
    except Exception as e:
        print("[forward] failed")
        print(f"  command={command}")
        print(f"  channel_key={content.get('channel_key')}")
        print(f"  channel_id={CHANNEL_ID}")
        print(f"  message_ids={message_ids}")
        print(f"  error_type={type(e).__name__}")
        print(f"  error={e}")
        bot.reply_to(message, "💢اكو مشكلة من البوت.\n حاول مرة ثانية")

def log_and_forward(message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""
    full_name = (first_name + " " + last_name).strip()

    log_msg = (
        f"👤 رسالة جديدة:\n"
        f"• الاسم: {full_name}\n"
        f"• اليوزر: @{username}\n"
        f"• الايدي: {user_id}\n"
        f"• نوع الرسالة: {message.content_type}\n"
        f"• من البوت @cs_stg3_bot\n"
    )

    if user_id != ADMIN_ID:
        sent = bot.send_message(LOG_CHANNEL_ID, log_msg)

        # لو الرسالة نصية نرسلها كرد على رسالة التفاصيل
        if message.content_type == "text":
            bot.send_message(
                LOG_CHANNEL_ID, message.text, reply_to_message_id=sent.message_id
            )
        else:
            # للملفات والأنواع الأخرى فقط نعيد توجيه الرسالة (بدون رد)
            try:
                bot.forward_message(
                    chat_id=LOG_CHANNEL_ID,
                    from_chat_id=message.chat.id,
                    message_id=message.message_id,
                )
            except Exception as e:
                print(f"خطأ في إعادة توجيه الرسالة إلى القناة: {e}")


# =========[ بدء تشغيل البوت ]=========
bot.polling()
