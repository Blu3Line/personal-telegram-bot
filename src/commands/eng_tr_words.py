from email import message
import pandas as pd
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import time

from src.objects import bot

# BUNUN DB VERİSONU YAZILACAK

data = pd.read_csv("./src/commands/kelimeoyunsrc/words.csv")#csvden pandas yardımıyla kelimeleri çekiyor
lst_data = data.to_dict(orient="records")#DataFrame objesini listenin içinde dict kelimeler olarak ayırıyor [{"Ingilizce":"word","Türkçe":"kelime"}, ...]
current_word = {}#random seçilecek kelimeyi bu değişkende tutucaz
# inline keyboardların callback dataları ona göre callbackquery tetiklenicek
callback_data = ["wrong_btn", "flip_btn", "true_btn"]


def random_word():#random kelimeyi current worde koyuyoruz
    global current_word

    current_word = random.choice(lst_data)
    return current_word


def card_keyboard():#makrkup için butonları ayarlıyoruz
    markup = InlineKeyboardMarkup()
    markup.row_width = 8
    layout = [InlineKeyboardButton(text="❌", callback_data="wrong_btn"),
              InlineKeyboardButton(text="Flip!", callback_data="flip_btn"),
              InlineKeyboardButton(text="✅", callback_data="true_btn")]
    markup.add(*layout)

    return markup

def last_word_markup():#son kelime için buton düzeni
    markup = InlineKeyboardMarkup()
    markup.row_width = 8
    layout = [
        InlineKeyboardButton(text="Flip!", callback_data="flip_btn")
    ]
    markup.add(*layout)
    
    return markup

flip_count = 0#kart ön yüz ve arka yüzü çevirmek için kullanılıcak

# tetiklenme olayı line 13

bir_kalmak_uzere = False #listede 2 kelime kalınca true döndürmemiz lazım
@bot.callback_query_handler(func=lambda call: call.data in callback_data)
async def callback_query(call):
    global flip_count, bir_kalmak_uzere
    if len(lst_data) == 2:#listede 2 kaldı ve execute olucak
        bir_kalmak_uzere = True
    if len(lst_data) > 1:#listede 1 den fazla kelime olunca geçme tuşları + flip olucak
        match call.data:

            case "wrong_btn":
                if flip_count % 2 == 0:  # türkçe tarafı çeviriliyken işlem yapamasın
                    print("wrong btn çalıştı")
            case "flip_btn":
                flip_count += 1
                
                if flip_count % 2 == 1:
                    await bot.edit_message_text(text=current_word["Türkçe"], chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=card_keyboard())
                else:
                    await bot.edit_message_text(text=current_word["Ingilizce"], chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=card_keyboard())
            case "true_btn":
                if flip_count % 2 == 0:  # türkçe tarafı çeviriliyken işlem yapamasın
                    lst_data.remove(current_word)
                    if bir_kalmak_uzere:#1 kalırsa son kelimeyi cardkeyboard markup ile yapmasın diye
                        await bot.edit_message_text(text=random_word()["Ingilizce"], chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=last_word_markup())
                        return
                    else:
                        await bot.edit_message_text(text=random_word()["Ingilizce"], chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=card_keyboard())
                # elif len(lst_data) == 1:#son kelime kalınca execute olucak
                #     
            case _:
                print("something went wrong")
    else:#listede 1 kelime varsa direkt olarak geçme tuşları olmucak
        if call.data == "flip_btn":
            flip_count += 1
            if flip_count % 2 == 1:#türkçe tarafına geçmek için
                await bot.edit_message_text(text=current_word["Türkçe"], chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=last_word_markup())
            else:
                await bot.edit_message_text(text=current_word["Ingilizce"], chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=last_word_markup())
        

    
@bot.message_handler(commands=["kelime"])
async def kelime_handler(message):
    if len(lst_data) > 1:#kelime listesinde 1den fazla varsa alltaki markup 1 kelime varsa diğer markup çalışıcak
        await bot.send_message(message.chat.id, random_word()["Ingilizce"], reply_markup=card_keyboard())
    else:
        await bot.send_message(message.chat.id, random_word()["Ingilizce"], reply_markup=last_word_markup())