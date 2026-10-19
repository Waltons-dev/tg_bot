import os
import aiohttp
from telegram import Update
from dotenv import load_dotenv

load_dotenv()

TOKEN_WEATHER = os.getenv("TOKEN_WEATHER")

URL_WEATHER = "https://api.openweathermap.org/data/2.5/weather"
URL_CAT = "https://api.thecatapi.com/v1/images/search"
URL_FACT = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"


def get_user_info(update: Update) -> str:
    user = update.effective_user
    chat = update.effective_chat

    if user is None or chat is None:
        return "Не удалось получить информацию о пользователе."

    return (
        f"Имя: {user.first_name}\n"
        f"Фамилия: {user.last_name or 'Не указана'}\n"
        f"Username: @{user.username or 'Не указан'}\n"
        f"ID пользователя: {user.id}\n"
        f"ID чата: {chat.id}"
    )


async def get_cat_url():
    try:
        timeout = aiohttp.ClientTimeout(total=10)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(URL_CAT) as response:
                if response.status != 200:
                    return None

                data = await response.json()

    except (aiohttp.ClientError, TimeoutError):
        return None

    if not data or not data[0].get("url"):
        return None

    return data[0]["url"]


async def get_fact():
    try:
        timeout = aiohttp.ClientTimeout(total=10)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(URL_FACT) as response:
                if response.status != 200:
                    return None

                data = await response.json()

    except (aiohttp.ClientError, TimeoutError):
        return None

    return data.get("text") if isinstance(data, dict) else None


async def get_weather(lat: float, lon: float) -> str:
    if not URL_WEATHER or not TOKEN_WEATHER:
        return "Не указан URL сервиса погоды или API-токен."

    params = {
        "lat": lat,
        "lon": lon,
        "appid": TOKEN_WEATHER,
        "units": "metric",
        "lang": "ru",
    }

    try:
        timeout = aiohttp.ClientTimeout(total=10)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(URL_WEATHER, params=params) as response:
                if response.status != 200:
                    return "Не удалось получить погоду. Проверь URL и API-токен."

                data = await response.json()

    except (aiohttp.ClientError, TimeoutError):
        return "Ошибка сетевого запроса погоды."

    weather_info = data.get("weather", [])
    main_info = data.get("main", {})
    wind_info = data.get("wind", {})
    city = data.get("name", "Неизвестный город")

    if not weather_info or not main_info:
        return "Сервис погоды вернул неполные данные."

    description = weather_info[0].get("description", "Нет описания")
    temperature = main_info.get("temp")
    feels_like = main_info.get("feels_like")
    wind_speed = wind_info.get("speed")

    if temperature is None or feels_like is None or wind_speed is None:
        return "Не удалось получить все данные о погоде."

    if wind_speed >= 10:
        recommendation = "На улице сильный ветер. Будь осторожен."
    elif temperature < 0:
        recommendation = "На улице мороз. Оденься потеплее."
    elif temperature >= 25:
        recommendation = "На улице тепло. Не забудь пить воду."
    else:
        recommendation = "Погода подходит для прогулки."

    return (
        f"Погода в городе {city}:\n"
        f"Описание: {description.capitalize()}\n"
        f"Температура: {temperature} °C\n"
        f"Ощущается как: {feels_like} °C\n"
        f"Скорость ветра: {wind_speed} м/с\n\n"
        f"{recommendation}"
    )
