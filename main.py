from flask import Flask, request
import telebot
import os

API_TOKEN = "8156774934:AAE7UU8-m-6YZ5G1HEhuky1vaz5ge7hcmNA"
bot = telebot.TeleBot(API_TOKEN)
RLM = '\u200F'  # کاراکتر راست‌چین‌کننده

app = Flask(__name__)

@app.route('/')
def index():
    return "I'm alive!"

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "لطفا متن خود را ارسال کنید")

@bot.message_handler(func=lambda m: m.text is not None)
def handle_message(message):
    if message.chat.type in ['private', 'group', 'supergroup']:
        rtl_text = RLM + message.text
        try:
            bot.reply_to(message, rtl_text)
        except Exception as e:
            print("خطا در ارسال پیام:", e)

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

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    bot.remove_webhook()
    bot.set_webhook(url="https://telegram-rtl-bot.onrender.com/webhook")  # ← آدرس تو اینه
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
