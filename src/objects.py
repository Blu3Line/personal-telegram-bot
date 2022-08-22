from telebot.async_telebot import AsyncTeleBot
from boto.s3.connection import S3Connection

import os
import json

scrpt_path = os.path.abspath(__file__)
dirpath = os.path.dirname(scrpt_path)
cfgpath = os.path.join(dirpath, 'config.json')

with open(cfgpath) as f:
    cfg = json.load(f)

#herokudan api key almak için
s3 = S3Connection(os.environ['api-key'])

bot = AsyncTeleBot(s3)
