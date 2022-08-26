from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

import random

from src.objects import bot
from src.utils.database_handler import find_word, get_words, add_new_word, delete_word


current_word = {}  # random seçilecek kelimeyi bu değişkende tutucaz
# inline keyboardların callback dataları ona göre callbackquery tetiklenicek
callback_data = ["wrong_btn", "flip_btn", "true_btn", "exit_btn"]
lst_data = []
flip_count = 0  # kart ön yüz ve arka yüzü çevirmek için kullanılıcak
is_last_word = False


def random_word():  # random kelimeyi current worde koyuyoruz
    # global current_word

    # current_word = random.choice(lst_data)
    # return current_word

    global current_word

    while True:  # bu looopun amacı eğer wrong btn basılırsa random choice yine aynı olursa api hata verir o yüzden %100 farklı choice olmalı
        result_word = random.choice(lst_data)
        if result_word != current_word:
            current_word = result_word
            break
    return current_word


def card_keyboard():  # makrkup için butonları ayarlıyoruz
    markup = InlineKeyboardMarkup()
    markup.row_width = 8
    if is_last_word:#eğer son kelimeye gelirse wrong ve true butonlarını kaldırır
        layout= [
            InlineKeyboardButton(text="Flip!", callback_data="flip_btn"),
            InlineKeyboardButton(text="Exit", callback_data="exit_btn")
        ]
    else:
        layout = [InlineKeyboardButton(text="❌", callback_data="wrong_btn"),
                InlineKeyboardButton(text="Flip!", callback_data="flip_btn"),
                InlineKeyboardButton(text="✅", callback_data="true_btn"),
                InlineKeyboardButton(text="Exit", callback_data="exit_btn")]
    markup.add(*layout)

    return markup


@bot.callback_query_handler(func=lambda call: call.data in callback_data)
async def callback_query(call):
    global flip_count, is_last_word
    if len(lst_data) == 1:  # listede 1 kaldıysa execute olucak
        is_last_word = True
    match call.data:

        case "wrong_btn":
            if flip_count % 2 == 0:  # Turkish tarafı çeviriliyken işlem yapamasın
                await bot.edit_message_text(text=random_word()["English"], chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=card_keyboard())

        case "flip_btn":
            flip_count += 1

            if flip_count % 2 == 1:
                await bot.edit_message_text(text=current_word["Turkish"], chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=card_keyboard())
            else:
                await bot.edit_message_text(text=current_word["English"], chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=card_keyboard())
        case "true_btn":
            if flip_count % 2 == 0:  # Turkish tarafı çeviriliyken işlem yapamasın
                lst_data.remove(current_word)
                if len(lst_data) == 1:
                    is_last_word = True
                await bot.edit_message_text(text=random_word()["English"], chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=card_keyboard())
        case "exit_btn":
            flip_count = 0  # döndürme sayısı sıfırlansın aga
            is_last_word = False
            await bot.delete_message(call.message.chat.id, call.message.message_id)

        case _:
            await bot.send_message(call.message.chat.id, "bir şeyler yanlış gitti matchcase")

@bot.message_handler(commands=["kelime"])
async def kelime_handler(message):
    global lst_data, is_last_word
    # databaseden kelimeleri bir list içine depolar ilerde bunu generator ile editle
    lst_data = get_words()
    if len(lst_data) == 1:# eğer başlangıç listesi 1 fiil ise
        is_last_word = True
    lst_data = [{"English": i[0], "Turkish":i[1]} for i in lst_data]
    await bot.send_message(message.chat.id, random_word()["English"], reply_markup=card_keyboard())


@bot.message_handler(regexp="^(/ekle)\s(kelime)")
async def kelime_ekle(message):
    input = message.text.strip().split()
    if len(input) == 4:
        eng = input[2]
        tr = input[3]
        add_new_word(eng, tr)
        await bot.reply_to(message, f"yeni kelime başarıyla eklendi: {eng}-{tr}")
    else:
        await bot.reply_to(message, "yeni kelime eklemek için:\n/ekle kelime <ingilizce> <türkçe>")


@bot.message_handler(regexp="^(/sil)\s(kelime)")
async def kelime_sil(message):
    input = message.text.strip().split()
    if len(input) == 4:
        eng = input[2]
        tr = input[3]
        delete_word(eng, tr)
        await bot.reply_to(message, f"kelime başarıyla silindi: {eng}-{tr}")
    else:
        await bot.reply_to(message, "kelimeyi silmek için:\n/sil kelime <ingilice> <türkçe>")

@bot.message_handler(regexp="^(/bul)\s(kelime)")
async def kelime_bul(message):
    input = message.text.strip().split()
    if (len(input)) == 3:
        word = input[-1]
        lst = find_word(word)#listenin içinde istenilen kelimeler tuple içinde
        for i in lst:
            await bot.reply_to(message, f"İngilizce:{i[0]}--Türkçe:{i[1]}\n")
    else:
        await bot.reply_to(message, "kelimeyi bulmak için:\n/bul kelime <ingilice veya türkçe>")
        

# TODO
# büyük kelime haznesi olucağı için generators öğren buraya uygula
# ileri seviye async öğren ve db ile iletişim ve bot reply olayını kısa süreye düşürmeye çalış
# DATABASEDEN KELİME SAYISI 0 ALINIRSA DİYE BİR SENARYO YAZ