
import asyncio

from src import *

# botla selamlaş
@bot.message_handler(func=lambda message: True if message.text.lower() == "!selam" else False)
@bot.message_handler(commands=["hello", "selam", "merhaba"])
async def selamla(message):
    me = await bot.get_me()
    await bot.reply_to(message, f'''\
    Selam, ben {me.first_name}.
Tanıştığıma memnun oldum.
                       ''')

#webhook yap
if __name__ == "__main__":
    
    asyncio.run(bot.polling())
