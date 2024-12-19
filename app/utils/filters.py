from pyrogram import filters
from utils.utils import join_checker
import config




async def user_is_active(_ , cli , msg ):
    user = config.con.user(chat_id=msg.from_user.id , full_name = msg.from_user.first_name)
    if user and user.is_active :
        return True
    return False



async def user_not_active(_ , cli , msg ) :
    user = config.con.user(chat_id=msg.from_user.id , full_name = msg.from_user.first_name)
    if user and not user.is_active :
        return True
    return False
    






async def user_is_join(_ , cli , msg ):
    channels = config.con.setting.channels
    is_join = await join_checker(cli , msg , channels)
    if not is_join : return True
    return False




async def user_not_join(_ , cli , msg ):
    channels = config.con.setting.channels
    is_join = await join_checker(cli , msg , channels)
    if not is_join : return False
    return True




user_not_join=filters.create(user_not_join)
user_is_join = filters.create(user_is_join)
user_is_active = filters.create(user_is_active)
user_not_active = filters.create(user_not_active)