
from .objects import bot

#commands
from .commands.start import start_message
from .commands.eng_tr_words import  callback_query, kelime_handler, kelime_ekle, kelime_sil, kelime_bul
from .commands.verbs import verb_handler, callback_query_verb
from .commands.duyurular import get_announcements
