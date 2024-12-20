from pyrogram import Client, filters
from utils import cache , btn , txt , logger
from utils import filters as f 
from config import con

@Client.on_message(f.user_is_join & f.user_is_active   , group = 2)
async def handlers(bot, msg):
    
    user = con.user(chat_id = msg.from_user.id  , full_name=msg.from_user.first_name)
    setting = con.setting
        

    btns = {
        f'{user.lang.profile_btn}': profile_handler,
        f'{user.lang.help_btn}': help_handler,
        f'{user.lang.support_btn}': support_handler,
        f'{user.lang.buy_btn}': buy_handler,
        # f'{setting.texts.plans_btn}': plans_handler,
        # f'{setting.texts.add_volume_with_join_btn}' : add_volume_with_join_btn_handler,
        # f'{setting.texts.add_volume_with_ref_btn}' : add_volume_with_ref_btn_handler,
        # f'{setting.texts.add_volume_with_payment_btn}'  : add_volume_with_payment_btn_handler,

        '/start' : start_handler ,
        '/help' : help_handler,
        '/support' : support_handler ,
        '/profile' :profile_handler,
        # '/setting' : setting_handler,
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
        
        elif status == 'back' : 
            await back_btn_manager(bot , call , user , setting )
        
        
        
    
    
    
async def show_coin_plan_handler(bot , call , user , setting) :
    plan_id = call.data.split(':')[1]
    for plan in setting.plans : 
        if int(plan.id) == int(plan_id) : 
            pay_url = con.create_payment(chat_id=call.from_user.id , plan=plan.id)
            await call.message.edit_text(plan.des , reply_markup = btn.buy_coin(user , pay_url.url))
            
            
            
    
async def back_btn_manager(bot ,call , user , setting ) : 
    status = call.data.split(':')[1]
    if status == 'buy' : 
        await call.message.edit_text(user.lang.buy_text , reply_markup = btn.buy_handler_btn(user))
    elif status == 'plans' : 
        await buy_coin_handler(bot , call , user , setting  )
        
        
        
        
        
async def buy_coin_handler(bot , call , user , setting ):
    await call.message.edit_text(user.lang.buy_text , reply_markup = btn.coin_plans_list(setting , user ))
    


async def invite_get_coin_handler(bot , call , user , setting ) : 
    print('fuck user ')