import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers import wake_up, say_hi, handle_location


def run_bot():
    load_dotenv()
    token = os.getenv("TOKEN")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", wake_up))
    app.add_handler(CommandHandler("myID", say_hi))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))
    app.add_handler(MessageHandler(filters.TEXT, say_hi))

    app.run_polling()
