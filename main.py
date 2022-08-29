import asyncio

from src import *

# botla selamlaş
@bot.message_handler(commands=["hello", "selam", "merhaba"])
async def selamla(message):
    me = await bot.get_me()
    target = message.from_user
    await bot.reply_to(message, f'''\
    Selam, ben {me.first_name}.
Tanıştığıma memnun oldum {target.first_name}!
''')

#webhook yap
if __name__ == "__main__":
    
    asyncio.run(bot.polling(non_stop=True))

'''
duyurular - Fırat Üniversitesi ilk 15 duyuruyu getirir.
fiil - ingilizce düzenli ve düzensiz fiil çalışma komutu
kelime - ingilizce türkçe kelime kart oyunu
ekle_kelime - yeni ingilizce türkçe kelime ekleme komutu
sil_kelime - olan kelimeyi silme komutu
bul_kelime - database den kelime bulma komutu
hava_durumu - Güncel hava durumunu öğrenme
'''
#gizlilik olayını kontrol et
#not uygulaması yap