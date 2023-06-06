import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from config import tg_bot_token

bot_token = tg_bot_token

# экземпляр бота и диспетчер
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

# Словарь для хранения данных чата
chat_data = {}

api_url = "http://localhost:5001"

#emoji
code_to_emoji = {
        "Clear": "Clear \U00002600",
        "Clouds": "Clouds \U00002601",
        "Rain": "Rain \U00002614",
        "Drizzle": "Drizzle \U00002614",
        "Thunderstorm": "Thunderstorm \U000026A1",
        "Snow": "Snow \U0001F328",
        "Mist": "Mist \U0001F32B"
    }

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    # Если город еще не сохранен в контексте чата, запрашиваем его у пользователя
    if not chat_data.get(message.chat.id):
        await message.answer("Hi, I'm a weather bot. Enter the name of the city to get the weather.")
        # Сохраняем город в контексте чата
        chat_data[message.chat.id] = {}
    else:
        # Город уже сохранен в контексте чата, поэтому предлагаем пользователю выбрать запрос
        await message.answer("Select a request:",
            reply_markup=buttons,
        )

# Обработчик команды /help
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    # Отправляем сообщение с помощью бота
    await message.answer('It is a telegram bot for getting the weather in your city. \n\nWrite the /start command and enter the name of your city. \n\nThen choose one of four options: \n\nTemperature; \nWeather Description; \nSunrise/sunset time; \nWeather forecast; \n\nOr you can change the city by clicking on the Change City button. \n\nEnjoy using it.')

# Список кнопок для выбора запроса
buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Temperature"),
            KeyboardButton(text="Weather description"),
            KeyboardButton(text="Sunrise/sunset time"),
            KeyboardButton(text="Weather forecast"),
        ],
        [KeyboardButton(text="Change city")],
    ],
    resize_keyboard=True,
)

@dp.message_handler()
async def message_handler(message: types.Message):
    chat_id = message.chat.id

    if message.text == "Change city":
        chat_data[chat_id].pop("city", None)
        await message.answer("Enter a new city:")
        return

    # Если город еще не сохранен в контексте чата, сохраняем его и запрашиваем запрос
    if not chat_data[chat_id].get("city"):
        chat_data[chat_id]["city"] = message.text
        await message.answer("Select a request::",
            reply_markup=buttons,
        )
        return

    # город из контекста чата
    city = chat_data[chat_id]["city"]

    # ответ пользователя в зависимости от выбранного запроса
    if message.text == "Temperature":
        # запрос на локальное API, чтобы получить описание погоды
        response = requests.get(f"{api_url}/weather?city={city}")
        if response.status_code == 200:
            data = response.json()
            temperature = data.get("temperature")
            feels_like = data.get("feels_like")
            temperature_advice = data.get("temperature_advice")
            # ответ обратно пользователю
            await message.answer(f"Temperature in {city}: {temperature}. \nFeels like: {feels_like}. \n{temperature_advice}")
        else:
            await message.answer("It was not possible to get weather data.")

    elif message.text == "Weather description":
        # запрос на  локальное API, чтобы получить описание погоды
        response = requests.get(f"{api_url}/wd?city={city}")
        if response.status_code == 200:
            data = response.json()
            wind = data.get("wind")
            wd = data.get("wd")
            weather_advice = data.get("weather_advice")
            
            if wd in code_to_emoji:
                wd = code_to_emoji[wd]
            
            # ответ обратно пользователю
            await message.answer(f"Weather description in {city}: {wd}. \nWind speed: {wind} \n{weather_advice}.")
        else:
            await message.answer("It was not possible to get weather data.")

    elif message.text == "Sunrise/sunset time":
        # запрос на  локальное API, чтобы получить время рассвета/заката
        response = requests.get(f"{api_url}/stime?city={city}")
        if response.status_code == 200:
            data = response.json()
            sunrise_time = data.get("sunrise_time")
            sunset_time = data.get("sunset_time")
            # ответ обратно пользователю
            await message.answer(f"Sunrise/sunset time in {city}: \nSunrise - {sunrise_time} \nSunset - {sunset_time}.")
        else:
            await message.answer("It was not possible to get sunrise/sunset time.")

    elif message.text == "Weather forecast":
        # запрос на локальное API, чтобы получить время рассвета/заката
        response = requests.get(f"{api_url}/forecast?city={city}")
        if response.status_code == 200:
            data = response.json()
            forecast = data.get("forecast")

            forecast_message = f"Weather forecast for {city}:\n"

            for item in forecast:
                date = item["date"]
                temperature = item["temperature"]
                description = item["description"]
                temperature_advice = item["temperature_advice"]
                weather_advice = item["weather_advice"]
                if description in code_to_emoji:
                    description = code_to_emoji[description]

                forecast_message += (
                    f"\nDate: {date}\nDescription: {description}\n"
                    f"Temperature: {temperature}\n{temperature_advice}\n"
                    f"{weather_advice}\n\n"
                )

            # Split the forecast message into chunks of maximum message length
            max_message_length = 4096  # Maximum length of a Telegram message
            forecast_chunks = [forecast_message[i:i + max_message_length] for i in range(0, len(forecast_message), max_message_length)]

            # Send each forecast chunk as a separate message
            for chunk in forecast_chunks:
                await message.answer(chunk)

    else:
        await message.answer("It was not possible to get the weather forecast.")


if __name__ == '__main__':
    executor.start_polling(dp)