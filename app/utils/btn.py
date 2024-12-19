from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineKeyboardButton , KeyboardButton , WebAppInfo)
import config
from utils.utils import add_change , all_changes



def join_channel(channels , user  ):
    buttons = []
    
    for channel in channels :
        buttons.append([InlineKeyboardButton(text=channel.name , url = channel.url )])
    buttons.append([InlineKeyboardButton(text=user.lang.joined_btn,callback_data='joined')])
    return InlineKeyboardMarkup(buttons)









def user_panel_menu(setting , user ):
    setting_text = f'{user.lang.setting_btn}'
    help_text = f'{user.lang.help_btn}'
    support_text = f'{user.lang.support_btn}'
    profile_text = f'{user.lang.profile_btn}'
    plans_text = f'{user.lang.buy_btn}'
    
    marks = [
        [plans_text],
        [setting_text, profile_text],
        [help_text, support_text],]
    
    
    
    for ads in setting.ads:
        if not ads.text.startswith('https://t.me/') and ads.text.startswith('https://'):
            miniapp_url = WebAppInfo(url=ads.text)
            marks.insert(0, [KeyboardButton(ads.name, web_app=miniapp_url)])
        
        else : 
            marks.insert(0, [KeyboardButton(ads.name)])

    return ReplyKeyboardMarkup(marks, resize_keyboard=True, placeholder=user.lang.placeholder_text)

    
    
    


def upgrade_btn(setting , user  ) : 
    url = WebAppInfo(url = f'{setting.settings.upgrade_url}/upgrade/?chat_id={str(user.chat_id)}')
    return InlineKeyboardMarkup([[InlineKeyboardButton(text = user.lang.upgrade_btn_text , web_app=url)]])




def setting_btn(setting , user ) : 
    buttons = []
    buttons.append([InlineKeyboardButton(text=user.lang.change_lang_btn,callback_data=f'setting:change_lang_btn'),])
    buttons.append([InlineKeyboardButton(text=user.lang.thumbnail_btn,callback_data=f'setting:thumbnail_btn'),])
    buttons.append([InlineKeyboardButton(text=f'{"☑️ " if user.resize_thumbnail_to_video else "⬜️ "} {user.lang.resize_thumbnail_to_video_btn}',callback_data=f'setting:resize_thumbnail_to_video'),])
    buttons.append([InlineKeyboardButton(text=user.lang.back_btn,callback_data=f'setting:back_to_start'),])
    return InlineKeyboardMarkup(buttons)



def cancel_uploader_btn(user , task_id) :
    buttons = [[InlineKeyboardButton(text=user.lang.cancel_btn_text ,callback_data=f'cancel_uploader:{str(task_id)}')]]
    return InlineKeyboardMarkup(buttons)

def cancel_downloader_btn(user  ,cancel_id) :
    buttons = [[InlineKeyboardButton(text=user.lang.cancel_btn_text ,callback_data=f'cancel_downloader:{str(cancel_id)}')]]
    return InlineKeyboardMarkup(buttons)





def thumbnail_manager(user , setting ) :
    buttons = []
    buttons.append([InlineKeyboardButton(text=user.lang.get_thumbnail_btn,callback_data=f'setting:get_thumbnail_btn'),])
    buttons.append([InlineKeyboardButton(text=user.lang.change_thumbnail_btn,callback_data=f'setting:change_thumbnail_btn'),])
    if user.default_thumbnail :
        buttons.append([InlineKeyboardButton(text=user.lang.remove_thumbnail_btn,callback_data=f'setting:remove_thumbnail_btn'),])
    buttons.append([InlineKeyboardButton(text=user.lang.back_btn,callback_data=f'setting:back_to_setting'),])
    return InlineKeyboardMarkup(buttons)
    


def change_lang_btn(setting , user ) :
    buttons = []
    for text in setting.texts :
        if text.lang_code == user.lang.lang_code :buttons.append(InlineKeyboardButton(text=f'▪️ {text.lang_name}',callback_data=f'setting:set_lang:{text.lang_code}'))
        else :buttons.append(InlineKeyboardButton(text=f'▫️ {text.lang_name}',callback_data=f'setting:set_lang:{text.lang_code}'))
    buttons_two_by_two = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    buttons_two_by_two.append([InlineKeyboardButton(text=user.lang.back_btn,callback_data=f'setting:back_to_setting'),])
    return InlineKeyboardMarkup(buttons_two_by_two)





    
def get_file(key , data , user ):
    get_auto  = '☑️' if data['auto_file_format'] == 'True' else '⬜️'
    get_file = '☑️' if data['auto_file_format'] == 'False' else '⬜️'
    buttons = [
        [InlineKeyboardButton(text=user.lang.dl_change_name_btn,callback_data=f'{key}-dl_change_name_btn')],
        [InlineKeyboardButton(text=user.lang.dl_change_thumb_btn,callback_data=f'{key}-dl_change_thumb_btn')],
        [InlineKeyboardButton(text=user.lang.dl_transfer_to_link_btn,callback_data=f'{key}-dl_transfer_to_link_btn')],
        [InlineKeyboardButton(text=f'{get_auto} {user.lang.dl_get_auto_file_btn}',callback_data=f'{key}-dl_get_auto_file_btn')],
        [InlineKeyboardButton(text=f'{get_file} {user.lang.dl_get_file_btn}',callback_data=f'{key}-dl_get_file_btn')],
        [InlineKeyboardButton(text=user.lang.dl_start_get_file_btn,callback_data=f'{key}-dl_start_get_file_btn')],
        ]
    
    if data['thumb'] != 'none' : 
        buttons.insert(2 , [InlineKeyboardButton(text=user.lang.dl_get_thumb_btn,callback_data=f'{key}-dl_get_thumb_btn')],)
    
    return InlineKeyboardMarkup(buttons)






def up_voice_btn(user ,data  ) : 
    changes = all_changes(data['key'])
    
    buttons = [
        [InlineKeyboardButton(text=user.lang.up_change_name_btn,callback_data=f'{data['key']}-up_change_name_btn')],
        
        *(
            [[InlineKeyboardButton(text=user.lang.up_get_telegram_file_btn, callback_data=f'{data["key"]}-up_get_telegram_file_btn')]]
            if changes  else []
        ),
        
        
        [InlineKeyboardButton(text=user.lang.up_get_download_link_btn,callback_data=f'{data['key']}-up_get_download_link_btn')],
        ]
    
    
    return InlineKeyboardMarkup(buttons)




def up_photo_btn(user , data) : 
    buttons = [[InlineKeyboardButton(text=user.lang.up_get_download_link_btn,callback_data=f'{data['key']}-up_get_download_link_btn')],]
    return InlineKeyboardMarkup(buttons)


def up_document_btn(user, data):
    get_auto = '☑️' if data['up_get_auto_file_btn'] == 'True' else '⬜️'
    changes = all_changes(data['key'])
    
    buttons = [
        [InlineKeyboardButton(text=user.lang.up_change_name_btn, callback_data=f'{data["key"]}-up_change_name_btn')],
        [InlineKeyboardButton(text=user.lang.up_set_thumb_btn, callback_data=f'{data["key"]}-up_set_thumb_btn')],
        
        *(
            [[InlineKeyboardButton(text=user.lang.up_get_thumb_btn, callback_data=f'{data["key"]}-up_get_thumb_btn')]]
            if data.get('thumb', None) not in ['none', None] else []
        ),
                
        [InlineKeyboardButton(text=f'{get_auto} {user.lang.up_get_auto_file_btn}', callback_data=f'{data["key"]}-up_get_auto_file_btn')],
    
        *(
            [[InlineKeyboardButton(text=user.lang.up_get_telegram_file_btn, callback_data=f'{data["key"]}-up_get_telegram_file_btn')]]
            if changes  else []
        ),
        
        
        [InlineKeyboardButton(text=user.lang.up_get_download_link_btn, callback_data=f'{data["key"]}-up_get_download_link_btn')],
    ]

    return InlineKeyboardMarkup(buttons)




def up_audio_btn(user , data ) :
    changes = all_changes(data['key'])
    buttons = [
        [InlineKeyboardButton(text=user.lang.up_change_name_btn, callback_data=f'{data["key"]}-up_change_name_btn')],
        [InlineKeyboardButton(text=user.lang.up_set_thumb_btn, callback_data=f'{data["key"]}-up_set_thumb_btn')],
        
        *(
            [[InlineKeyboardButton(text=user.lang.up_get_thumb_btn, callback_data=f'{data["key"]}-up_get_thumb_btn')]]
            if data.get('thumb', None) not in ['none', None] else []
        ),
                
        [
            InlineKeyboardButton(text=user.lang.up_change_singer_name_btn, callback_data=f'{data["key"]}-up_change_singer_name_btn'),
            InlineKeyboardButton(text=user.lang.up_change_muzic_name_btn, callback_data=f'{data["key"]}-up_change_muzic_name_btn')
        ],
    
    
    
        *(
            [[InlineKeyboardButton(text=user.lang.up_get_telegram_file_btn, callback_data=f'{data["key"]}-up_get_telegram_file_btn')]]
            if changes  else []
        ),
        
        
        [InlineKeyboardButton(text=user.lang.up_get_download_link_btn, callback_data=f'{data["key"]}-up_get_download_link_btn')],
    ]

    return InlineKeyboardMarkup(buttons)







def up_video_btn(user , data ) :
    changes = all_changes(data['key'])

    buttons = [
        [InlineKeyboardButton(text=user.lang.up_change_name_btn, callback_data=f'{data["key"]}-up_change_name_btn')],
        [InlineKeyboardButton(text=user.lang.up_set_thumb_btn, callback_data=f'{data["key"]}-up_set_thumb_btn')],
        [InlineKeyboardButton(text=user.lang.up_get_thumb_btn, callback_data=f'{data["key"]}-up_get_thumb_btn')],

        
        *(
            [[InlineKeyboardButton(text=user.lang.up_get_telegram_file_btn, callback_data=f'{data["key"]}-up_get_telegram_file_btn')]]
            if changes  else []
        ),
        
        
        [InlineKeyboardButton(text=user.lang.up_get_download_link_btn, callback_data=f'{data["key"]}-up_get_download_link_btn')],
    ]
    
    
    if data.get('softsub' , None ) not in ['none' , None ] : 
        buttons.insert(3 , [InlineKeyboardButton(text=user.lang.up_change_suftsub_video_btn, callback_data=f'{data["key"]}-up_change_suftsub_video_btn')])
    else :
        buttons.insert(3 , [InlineKeyboardButton(text=user.lang.up_set_softsub_video_btn, callback_data=f'{data["key"]}-up_set_softsub_video_btn')])
    return InlineKeyboardMarkup(buttons)