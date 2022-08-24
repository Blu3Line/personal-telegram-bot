from src.objects import bot

#bot ile konuşma başlatılırsa tetiklenicek fonksiyon
@bot.message_handler(commands=["start"])
async def start_message(message):
    await bot.reply_to(message,"sa mal")
