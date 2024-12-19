from pyrogram import Client, filters
from utils import logger
from utils import cache
from utils import filters as f 
from config import con

@Client.on_message(f.user_is_join & f.user_is_active   , group = 2)
async def handlers(bot, msg):
    
    

    if msg.text  :
        
        user = con.user(chat_id=msg.from_user.id , full_name = msg.from_user.first_name )
        setting = con.setting
    
        # if msg.text == '/start' : 
        #     await start_handler(bot , msg ,user , setting )
        
        # elif msg.text == '/privacy' : 
        #     await privacy_handler(bot , msg , user , setting )
        
        # elif msg.text == '/upgrade' : 
        #     await upgrade_handler(bot , msg , user , setting )
        
        # elif msg.text == '/setting' : 
        #     await setting_handler(bot , msg , user , setting)
        
        # elif msg.text == '/default_thumbnail' :
        #     await msg.reply_text(quote  =True , text = user.lang.thumbnail_manager_text , reply_markup = btn.thumbnail_manager(user=user , setting=setting ))

        # elif msg.text in ['/usage' , '/profile'] : 
        #     await usage_handler(bot , msg , user , setting )
        
        # elif msg.text == '/free' : 
        #     await free_volume(bot , msg ,user , setting)
        

    