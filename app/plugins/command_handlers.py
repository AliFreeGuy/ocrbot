from pyrogram import Client, filters
from utils import logger
from utils import cache
from config import con

@Client.on_message(filters.command('start')  , group = 2)
async def say_hello(bot, msg):
    user = con.user(chat_id=msg.from_user.id , full_name=msg.from_user.first_name)
    await bot.send_message(msg.from_user.id ,user.lang.start_text )
    
    
    
    
    