import requests

import os
import json

from src import bot

def weather_data(city:str):
    cfgpath = os.path.abspath("config.json")
    with open(cfgpath) as f:
        cfg = json.load(f)
    
    parameters = {
        "access_key":cfg["weatherkey"],
        "query":city
    }
    api_url = "http://api.weatherstack.com/current"
    
    with requests.get(url=api_url, params=parameters) as response:
        data = response.json()
    try:
        şehir = data["location"]["name"]
        ülke = data["location"]["country"]
        derece = data["current"]["temperature"]
        hava_durumu = " ".join(data["current"]["weather_descriptions"])
        hissedilen_derece = data["current"]["feelslike"]
        tarih = data["location"]["localtime"]
        
        return f"Lokasyon: {şehir}/{ülke}\nDurum: {derece}°C {hava_durumu}\nHissedilen: {hissedilen_derece}°C\nTarih: {tarih}"
    except KeyError:
        return None
    except Exception as e:
        print("sorun oluştu: ", e)
        return None


@bot.message_handler(commands=["hava_durumu"])
async def hava_durumu(message):
    input = message.text.strip().split()
    if len(input) == 2:
        weather_result = weather_data(input[1])
        if weather_result:
            await bot.reply_to(message, weather_result)
        else:
            await bot.reply_to(message, "hatalı şehir girişi ya da sorun oluştu!")
    else:
        await bot.reply_to(message, "hava durumunu öğrenmek için:\n/hava_durumu <şehir_ismi>")
    