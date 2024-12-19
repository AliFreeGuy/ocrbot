
    
    
    
    
    
    
    
    
# from pyrogram import Client, filters
# from utils import cache , logger , btn,txt
# from utils import filters as f
# import config
# from utils.utils import join_checker
# from .main_handlers import handlers
# from utils.utils import alert

# @Client.on_message(filters.private, group=3)
# async def invite_checker(client, message):
    
#     try : 
#         if message.text and len(message.text.split(' ')) == 2 and message.text.split(' ')[0] == '/start' and message.text.split(' ')[1].startswith('ref_') :
#             new_user = int(message.from_user.id)
#             inviter = int(message.text.split(' ')[1].replace('ref_', ''))
#             redis = cache.redis
#             user_invite_key = f'user_invite:{new_user}'
#             inviter_exists = redis.get(user_invite_key)
#             user = config.con.user(chat_id=int(inviter))
#             setting = config.con.setting
            
            
#             if inviter_exists:
#                 await client.send_message(inviter,user.lang.inviter_has_alredy_invited_text.replace('user' ,message.from_user.first_name))
#                 await client.send_message(new_user,user.lang.user_has_alredy_invited_text)
#             else:
#                 if new_user != inviter:
#                     user_key = f'invite:{str(inviter)}:{str(new_user)}'
#                     exists = redis.exists(user_key)

#                     if not exists:
#                         redis.set(user_key, 'no') 
#                         redis.set(user_invite_key, inviter) 
#                         user = config.con.user(chat_id=int(inviter)  , daili_volume = user.daili_volume + int(setting.settings.ref_volume))
#                         await client.send_message( inviter,user.lang.user_invite_ref_text.replace('volume'  , str(setting.settings.ref_volume)))

#             message.text = '/start'
#             await handlers(client, message)
            
            
#     except Exception as e : 
#         logger.warning(str(e))
#         await handlers(client, message)
#         return





# @Client.on_message(filters.private, group=4)
# async def force_member_info(client, message):
#     if message.text and len(message.text.split(' ')) == 2 and message.text.split(' ')[0] == '/start' and message.text.split(' ')[1].startswith('force_') :
#         setting = config.con.setting
#         hash = message.text.replace('/start force_' , '')
#         force_channels = setting.force_channels
    
#         for channel in force_channels : 
            
#             if hash == channel.hash_info : 
#                 await message.reply(text = txt.generate_channel_report(channel) , quote = True)
        


# @Client.on_message(filters.private & f.user_not_active , group=0)
# async def user_not_active(bot, msg):
#     user = config.con.user(chat_id=msg.from_user.id )
#     setting = config.con.setting
#     await msg.reply_text(user.lang.user_not_active_text ,quote=True ,reply_markup = btn.upgrade_btn(user=user , setting=setting))
    
    
    
    
    
# @Client.on_message(filters.private & f.user_not_join , group=0)
# async def user_not_join(bot, msg):
#     user = config.con.user(chat_id=msg.from_user.id )
#     setting = config.con.setting
#     channels = []
   
#     force_channels = setting.force_channels
#     for ch in force_channels : 
#         if ch.is_active : 
#             channels.append(ch.channel)
    
#     channels = await join_checker(bot , msg , channels )
#     await msg.reply_text(user.lang.user_not_join_text ,quote=True , reply_markup =btn.join_channel(channels=channels , user = user))


# @Client.on_callback_query( f.user_not_join , group=0)
# async def user_not_join_call(bot, msg):
#     await bot.delete_messages(msg.from_user.id , msg.message.id )
#     user = config.con.user(chat_id=msg.from_user.id )
#     setting = config.con.setting
#     channels = []
#     force_channels = setting.force_channels
#     for ch in force_channels : 
#         if ch.is_active : 
#             channels.append(ch.channel)
    
#     channels = await join_checker(bot , msg , channels )
#     await alert(bot , msg , msg = user.lang.user_not_join_text)
#     await bot.send_message(chat_id =msg.from_user.id , text = user.lang.user_not_join_text  , reply_markup =btn.join_channel(channels=channels , user = user))

    
    
    
    
    
    
# @Client.on_message(filters.channel  , group=0)
# async def download_content_forwarder(b , m ) :
#     setting = config.con.setting
#     if setting.settings.backup_channel and int(m.chat.id) == int(setting.settings.backup_channel.chat_id) :
#         if m.media and m.caption :
#             user = int(m.caption.split(':')[1])
#             m.caption = None 
#             await m.copy(user)
            
