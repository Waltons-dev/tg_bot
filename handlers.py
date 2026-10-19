from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import ContextTypes
from utils import get_user_info, get_cat_url, get_weather, get_fact


def get_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["Фото котика", "Сгенери аватар"],
            ["Мой ID", "Случайный факт"],
            ["Погода сегодня"],
        ],
        resize_keyboard=True,
    )


async def wake_up(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    await update.message.reply_text(
        "Привет! Я бот с несколькими полезными функциями.",
        reply_markup=get_keyboard(),
    )


async def say_hi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        return

    text = update.message.text

    if text == "Фото котика":
        photo_url = await get_cat_url()

        if photo_url:
            await update.message.reply_photo(
                photo=photo_url,
                caption="Держи фотографию котика!",
            )
        else:
            await update.message.reply_text(
                "Не удалось получить фотографию котика."
            )

    elif text == "Сгенери аватар":
        user = update.effective_user

        if user:
            await update.message.reply_photo(
                photo=f"https://robohash.org/{user.id}.png",
                caption="Твой сгенерированный аватар!",
            )

    elif text == "Мой ID":
        await update.message.reply_text(get_user_info(update))

    elif text == "Случайный факт":
        fact = await get_fact()

        if fact:
            await update.message.reply_text(f"Случайный факт:\n{fact}")
        else:
            await update.message.reply_text(
                "Не удалось получить случайный факт."
            )

    elif text == "Погода сегодня":
        await request_location(update, context)

    elif text == "Отмена":
        await update.message.reply_text(
            "Главное меню:",
            reply_markup=get_keyboard(),
        )

    else:
        await update.message.reply_text(
            "Выбери действие в меню.",
            reply_markup=get_keyboard(),
        )



async def request_location(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if update.message is None:
        return

    keyboard = [
        [KeyboardButton("Отправить геопозицию", request_location=True)],
        [KeyboardButton("Отмена")],
    ]

    await update.message.reply_text(
        "Нажми кнопку ниже, чтобы отправить свою геопозицию.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )


async def handle_location(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if update.message is None or update.message.location is None:
        return

    location = update.message.location
    weather = await get_weather(location.latitude, location.longitude)

    await update.message.reply_text(weather)
    await update.message.reply_text(
        "Главное меню:",
        reply_markup=get_keyboard(),
    )
