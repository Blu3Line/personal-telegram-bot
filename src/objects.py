from telebot.async_telebot import AsyncTeleBot

import os
import json

with open("src\config.json") as read:
    cfg = json.load(read)
bot = AsyncTeleBot(cfg["api-key"])
