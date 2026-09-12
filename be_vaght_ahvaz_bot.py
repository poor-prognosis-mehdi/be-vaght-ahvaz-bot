import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN ="8730995107:AAH1RJmIUEVwKDoaaIKl_o5x3m7j4dg1kU8"
ADMIN_ID = 218104646

ABOUT_BOT_TEXT = """سلام هم‌استانی عزیز 👋

توی این بات تلگرام قسمتی رو گذاشتیم برای پیام‌های شما درباره مشکلات و مسائل روز استان خوزستان؛ که هر چی می‌خواستید به ما منتقل کنید رو از طریق این قسمت، بدون درج اسم و آیدی شما و به‌صورت کاملاً مخفیانه، به دست تیم پایگاه خبری به وقت اهواز می‌رسونه و ما پیگیر مشکلات شما خواهیم بود.

ممنون از انتخاب ما به‌عنوان یک پل برای بیان مشکلاتتون 🙏"""

waiting_users = {}
question_map = {}  # کد سوال -> آیدی عددی کاربر
next_question_id = 1
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()

    btn_about = InlineKeyboardButton("🤖 معرفی بات", callback_data="about_bot")
    btn_question = InlineKeyboardButton("✉️ پیام شخصی پنهانی", callback_data="ask_question")

    # ترتیب ردیف‌ها دقیقاً همین‌طور که چیده شده رندر می‌شود
    markup.row(btn_about)
    markup.row(btn_question)

    bot.send_message(message.chat.id, "یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "about_bot")
def about_bot(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, ABOUT_BOT_TEXT)

@bot.callback_query_handler(func=lambda call: call.data == "ask_question")
def ask_question(call):
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    waiting_users[user_id] = True
    bot.send_message(user_id, "مشکل یا مسئله منطقه سکونت خود را بیان کنید :")

@bot.message_handler(func=lambda message: message.from_user.id in waiting_users)
def receive_question(message):
    global next_question_id
    user = message.from_user

    qid = next_question_id
    next_question_id += 1
    question_map[qid] = user.id

    text = f"""
📩 صحبت جدید دریافت شد (ناشناس)
🔑 کد سوال: {qid}
💬 متن سوال:
{message.text}

↩️ برای پاسخ، این دستور را بفرست:
/reply {qid} متن پاسخ شما
"""
    bot.send_message(ADMIN_ID, text)
    bot.send_message(message.chat.id, "✅  صحبت شما با موفقیت ارسال شد و در حال پردازش برای بررسی موضوع هستیم.")
    del waiting_users[user.id]

@bot.message_handler(commands=['reply'])
def reply_to_user(message):
    if message.from_user.id != ADMIN_ID:
        return  # فقط ادمین اجازه پاسخ دادن دارد

    try:
        parts = message.text.split(maxsplit=2)
        qid = int(parts[1])
        answer_text = parts[2]
    except (IndexError, ValueError):
        bot.send_message(ADMIN_ID, "❌ فرمت درست: /reply کد متن‌پاسخ")
        return

    target_user_id = question_map.get(qid)
    if not target_user_id:
        bot.send_message(ADMIN_ID, "❌ کد سوال معتبر نیست یا قبلاً پاسخ داده شده.")
        return

    try:
        bot.send_message(target_user_id, f"📬 پاسخ به صحبت شما:\n\n{answer_text}")
        bot.send_message(ADMIN_ID, "✅ پاسخ ارسال شد.")
        del question_map[qid]
    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ ارسال پاسخ ناموفق بود: {e}")

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
