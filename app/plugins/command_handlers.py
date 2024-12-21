from pyrogram import Client, filters
from utils import cache , btn , txt , logger
from utils import filters as f 
from config import con , API_URL
from pyrogram import Client
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton)




@Client.on_message(filters.private &f.user_is_join & f.user_is_active   , group = 2)
async def handlers(bot, msg):
    
    user = con.user(chat_id = msg.from_user.id  , full_name=msg.from_user.first_name)
    setting = con.setting
        

    btns = {
        f'{user.lang.profile_btn}': profile_handler,
        f'{user.lang.help_btn}': help_handler,
        f'{user.lang.support_btn}': support_handler,
        f'{user.lang.buy_btn}': buy_handler,
        f'{user.lang.setting_btn}': setting_handler,
        # f'{setting.texts.add_volume_with_join_btn}' : add_volume_with_join_btn_handler,
        # f'{setting.texts.add_volume_with_ref_btn}' : add_volume_with_ref_btn_handler,
        # f'{setting.texts.add_volume_with_payment_btn}'  : add_volume_with_payment_btn_handler,

        '/start' : start_handler ,
        '/help' : help_handler,
        '/support' : support_handler ,
        '/profile' :profile_handler,
        '/setting' : setting_handler,
        # '/coin' : plans_handler,
        # '/free_coin' : profile_handler,
        # '🔙' : start_handler
    }
    
    
    

    if msg and msg.text:
        handler_func = btns.get(msg.text)
        ads = setting.ads
        active_ads = [ad.name for ad in ads ]
        
        if handler_func:
            await handler_func(bot, msg, user, setting)
            
        elif msg.text in active_ads : 
            await ads_handler(bot , msg , user , setting )
        
        
            
            
            
            
async def start_handler(bot , msg , user ,setting ) : 
    await msg.reply(user.lang.start_text , reply_markup = btn.user_panel_menu(setting , user ) ,quote = True)
    
    
    
async def help_handler(bot , msg , user ,setting ) : 
    await msg.reply(user.lang.help_text , reply_markup = btn.user_panel_menu(setting , user ) ,quote = True)
      
      
      
async def support_handler(bot , msg , user ,setting ) : 
    await msg.reply(user.lang.support_text , reply_markup = btn.user_panel_menu(setting , user ) ,quote = True)
    
    
    
async def profile_handler(bot , msg , user , setting ) : 
    await msg.reply(txt.format_user_info(user), quote = True)
    
    
    
async def buy_handler(bot , msg , user , setting ) : 
    await msg.reply(user.lang.buy_text  , quote =True , reply_markup = btn.buy_handler_btn(user))
    
    
    
async def setting_handler(bot , msg , user , setting ) :
    await msg.reply(user.lang.setting_text , quote = True , reply_markup = btn.setting_btn(setting , user ))
    
    
    
async def ads_handler(bot , msg , user , setting   ) : 
    try : 
        ads = setting.ads
        active_ads = [ad.name for ad in ads ]
        if msg.text in active_ads : 
            selected_ad = next((ad for ad in ads if ad.name == msg.text), None)
            if selected_ad.text.startswith('https://t.me/') : 
                link = selected_ad.text
                parts = link.split('/')
                chat_id = f'-100{parts[-2]}'
                message_id = parts[-1]  
                ads_msg = await bot.get_messages(int(chat_id), int(message_id))
                if ads_msg : 
                    await ads_msg.copy(msg.from_user.id , reply_markup  = btn.user_panel_menu(setting , user ))
            else : 
                await msg.reply(selected_ad.text , quote = True , reply_markup  = btn.user_panel_menu(setting , user ))
    except Exception as e :
        logger.error(str(e))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
@Client.on_callback_query(f.user_is_active & f.user_is_join, group=1)
async def call_handlers(bot , call ) : 
    

    logger.info(f'callback data : {call.data}')
    
    
    if call.data :
        user = con.user(chat_id=call.from_user.id  , full_name=call.from_user.first_name)
        setting = con.setting
        status = call.data.split(':')[0]
        
        if status == 'buy' : 
            await buy_coin_handler(bot , call , user , setting )
        
        elif status == 'invite' : 
            await invite_get_coin_handler(bot , call , user , setting )
        
        elif status == 'joined' : 
            message = call.message
            message.text = '/start' 
            await handlers(bot , message)
            
        elif status == 'get_coin' : 
            await show_coin_plan_handler(bot , call , user , setting) 
        
        elif status == 'setting' : 
            await change_lang_btn_handler(bot , call , user , setting ) 
            
            
        elif status == 'back' : 
            await back_btn_manager(bot , call , user , setting )
        

    
    
    
    
    
    
    
    
    
    
    
    
async def change_lang_btn_handler(bot , call , user , setting ) :
    
    
    status = call.data.split(':')[2]
    
    
    if status == 'show' : 
        await call.message.edit_text(user.lang.change_lang_text , reply_markup = btn.change_lang_btn(setting , user))
    
    elif status != user.lang.lang_code :
        user = con.user(chat_id=call.from_user.id , full_name=call.from_user.id , lang = status)
        await bot.send_message(chat_id = call.from_user.id , text = user.lang.changed_lang_text , reply_markup = btn.user_panel_menu(setting , user))
        
        await call.message.edit_text(user.lang.change_lang_text , reply_markup = btn.change_lang_btn(setting , user))
    
    
    
    
    
async def show_coin_plan_handler(bot , call , user , setting) :
    status = call.data.split(':')
    plan_id = status[2]
    data =status[1]
    for plan in setting.plans : 
        if int(plan.id) == int(plan_id) : 
            
            if data == 'des' : 
                await call.message.edit_text(plan.des , reply_markup = btn.buy_coin(user , plan_id ))
                
            elif data ==  'rial' : 
                pay_url = con.create_payment(chat_id=call.from_user.id , plan=plan.id)
                text = f'{plan.des} \n\n{user.lang.pay_with_rial_text}'
                text = text.replace('$url' , pay_url.url)
                text = text.replace('$plan_name' , plan.name)
                text = text.replace('$plan_price' , str(plan.price_ir))
                await call.message.edit_text(text , reply_markup = btn.buy_coin(user , plan_id ))
                
            elif data == 'trx' : 
                text = f'{plan.des} \n\n{user.lang.pay_with_tron_text}'
                text = text.replace('$plan_name' , plan.name)
                text = text.replace('$plan_price' , str(plan.price_ir))
                await call.message.edit_text(text , reply_markup = btn.buy_coin(user , plan_id ))
                

            
    
async def back_btn_manager(bot ,call , user , setting ) : 
    status = call.data.split(':')[1]
    if status == 'buy' : 
        await call.message.edit_text(user.lang.buy_text , reply_markup = btn.buy_handler_btn(user))
    elif status == 'plans' : 
        await buy_coin_handler(bot , call , user , setting  )
    elif status == 'setting'  : 
        await call.message.edit_text(user.lang.setting_text  , reply_markup = btn.setting_btn(setting , user ))
        
        
        
        
        
async def buy_coin_handler(bot , call , user , setting ):
    await call.message.edit_text(user.lang.buy_text , reply_markup = btn.coin_plans_list(setting , user ))
    


async def invite_get_coin_handler(bot , call , user , setting ) : 
    await call.message.edit_text(user.lang.invite_text_1)
    invite_data  = user.lang.invite_text_2
    if isinstance(invite_data , str) : 
        user_invite_link = f'\n\nhttps://t.me/{setting.setting.bot_username}?start=ref_{call.from_user.id}'
        chat_id = int(f'-100{invite_data.replace("https://t.me/c/","").split("/")[0]}')
        message_id = int(f'{invite_data.replace("https://t.me/c/","").split("/")[1]}')
        msg = await bot.get_messages(chat_id=chat_id  ,message_ids=message_id)
        invite_msg_user = await msg.copy(call.from_user.id )
        await invite_msg_user.edit_text(user_invite_link)
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


@Client.on_inline_query()
async def answer(client, inline_query):
    
    setting = con.setting
    user = con.user(chat_id=inline_query.from_user.id , full_name=inline_query.from_user.first_name)
    user_invite_link = f'https://t.me/{setting.setting.bot_username}?start=ref_{inline_query.from_user.id}'

    thumb_url = f"{API_URL.rstrip('/')}/{setting.setting.bot_logo.lstrip('/')}"
    await inline_query.answer(
        results=[
            InlineQueryResultArticle(
                title="اینجا بزن !",
                input_message_content=InputTextMessageContent(
                    f"{user.lang.invite_text}\n\n{user_invite_link}"
                ),
                thumb_url=thumb_url,
                description="**سکه رایگان بگیرید**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(
                            "بزن بریم !",
                            url=user_invite_link
                        )]
                    ]
                )
            ),
        ],
        cache_time=1
    )
