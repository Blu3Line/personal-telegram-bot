
import asyncio
from telebot.async_telebot import AsyncTeleBot
import requests as rq
import json

with open('config.json', 'r') as f:
	cfg = json.load(f)

bot = AsyncTeleBot(cfg["api_key"])


# botla selamlaş
@bot.message_handler(func=lambda message: True if message.text.lower() == "!selam" else False)
@bot.message_handler(commands=["hello", "selam", "merhaba"])
async def selamla(message):
    me = await bot.get_me()
    await bot.reply_to(message, f'''\
    Selam, ben {me.first_name}.
Tanıştığıma memnun oldum.
                       ''')


# agify api ve agify message handler (agify api da daha fazla özellikler var onu da eklersin)


def input_control(message):#regula expression ile update at buraya
    # input doğruluğuna göre message handler çalışması için birkaç ön şartlar
    if not (message.text.lower().startswith("!agify")) or len(message.text.split()) > 2:
        return False
    else:
        return True


# yukardaki fonksiyonu  burda kontrol ediyor eğer True ise çalışır
@bot.message_handler(func=input_control)
async def yas_tahmin(message):
    parameters = {
        "name": f"{message.text.split()[1]}"
    }
    url = "https://api.agify.io"
    # yukarda api setup yaptık aşşağıda async olarak request atmamız gerekiyor. ama bilmiyorum
    response = rq.get(url=url, params=parameters)
    response.raise_for_status()
    result = response.json()["age"]
    if result == None:
        await bot.reply_to(message, "Sonuç getiremedim benim aptallığım!")
    else:
        await bot.reply_to(message, f"Yaşınız tahminen:{result}. Eğer doğru değilse benim aptallığım!")
        await bot.reply_to(message, f"debug mode:{response.json()}")
# yukardaki kod parçacığı noobca yazıldı httpio dene


# fırat üniversitesi ui


if __name__ == "__main__":
    asyncio.run(bot.polling())
