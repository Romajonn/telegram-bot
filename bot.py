import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Render uchun port serveri
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

# Veb-serverni orqa fonda (background thread) yoqamiz
threading.Thread(target=run_dummy_server, daemon=True).start()
import telebot
from telebot import types

# Tokeningizni yozing
API_TOKEN = '8721986149:AAHun68uIGe7Rm_3mi2q5sb9iQHmJVd4OKg'

# Kanal username'ini yozing
CHANNEL_USERNAME = '@Namangan_toshkent3'

bot = telebot.TeleBot(API_TOKEN)

# Eski webhookni o'chirish
bot.remove_webhook()

def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        return status in ['creator', 'administrator', 'member']
    except Exception as e:
        print(f"Tekshirishda xatolik: {e}")
        return False

@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'document', 'sticker'])
def check_sub(message):
    if message.chat.type == 'private' or message.from_user.is_bot:
        return

    if not is_subscribed(message.from_user.id):
        try:
            bot.delete_message(message.chat.id, message.message_id)
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("📢 Kanalga obuna bo'lish", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"))
            
            bot.send_message(
                message.chat.id,
                f"⚠️ **{message.from_user.first_name}**, guruhda yozish uchun avval rasmiy kanalimizga obuna bo'ling!",
                reply_markup=markup,
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Xabar o'chirishda xatolik: {e}")

print("Bot muvaffaqiyatli ishga tushdi! Guruhni tekshirmoqda...")
bot.infinity_polling(skip_pending=True)
