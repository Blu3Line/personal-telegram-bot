from telebot.async_telebot import AsyncTeleBot

import os
import json

# scrpt_path = os.path.abspath(__file__)
# dirpath = os.path.dirname(scrpt_path)
# cfgpath = os.path.join(dirpath, 'config.json')

# with open(cfgpath) as f:
#     cfg = json.load(f)

bot = AsyncTeleBot(os.getenv("api-key"))
