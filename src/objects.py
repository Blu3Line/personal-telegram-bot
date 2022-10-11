from telebot.async_telebot import AsyncTeleBot

import os

BOT = os.getenv("api-key")

if BOT == None:
    print("executed")
    from dotenv import load_dotenv
    load_dotenv()
    BOT = os.getenv("api-key")
    

DB_URI = os.getenv("DATABASE_URL")#cfg vars da hatalı yazmışım unlucky
WEATHER_KEY = os.getenv("weather-key")

bot = AsyncTeleBot(BOT)
