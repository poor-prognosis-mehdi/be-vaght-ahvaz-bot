import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ============================ تنظیمات (اینجا را پر کنید) ============================
# توکنی که از @BotFather گرفته‌اید، دقیقاً همینجا جایگزین کنید:
BOT_TOKEN ="8730995107:AAFB_JZioOcagqhdh3yL7gDwZEqt8JKKGqI"

# آیدی عددی چتی که پیام‌های ناشناس باید به آن فوروارد شود (آیدی خودتان یا یک گروه خصوصی)
# برای گرفتن آیدی عددی خودتان می‌توانید به بات @userinfobot در تلگرام پیام بدهید.
ADMIN_CHAT_ID = 218104646

# لینک و نام کانال خبری شما
CHANNEL_LINK = "https://t.me/your_channel"
CHANNEL_NAME = "به وقت اهواز"
# =====================================================================================

WAITING_FOR_MESSAGE = 1


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    intro_text = (
        f"سلام 👋\n\n"
        f"به بات *{CHANNEL_NAME}* خوش آمدید.\n\n"
        f"📰 برای دنبال کردن آخرین اخبار به کانال ما بپیوندید:\n"
        f"{CHANNEL_LINK}\n\n"
        f"همچنین می‌توانید پیام یا خبر خود را به‌صورت *کاملاً ناشناس* برای ما ارسال کنید."
    )
    keyboard = [
        [InlineKeyboardButton("📢 عضویت در کانال", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✉️ ارسال پیام ناشناس", callback_data="anon_msg")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        intro_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup
    )


async def ask_for_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "پیام خود را بنویسید و ارسال کنید.\n"
        "این پیام بدون نام یا شناسه شما برای ادمین فرستاده می‌شود.\n"
        "برای انصراف /cancel را بزنید."
    )
    return WAITING_FOR_MESSAGE


async def forward_anonymous(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if ADMIN_CHAT_ID:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"📩 پیام ناشناس جدید:\n\n{update.message.text}",
        )
    await update.message.reply_text("✅ پیام شما با موفقیت و به‌صورت ناشناس ارسال شد. ممنون!")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("ارسال پیام لغو شد.")
    return ConversationHandler.END


def main() -> None:
    if "ExampleTokenReplaceThisWithYourOwn" in BOT_TOKEN:
        raise RuntimeError(
            "لطفاً مقدار BOT_TOKEN را در بخش تنظیمات بالای فایل با توکن واقعی خودتان جایگزین کنید."
        )

    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(ask_for_message, pattern="^anon_msg$")],
        states={
            WAITING_FOR_MESSAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, forward_anonymous)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)

    logger.info("Bot is starting (polling mode)...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
