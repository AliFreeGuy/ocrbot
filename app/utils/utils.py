
from pyrogram.errors import UserNotParticipant
import jdatetime
import re
from utils.cache import cache
import jdatetime
import datetime
from .logger import logger
import jdatetime
import os
import uuid
import hashlib
from pyrogram.types import Message
from pyrogram.file_id import FileId
from typing import Any, Optional, Union
from pyrogram.raw.types.messages import Messages
from datetime import datetime
from pyrogram.types import InlineKeyboardButton , InlineKeyboardMarkup , ReplyKeyboardMarkup , KeyboardButton
import re

from pyrogram.errors import UserNotParticipant
from utils.cache import cache
from utils import logger
import datetime
import random
import config
from datetime import datetime, timedelta
import requests
from urllib.parse import unquote
from config import DEBUG
import re
import os


PROXY_SCHEME = os.getenv('PROXY_SCHEME')
PROXY_HOSTNAME = os.getenv('PROXY_HOSTNAME')
PROXY_PORT = os.getenv('PROXY_PORT')

r = cache.redis

proxies = {
        'http': f'{PROXY_SCHEME}://{PROXY_HOSTNAME}:{PROXY_PORT}',
        'https': f'{PROXY_SCHEME}://{PROXY_HOSTNAME}:{PROXY_PORT}'
}



def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)




def b_to_mb(data):
    file_size_in_megabytes = data / (1024 * 1024)
    file_size = (f"{file_size_in_megabytes:.2f}")
    return float(file_size)


def delet_dir(path):
        os.system(f"rm -rf {path}")

def random_code():
    return uuid.uuid4()

def m_to_g(data):
    try :
        number = data
        result = number / 1000
        formatted_result = "{:.1f}".format(result)
        return formatted_result
    except Exception as e : print('m to g utils  ' , str(e))

def jdate(date_miladi):
    try :
        try :date_time = jdatetime.datetime.strptime(date_miladi, "%Y-%m-%dT%H:%M:%S.%fZ")
        except : date_time = jdatetime.datetime.strptime(date_miladi, "%Y-%m-%dT%H:%M:%SZ")
        date_shamsi = jdatetime.datetime.fromgregorian(datetime=date_time).replace(hour=0, minute=0, second=0, microsecond=0)
        current_date_shamsi = jdatetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        remaining_days = (date_shamsi - current_date_shamsi).days
        date = date_shamsi.strftime('%Y-%m-%d').split('-')
        date = f'{date[2]}-{date[1]}-{date[0]}'
        result = {
            'date': date,
            'day': remaining_days
        }
        return result
    except Exception as e : print('jdate utils ' , str(e))




def file_checker(unique_id , quality):
    vids_data = [cache.redis.hgetall(i) for i in cache.redis.keys(f'vid_data:*')]
    vid_data = None 
    for vid in vids_data :
        if vid.get('unique_id') == unique_id and vid.get('quality') == quality and vid.get('file_id') :
            vid_data = vid
    return vid_data




async def join_checker(cli , msg , channels ):
    my_channels = channels
    not_join = []
    for channel in my_channels : 
        try :  
            data = await cli.get_chat_member(int(channel.chat_id), msg.from_user.id )
        except UserNotParticipant :
            not_join.append(channel)
            continue
        except Exception as e  :
            continue
    return not_join




async def alert(client ,call , msg = None ):
    try :
        if msg is None : await call.answer('خطا لطفا دوباره تلاش کنید', show_alert=True)
        else : await call.answer(msg , show_alert = True)
    except Exception as e : logger.error(e)
    
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   



async def parse_file_id(message: "Message") -> Optional[FileId]:
    media = get_media_from_message(message)
    if media:
        return FileId.decode(media.file_id)

async def parse_file_unique_id(message: "Messages") -> Optional[str]:
    media = get_media_from_message(message)
    if media:
        return media.file_unique_id  

async def get_file_ids(message : Message) -> Optional[FileId]:
    if message.empty:
        raise None
    media = get_media_from_message(message)
    file_unique_id = await parse_file_unique_id(message)
    file_id = await parse_file_id(message)
    file_size_mb = round(getattr(media, "file_size", 0) / (1024 * 1024), 2)
    setattr(file_id, "file_size", file_size_mb)
    setattr(file_id, "mime_type", getattr(media, "mime_type", ""))
    setattr(file_id, "file_name", getattr(media, "file_name", ""))
    setattr(file_id, "duration", getattr(media, "duration", ""))
    setattr(file_id, "unique_id", file_unique_id)
    
    file_dict = {
        "file_size": file_size_mb,
        "mime_type": getattr(media, "mime_type", ""),
        "file_name": getattr(media, "file_name", ""),
        "duration": getattr(media, "duration", ""),
        "unique_id": file_unique_id
    }
    
    return file_id, file_dict

def get_media_from_message(message: "Message") -> Any:
    media_types = (
        "audio",
        "document",
        "photo",
        "sticker",
        "animation",
        "video",
        "voice",
        "video_note",
    )
    for attr in media_types:
        media = getattr(message, attr, None)
        if media:
            return media


def get_hash(media_msg: Union[str, Message], length: int = 6) -> str:
    if isinstance(media_msg, Message):
        media = get_media_from_message(media_msg)
        unique_id = getattr(media, "file_unique_id", "")
    else:
        unique_id = media_msg
    long_hash = hashlib.sha256(unique_id.encode("UTF-8")).hexdigest()
    return long_hash[:length]




def get_name(media_msg: Union[Message, FileId]) -> str:

    if isinstance(media_msg, Message):
        media = get_media_from_message(media_msg)
        file_name = getattr(media, "file_name", "")

    elif isinstance(media_msg, FileId):
        file_name = getattr(media_msg, "file_name", "")

    if not file_name:
        if isinstance(media_msg, Message) and media_msg.media:
            media_type = media_msg.media.value
        elif media_msg.file_type:
            media_type = media_msg.file_type.name.lower()
        else:
            media_type = "file"

        formats = {
            "photo": "jpg", "audio": "mp3", "voice": "ogg",
            "video": "mp4", "animation": "mp4", "video_note": "mp4",
            "sticker": "webp"
        }

        ext = formats.get(media_type)
        ext = "." + ext if ext else ""

        date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{media_type}-{date}{ext}"

    return file_name








def get_url_info(url, filename=None):

    try:


        if DEBUG == 'True':response = requests.get(url, stream=True, timeout=5, proxies=proxies, allow_redirects=True)
        else:response = requests.get(url, stream=True, timeout=5, allow_redirects=True)
        main_file_size = int(response.headers.get('content-length', 0))

        if filename is None:
            content_disposition = response.headers.get('Content-Disposition')

            try :
                if content_disposition:filename = unquote(content_disposition.split("filename=")[1])
                else:filename = url.split('/')[-1]
            except : filename = url.split('/')[-1]

        data = {
                    'file_name': filename.replace('"' , ''),
                    'file_size_str': sizeof_fmt(main_file_size),
                    'file_size': main_file_size / (1024 * 1024),
                  }
        
        if main_file_size != 0:
            return data
        return None
    


    except Exception as e:
        print(e)
        return None
    
    
    

def url_getter(text ):
    pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    matches = re.findall(pattern, text , re.MULTILINE | re.IGNORECASE)
    return matches








async def get_thumb(chat_id , msg_id , bot ) : 
    
    try :
        thumb  = await bot.get_messages(int(chat_id), int(msg_id))
        if thumb : 
            return thumb
        return None 
    except : 
        return None



def seconds_to_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours}:{minutes}:{seconds}"





def add_change( file_id, change_field):
    cache.redis.sadd(f"{file_id}:changes", change_field)
    return True

def all_changes( file_id):
    return list(cache.redis.smembers(f"{file_id}:changes"))



def delete_change(file_id, change_field):
    cache.redis.srem(f"{file_id}:changes", change_field)
    return True

def delete_all_changes(file_id):
    cache.redis.delete(f"{file_id}:changes")
    return True