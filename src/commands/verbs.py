from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

import random

from src.objects import bot
from src.Database.database_handler import get_verbs

current_verb = {}  # random seçilecek kelimeyi bu değişkende tutucaz
# inline keyboardların callback dataları ona göre callbackquery tetiklenicek
callback_datas = ["wrong_btn_v", "flip_btn_v", "true_btn_v", "exit_btn_v", "regular", "irregular"]
lst_data = []
flip_times = 0
is_last_verb = False
def random_verb():  # random fiili current_verbe koyuyoyurz
    global current_verb
    while True:  # bu loopun amacı eğer wrong btn basılırsa random choice yine aynı olursa api hata verir onu bypass
        result_verb = random.choice(lst_data)
        if result_verb != current_verb:
            current_verb = result_verb
            break
    return current_verb

def card_keyboard():  # makrkup için butonları ayarlıyoruz
    markup = InlineKeyboardMarkup()
    markup.row_width = 8
    if is_last_verb:#eğer son fiile gelirse wrong ve true butonları kaldırır
        layout = [
            InlineKeyboardButton(text="Flip!", callback_data="flip_btn_v"),
            InlineKeyboardButton(text="Exit", callback_data="exit_btn_v")]
    else:
        layout = [InlineKeyboardButton(text="❌", callback_data="wrong_btn_v"),
                InlineKeyboardButton(text="Flip!", callback_data="flip_btn_v"),
                InlineKeyboardButton(text="✅", callback_data="true_btn_v"),
                InlineKeyboardButton(text="Exit", callback_data="exit_btn_v")]
    markup.add(*layout)

    return markup

def verb_choose_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 8
    layout = [
        InlineKeyboardButton(text="irregular verbs", callback_data="irregular"),
        InlineKeyboardButton(text="Exit", callback_data="exit_btn_v"),
        InlineKeyboardButton(text="regular verbs", callback_data="regular")
    ]
    markup.add(*layout)
    return markup


@bot.message_handler(commands=["fiil"])
async def verb_handler(message):
    await bot.send_message(message.chat.id, "Lütfen çalışmak istediğiniz verb türünü seçin.", reply_markup=verb_choose_markup())

#ilerde maintain yaptığında keliemler query ile birleştirip kodu azalt
@bot.callback_query_handler(func=lambda call: call.data in callback_datas)
async def callback_query_verb(call):
    global lst_data, flip_times,is_last_verb
    
    match call.data:
        
        case "irregular":
            # databaseden kelimeleri bir list içine depolar ilerde bunu generator ile editle
            lst_data = get_verbs("irregularverbs")
            if len(lst_data) == 1:# eğer başlangıç listesi 1 fiil ise
                is_last_verb = True
            await bot.edit_message_text(text=f"Verb: {random_verb()[0]}",
                                        chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        reply_markup=card_keyboard())
        
        case "exit_btn_v":
            flip_times = 0 #döndürme sayısı sıfırlansın aga
            is_last_verb = False #exit butonu basıp bir daha program çağırılırsa diye
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        
        case "regular":
            
            
            # databaseden kelimeleri bir list içine depolar ilerde bunu generator ile editle
            lst_data = get_verbs("regularverbs")
            if len(lst_data) == 1:# eğer başlangıç listesi 1 fiil ise
                is_last_verb = True
            await bot.edit_message_text(text=f"Verb: {random_verb()[0]}",
                                        chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        reply_markup=card_keyboard())
        case "wrong_btn_v":
            if flip_times % 2 == 0: #kart arka tarafı açık şekilde geçmesin diye
                await bot.edit_message_text(text=f"Verb: {random_verb()[0]}",
                                            chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            reply_markup=card_keyboard())
        
        case "flip_btn_v":
            flip_times += 1
            if flip_times % 2 == 0:
                await bot.edit_message_text(text=f"Verb: {current_verb[0]}",
                                            chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            reply_markup=card_keyboard())
            else:
                await bot.edit_message_text(text=f"""Simple Past(v2): {current_verb[1]}\nPast Participle(v3): {current_verb[2]}\nTürkçe Anlamı: {current_verb[3]}""",
                                            chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            reply_markup=card_keyboard())
        
        case "true_btn_v":
            if flip_times % 2 == 0: #kart arka tarafı açık şekilde geçmesin diye
                lst_data.remove(current_verb)
                if len(lst_data) == 1:
                    is_last_verb = True
                await bot.edit_message_text(text=f"Verb: {random_verb()[0]}",
                                        chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        reply_markup=card_keyboard())
        case _:
            await bot.send_message(call.message.chat.id, "bir şeyler yanlış gitti matchcase")
            
# DATABASEDEN VERB SAYISI 0 ALINIRSA DİYE BİR SENARYO YAZ