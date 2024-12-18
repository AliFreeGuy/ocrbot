
from django.db.models.signals import pre_save ,post_save
from django.dispatch import receiver
from .models import SendMessageModel , Setting , User
from core.tasks import send_message
import asyncio
from django.conf import settings
from pyrogram import Client
from core.logger import logger
from core.tasks import send_message_for_user


@receiver(post_save, sender=SendMessageModel)
def create_send_message_task(sender, instance, created, **kwargs):
    if created: 
        send_message.delay_on_commit(instance.id)




@receiver(pre_save, sender=Setting)
def generate_session_string_setting(sender, instance, **kwargs):
    loop = asyncio.new_event_loop() 
    asyncio.set_event_loop(loop)  
    session_string = loop.run_until_complete(async_generate_session_string(instance))
    instance.session_string = session_string


async def async_generate_session_string(instance):
    try :
        if settings.DEBUG:
            bot = Client(
                'create-session-string',
                api_hash=instance.api_hash,
                api_id=instance.api_id,
                bot_token=instance.bot_token,
                proxy=settings.PROXY
                
            )
        else:
            bot = Client(
                'create-session-string',
                api_hash=instance.api_hash,
                api_id=instance.api_id,
                bot_token=instance.bot_token
            )

        async with bot:
            session_string = await bot.export_session_string()
            return session_string
    except Exception as e :
        logger.error(str(e))
        
        
        


@receiver(pre_save, sender=User)
def user_pre_save(sender, instance, **kwargs):
    try:
        
        old_instance = sender.objects.get(id=instance.id)
    except sender.DoesNotExist:
        old_instance = None

    if old_instance and old_instance.coin != instance.coin:

        if int(instance.coin) < int(old_instance.coin) : 
            text = instance.lang.inc_coin_text
            text.replace('$user' , instance.full_name)
            text.replace('$new_coin' , str(instance.coin))
            text.replace('$old_coin' , str(old_instance.coin))
            send_message_for_user.delay_on_commit(message = text , chat_id = instance.chat_id)
        
        elif int(instance.coin) > int(old_instance.coin) : 
            text = instance.lang.dec_coin_text
            text.replace('$user' , instance.full_name)
            text.replace('$new_coin' , str(instance.coin))
            text.replace('$old_coin' , str(old_instance.coin))
            send_message_for_user.delay_on_commit(message = text , chat_id = instance.chat_id)
            

        
        
