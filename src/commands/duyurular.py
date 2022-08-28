from bs4 import BeautifulSoup
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

import requests

from src.objects import bot

TARGET_URL = "https://www.firat.edu.tr/tr"
locat_index = 0
comms = ["ileri", "geri", "exit_s", "en_bas", "en_son"]

def scrape_target():#gerekli datayı hedef siteden çekiyoruz.
    with requests.Session() as session:
        with session.get(url=TARGET_URL) as response:
            response.raise_for_status()

            html = response.text
    soup = BeautifulSoup(html, "html.parser")
    lst = soup.select(".swiper-wrapper h5 a")
    announcements_link = [i.get("href") for i in lst]
    announcements_text = [x.getText().strip() for x in lst]
    return announcements_link, announcements_text


def keyboard_markup():# inline keyboard remove felan var onu öğren belki daha iidir
    markup = InlineKeyboardMarkup()
    markup.row_width = 8
    link_btn = InlineKeyboardButton("Duyuruya gitmek için tıklayın", url=ann_data[0][locat_index],callback_data="lnk_btn")
    markup.add(link_btn)
    
    exit_btn = InlineKeyboardButton("Duyuruları kapatmak için tıklayın",callback_data="exit_s")
    markup.add(exit_btn)
    if locat_index == len(ann_data[1])-1:
        layout = [InlineKeyboardButton("<<1",callback_data="en_bas"),
                  InlineKeyboardButton(f"<{locat_index}",callback_data="geri"),
                  InlineKeyboardButton(f"·{locat_index+1}·", callback_data="guncel"),
                  InlineKeyboardButton(" ",callback_data="bos"),
                  InlineKeyboardButton(" ", callback_data="bos")]
    elif locat_index == 0:
        layout = [InlineKeyboardButton(" ",callback_data="bos"),
                  InlineKeyboardButton(" ",callback_data="bos"),
                  InlineKeyboardButton(f"·{locat_index+1}·", callback_data="guncel"),
                  InlineKeyboardButton(">",callback_data="ileri"),
                  InlineKeyboardButton(f"{len(ann_data[1])}>>", callback_data="en_son")]
    else:
        layout = [InlineKeyboardButton("<<1",callback_data="en_bas"),
                  InlineKeyboardButton(f"<{locat_index}",callback_data="geri"),
                  InlineKeyboardButton(f"·{locat_index+1}·", callback_data="guncel"),
                  InlineKeyboardButton(f"{locat_index+2}>",callback_data="ileri"),
                  InlineKeyboardButton(f"{len(ann_data[1])}>>", callback_data="en_son")]
    
    markup.add(*layout)
    return markup

#buga girerse constant yapma locat indexi normal var yap
@bot.callback_query_handler(func=lambda call: call.data in comms)
async def scrape_buttons(call):
    global locat_index
    
    match call.data:
        
        case "ileri":
            locat_index += 1
            await bot.edit_message_text(text=f"{ann_data[1][locat_index]}",
                                        chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        reply_markup=keyboard_markup())
        case "geri":
            locat_index -= 1
            await bot.edit_message_text(text=f"{ann_data[1][locat_index]}",
                                        chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        reply_markup=keyboard_markup())
        case "exit_s":
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        case "en_bas":
            locat_index = 0
            await bot.edit_message_text(text=f"{ann_data[1][locat_index]}",
                                        chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        reply_markup=keyboard_markup())
        case "en_son":
            locat_index = len(ann_data[1])-1
            await bot.edit_message_text(text=f"{ann_data[1][locat_index]}",
                                        chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        reply_markup=keyboard_markup())
        case _:
            raise AssertionError ("kral hata var")
@bot.message_handler(commands=["duyurular"])
async def get_announcements(message):
    global ann_data# duyurular komutu başladığı an datayı bu değişkene atıyoruz ([links], [texts])
    global locat_index
    locat_index = 0# her duyurular komutu execute olduğunda baştan başlıcak duyurulara
    ann_data = scrape_target()

    await bot.send_message(message.chat.id, f"{locat_index + 1}){ann_data[1][locat_index]}", reply_markup=keyboard_markup())
    