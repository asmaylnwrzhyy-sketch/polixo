import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL = "@taeebig"
WEBAPP_URL = "https://asmaylnwrzhyy-sketch.github.io/polixo/?v=20260930"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "📢 عضویت در کانال",
                url="https://t.me/taeebig"
            )
        ],
        [
            InlineKeyboardButton(
                "✅ بررسی عضویت",
                callback_data="check_membership"
            )
        ]
    ]

    await update.message.reply_text(
        "👋 به پولیکس خوش اومدی!\n\n"
        "برای استفاده از ربات، ابتدا در کانال عضو شو و "
        "سپس روی «بررسی عضویت» بزن.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL,
            user_id=user_id
        )

        if member.status in ["member", "administrator", "creator"]:
            keyboard = [
                [
                    InlineKeyboardButton(
                        "🎮 ورود به بازی",
                        web_app=WebAppInfo(url=WEBAPP_URL)
                    )
                ]
            ]

            await query.edit_message_text(
                "✅ عضویت شما تأیید شد!\n\n"
                "🎮 حالا می‌تونی وارد بازی پولیکس بشی.",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        else:
            await query.answer(
                "❌ ابتدا باید در کانال عضو شوید.",
                show_alert=True
            )

    except Exception as e:
        print("Membership check error:", e)

        await query.answer(
            "⚠️ بررسی عضویت انجام نشد. دوباره تلاش کن.",
            show_alert=True
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        CallbackQueryHandler(
            check_membership,
            pattern="^check_membership$"
        )
    )

    print("🤖 Polixo Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
