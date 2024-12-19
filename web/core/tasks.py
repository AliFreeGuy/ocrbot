
from celery import shared_task

from pyrogram import Client 
from django.conf import settings
from core import models
import logging
import os

logger = logging.getLogger('tasks')


@shared_task
def send_message(message_id) :
    
    setting = models.Setting.objects.first()
    message = models.SendMessageModel.objects.get(id = message_id)
    
    if settings.DEBUG:
        bot = Client(
                'send_message_task',
                api_hash=setting.api_hash,
                api_id=int(setting.api_id),
                session_string=setting.session_string,
                proxy=settings.PROXY,
                in_memory  = True
                
                
            )
    else:
        bot = Client(
                'send_message_task',
            api_hash=setting.api_hash,
            api_id=int(setting.api_id),
            session_string=setting.session_string,
            in_memory  = True
        )
    
    
    
    with bot :
        
        users = message.users.all() if message.users.all() else models.User.objects.all()
        if message.message.startswith('https://t.me/c/') :
            chat_id = int(f'-100{message.message.replace("https://t.me/c/","").split("/")[0]}')
            message_id = int(f'{message.message.replace("https://t.me/c/","").split("/")[1]}')
            msg = bot.get_messages(chat_id=chat_id  ,message_ids=message_id)
            for user in users :
                try :
                    
                    if message.is_forward :
                        msg.forward(user.chat_id)
                    else :
                        msg.copy(user.chat_id)
                except Exception as e:
                    logger.error(e)
                    continue
                    
                    
        else :
            
            text = message.message
            for user in  users :
                try :
                    bot.send_message(chat_id=user.chat_id ,text = text)
                except Exception as e :
                    logger.error(str(e))
                    continue
                            
            
                
    
    
@shared_task
def send_message_for_user(message , chat_id) : 
    setting = models.Setting.objects.first()

    if settings.DEBUG:
        bot = Client(
                's',
                api_hash=setting.api_hash,
                api_id=int(setting.api_id),
                session_string=setting.session_string,
                proxy=settings.PROXY,
                in_memory  = True
                
                
                
            )
    else:
        bot = Client(
            's',
            api_hash=setting.api_hash,
            api_id=int(setting.api_id),
            session_string=setting.session_string,
            in_memory  = True
            
        )
    
    
    with bot : 
          
        bot.send_message(chat_id=int(chat_id) , text = message)
        
        
        
        
        
    
    
@shared_task
def workflow_amount_checker_task() : 
    workflows = models.WorkFlowModel.objects.filter(is_active = True)
    print(workflows)