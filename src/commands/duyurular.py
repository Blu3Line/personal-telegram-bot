from bs4 import BeautifulSoup
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

import requests

from src.objects import bot

TARGET_URL = "https://www.firat.edu.tr/tr"
LOCAT_INDEX = 0
comms = ["ileri", "geri", "exit_s"]

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
    link_btn = InlineKeyboardButton("Duyuruya gitmek için tıklayın", url=ann_data[0][LOCAT_INDEX],callback_data="lnk_btn")
    markup.add(link_btn)
    
    exit_btn = InlineKeyboardButton("Duyuruları kapatmak için tıklayın",callback_data="exit_s")
    markup.add(exit_btn)
    if LOCAT_INDEX == len(ann_data[1])-1:
        layout = [InlineKeyboardButton("<",callback_data="geri")]
    elif LOCAT_INDEX == 0:
        layout = [InlineKeyboardButton(">",callback_data="ileri")]
    else:
        layout = [InlineKeyboardButton("<",callback_data="geri"),
                  InlineKeyboardButton(">",callback_data="ileri")]
    
    markup.add(*layout)
    return markup

#buga girerse constant yapma locat indexi normal var yap
@bot.callback_query_handler(func=lambda call: call.data in comms)
async def scrape_buttons(call):
    global LOCAT_INDEX
    
    match call.data:
        
        case "ileri":
            LOCAT_INDEX += 1
            await bot.edit_message_text(text=f"{LOCAT_INDEX + 1}){ann_data[1][LOCAT_INDEX]}",
                                        chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        reply_markup=keyboard_markup())
        case "geri":
            LOCAT_INDEX -= 1
            await bot.edit_message_text(text=f"{LOCAT_INDEX + 1}){ann_data[1][LOCAT_INDEX]}",
                                        chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        reply_markup=keyboard_markup())
        case "exit_s":
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        case _:
            print("dbgdbdgbdg")
@bot.message_handler(commands=["duyurular"])
async def get_announcements(message):
    global ann_data# duyurular komutu başladığı an datayı bu değişkene atıyoruz ([links], [texts])
    global LOCAT_INDEX
    LOCAT_INDEX = 0# her duyurular komutu execute olduğunda baştan başlıcak duyurulara
    ann_data = scrape_target()

    await bot.send_message(message.chat.id, f"{LOCAT_INDEX + 1}){ann_data[1][LOCAT_INDEX]}", reply_markup=keyboard_markup())
    