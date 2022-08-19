from telebot.async_telebot import AsyncTeleBot

import os


bot = AsyncTeleBot(os.getenv("TELEGRAM_API_KEY"))
