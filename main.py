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
