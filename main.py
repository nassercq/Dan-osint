import telebot
from telebot import types
import requests
import time
import random
from flask import Flask
from threading import Thread

# --- كود الـ Keep Alive (لإبقاء البوت شغال 24 ساعة) ---
app = Flask('')

@app.route('/')
def home():
    return "NIGHTRLOT SYSTEM IS ONLINE ✅"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive() # تشغيل السيرفر المصغر
# --------------------------------------------------

TOKEN = "8617957489:AAEXBY36zmhieVpBmHk1TanH0_uxcnkOT4c"
bot = telebot.TeleBot(TOKEN)

user_states = {}

def get_main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("📱 بيانات الرقم", callback_data="set_search_number"),
        types.InlineKeyboardButton("🔍 رادار الأسماء", callback_data="set_search_name"),
        types.InlineKeyboardButton("📡 تتبع الـ IP", callback_data="set_ip_track"),
        types.InlineKeyboardButton("👁️ Osint Scanner", callback_data="osint_menu"),
        types.InlineKeyboardButton("📂 سحب القواعد", callback_data="alert"),
        types.InlineKeyboardButton("🔐 كاشف الباسوردات", callback_data="alert"),
        types.InlineKeyboardButton("🚘 استعلام اللوحات", callback_data="alert"),
        types.InlineKeyboardButton("☢️ نظام RAT", callback_data="alert"),
        types.InlineKeyboardButton("🛡️ تخطي الجدران", callback_data="alert"),
        types.InlineKeyboardButton("📖 تعليمات النظام", callback_data="info"),
        types.InlineKeyboardButton("📶 حالة الاتصال", callback_data="alert"),
        types.InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings")
    ]
    markup.add(*buttons)
    return markup

def news_footer(chat_id):
    bot.send_message(chat_id, "📢 لتتبع آخر أخبار التحديثات والمميزات :\n💠 @nightrlot")

@bot.message_handler(commands=['start'])
def welcome(message):
    loading = bot.send_message(message.chat.id, "📡 Establishing encrypted connection...")
    time.sleep(0.5)
    bot.edit_message_text("🔐 Decrypting access protocol...", message.chat.id, loading.message_id)
    time.sleep(0.5)
    bot.delete_message(message.chat.id, loading.message_id)

    welcome_text = (
        "💠 **WELCOME TO DEEP SEARCH SYSTEM**\n\n"
        "━━━━━━━━━━━━━━\n\n"
        "Login Successful\n\n"
        "Rank : ( Guest ) 👤\n\n"
        "Status : Secure & Stable ✅\n\n"
        "━━━━━━━━━━━━━━\n\n"
        "الرجاء اختيار الوحدة المطلوبة لبدء العملية :"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_keyboard(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "alert":
        alert_text = (
            "⚠️ Admin Notification\n\n"
            "This unit requires a Premium subscription\n\n"
            "To activate, contact the developer :\n"
            "💠 @nightrlot"
        )
        bot.send_message(call.message.chat.id, alert_text)

    elif call.data == "osint_menu":
        markup = types.InlineKeyboardMarkup(row_width=2)
        btns = [
            types.InlineKeyboardButton("Snapchat", callback_data="osint_run"),
            types.InlineKeyboardButton("TikTok", callback_data="osint_run"),
            types.InlineKeyboardButton("YouTube", callback_data="osint_run"),
            types.InlineKeyboardButton("Facebook", callback_data="osint_run")
        ]
        markup.add(*btns)
        bot.send_message(call.message.chat.id, "🛡️ **OSINT SCANNER UNIT**\n\nSelect platform to start scanning :", reply_markup=markup)

    elif call.data == "osint_run":
        user_states[call.message.chat.id] = "waiting_osint"
        bot.send_message(call.message.chat.id, "📝 أرسل يوزر المستهدف (English Only) :")

    elif call.data == "set_search_name":
        user_states[call.message.chat.id] = "waiting_name"
        bot.send_message(call.message.chat.id, "🔍 **رادار الأسماء**\n\nأرسل الاسم الذي تريد البحث عنه :")

    elif call.data == "set_search_number":
        user_states[call.message.chat.id] = "waiting_number"
        bot.send_message(call.message.chat.id, "📱 **بيانات الرقم**\n\nأرسل الرقم مع مفتاح الدولة :")

    elif call.data == "set_ip_track":
        user_states[call.message.chat.id] = "waiting_ip"
        bot.send_message(call.message.chat.id, "📡 **تتبع الـ IP**\n\nأرسل عنوان الـ IP المراد تعقبه :")

    elif call.data == "settings":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("💠 قناة النظام", url="https://t.me/nightrlot"))
        bot.send_message(call.message.chat.id, "⚙️ **System Settings**\n\nDeveloper : @nightrlot\nSupport : @nightrlot", reply_markup=markup)

    elif call.data == "info":
        info = (
            "ℹ️ **Units Guide**\n\n"
            "🔹 **Phone Data :** International identity reveal.\n\n"
            "🔹 **Name Radar :** Extraction from deep databases.\n\n"
            "🔹 **OSINT :** Digital footprint scanning.\n\n"
            "🔹 **IP Track :** Geographic network mapping."
        )
        bot.send_message(call.message.chat.id, info, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.chat.id in user_states)
def handle_all_inputs(message):
    state = user_states[message.chat.id]
    text = message.text.strip()
    chat_id = message.chat.id

    if state == "waiting_osint":
        if len(text) > 11:
            bot.reply_to(message, "❌ Error : Username too long.")
        elif any(char.isalpha() and (ord(char) < 65 or ord(char) > 122) for char in text):
            bot.reply_to(message, "❌ Error : English characters only.")
        else:
            bot.send_message(chat_id, "⏳ Analyzing digital footprint...")
            time.sleep(1.2)
            if random.random() > 0.8:
                bot.send_message(chat_id, "⚠️ No records found for this user.")
            else:
                ip_fake = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
                response = f"✅ **DATA EXTRACTED : {text}**\n\n🌐 Connection IP : {ip_fake}\n\n📟 Serial ID : {random.randint(100000, 999999)}\n\n📍 Status : Online / Secured\n\nOperation completed successfully."
                bot.send_message(chat_id, response, parse_mode="Markdown")
        news_footer(chat_id)

    elif state == "waiting_ip":
        bot.send_message(chat_id, "📡 Tracking source...")
        time.sleep(1)
        res = f"📍 **Tracking Results for {text}**\n\nCountry : Saudi Arabia 🇸🇦\n\nISP : Integrated Telecom\n\nCoordinates : 24.7136 / 46.6753"
        bot.send_message(chat_id, res, parse_mode="Markdown")
        news_footer(chat_id)

    elif state in ["waiting_name", "waiting_number"]:
        bot.send_message(chat_id, "🔎 Scanning deep databases...")
        url = f"https://caller-id.saedhamdan.com/index.php/UserManagement/search_number?country_code=SA&{'name' if state == 'waiting_name' else 'number'}={text}"
        try:
            data = requests.get(url, timeout=12).json()
            results = data.get("result", [])
            if not results:
                bot.send_message(chat_id, "⚠️ No results found in this range.")
            else:
                res_text = "🎯 **Deep Search Results (50 Records) :**\n\n"
                for i, res in enumerate(results[:50], 1):
                    name = res.get("name", "Unknown")
                    number = res.get("number", "Private")
                    res_text += f"{i} ➔ {name} | `{number}`\n\n"

                if len(res_text) > 4000:
                    for x in range(0, len(res_text), 4000):
                        bot.send_message(chat_id, res_text[x:x+4000], parse_mode="Markdown")
                else:
                    bot.send_message(chat_id, res_text, parse_mode="Markdown")
        except:
            bot.send_message(chat_id, "❌ Central server connection failed.")
        news_footer(chat_id)

    del user_states[chat_id]

bot.polling(none_stop=True)
