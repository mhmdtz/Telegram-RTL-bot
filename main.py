# فایل اصلی ربات تلگرام RTL با کامنت فارسی

from keep_alive import keep_alive  # تابع نگه داشتن ربات فعال با استفاده از Flask
import telebot
import time

# توکن ربات تلگرام (توجه: این توکن عمومی است، امنیت آن مهم است)
API_TOKEN = "8156774934:AAE7UU8-m-6YZ5G1HEhuky1vaz5ge7hcmNA"
bot = telebot.TeleBot(API_TOKEN)

RLM = '\u200F'  # کاراکتر جهت‌گیری راست به چپ

# راه‌اندازی سرور کوچک Flask برای keep_alive
keep_alive()

# پاسخ به دستور /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "لطفا متن خود را ارسال کنید")

# پاسخ به تمام پیام‌های متنی (راست‌چین کردن متن)
@bot.message_handler(func=lambda m: m.text is not None)
def handle_message(message):
    if message.chat.type in ['private', 'group', 'supergroup']:
        rtl_text = RLM + message.text
        try:
            bot.reply_to(message, rtl_text)
        except Exception as e:
            print("خطا در ارسال پیام:", e)

# پاسخ به inline query برای ارسال متن راست‌چین
@bot.inline_handler(func=lambda query: True)
def handle_inline_query(inline_query):
    try:
        query_text = inline_query.query
        if not query_text:
            return
        rtl_text = RLM + query_text
        result = telebot.types.InlineQueryResultArticle(
            id='1',
            title="📤 ارسال متن راست‌چین",
            input_message_content=telebot.types.InputTextMessageContent(rtl_text)
        )
        bot.answer_inline_query(inline_query.id, [result])
    except Exception as e:
        print("خطای inline:", e)

# حلقه اصلی اجرای ربات با مدیریت خطا و تلاش مجدد
while True:
    try:
        bot.polling(non_stop=True)
    except Exception as e:
        print("خطای polling:", e)
        time.sleep(5)
