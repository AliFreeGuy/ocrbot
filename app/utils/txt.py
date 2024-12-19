from datetime import datetime
import jdatetime




def user_usage(user,setting):
    if user.plan:
        max_file_size_mb = user.plan.max_file_size  
        daily_volume_mb = user.plan.daili_volume  
        traffic_usage_mb = user.daili_volume

        max_file_size_gb = max_file_size_mb / 1024  
        daily_volume_gb = daily_volume_mb / 1024 
        traffic_usage_gb = traffic_usage_mb / 1024 
        remaining_daily_volume_gb = traffic_usage_gb

        formatted_max_file_size = f"{max_file_size_gb:.2f} GB"
        formatted_daily_volume = f"{daily_volume_gb:.2f} GB"
        formatted_remaining_daily_volume = f"{remaining_daily_volume_gb:.2f} GB"

        volume_text = user.lang.plan_daili_volume
        file_size_text = user.lang.max_file_size_text
        remaining_size_text = user.lang.remaining_daili_size
    else:
        formatted_max_file_size = "0.00 GB"
        formatted_daily_volume = "0.00 GB"
        formatted_remaining_daily_volume = "0.00 GB"

        volume_text = user.lang.plan_daili_volume
        file_size_text = user.lang.max_file_size_text
        remaining_size_text = user.lang.remaining_daili_size

    output = (
        f"{volume_text}: {formatted_daily_volume}\n"  # حجم روزانه پلن
        f"{file_size_text}: {formatted_max_file_size}\n"  # حجم فایل‌های مجاز
        f"{remaining_size_text}: {formatted_remaining_daily_volume}\n"  # حجم باقی‌مانده روزانه
        "-------\n"
        f"{user.lang.usage_sub_text}"
    )

    return output










def file_info(user ,data ):
    text = f'''
{user.lang.dl_file_name_text} : `{data['file_name'].replace('"' , '')}`

{user.lang.dl_file_size_text} : `{data['file_size_str']}`

{user.lang.dl_file_status_text} : `{data['status']}`
'''
    
    return text



def up_photo_text(user , file_data) : 
    text = f'''
{user.lang.up_file_type_text} : `{user.lang.up_file_type_photo_text}`
{user.lang.up_file_size_text} : `{str(file_data['file_size_str'])}`
{user.lang.up_file_quality_text} : `{file_data['quality']}`

{user.lang.up_file_status_text} : `{file_data['status']}`

'''
    return text






def up_voice_text(user , file_data) : 
    text = f'''
{user.lang.up_file_type_text} : `{user.lang.up_file_type_voice_text}`
{user.lang.up_file_size_text} : `{str(file_data['file_size_str'])}`
{user.lang.up_file_duration_text} : `{file_data['duration']}`

{user.lang.up_file_name_text} : `{file_data['file_name']}`

'''

    return text


def up_document_txt(user , data) :
    text = f'''
{user.lang.up_file_type_text} : `{user.lang.up_file_type_doc_text}`
{user.lang.up_file_size_text} : `{str(data['file_size_str'])}`
{user.lang.up_file_is_thumb} : `{'✅' if data.get('thumb' , None ) not in [None , 'none'] else '❌'} `

{user.lang.up_file_name_text} : `{data['file_name']}`

'''
    return text



def up_audio_txt(user , data) :
    
    text = f'''
{user.lang.up_file_type_text} : `{user.lang.up_file_type_audio_text}`
{user.lang.up_file_size_text} : `{str(data['file_size_str'])}`
{user.lang.up_music_name_text} : `{data['up_music_name_text']} `
{user.lang.up_singer_name_text} : `{data['up_singer_name_text']} `
{user.lang.up_file_is_thumb} : `{'✅' if data.get('thumb' , None ) not in ['none' , None ] else '❌'} `
{user.lang.up_file_duration_text} : `{data['duration']}`

{user.lang.up_file_name_text} : `{data['file_name']}`

'''
    return text





def up_video_text(user , data) :
    
    text = f'''
{user.lang.up_file_type_text} : `{user.lang.up_file_type_video_text}`
{user.lang.up_file_size_text} : `{str(data['file_size_str'])}`
{user.lang.up_file_is_thumb} : `{'✅' if data.get('thumb' , None ) not in ['none' , None ] else '❌'} `
{user.lang.up_file_duration_text} : `{data['duration']}`
{user.lang.up_file_quality_text} : `{data['quality']}`

{user.lang.up_file_name_text} : `{data['file_name']}`

'''
    return text








# تابع تبدیل تاریخ میلادی به شمسی
def convert_to_shamsi(date_str):
    print(date_str)
    if date_str:
        # ابتدا رشته تاریخ را به شیء datetime تبدیل می‌کنیم
        try:
            date_obj = datetime.fromisoformat(date_str)
        except ValueError:
            return '-'  # در صورت خطا در تبدیل تاریخ به تاریخ میلادی، مقدار پیشفرض را برمی‌گردانیم
        # سپس تاریخ میلادی را به شمسی تبدیل می‌کنیم
        shamsi_date = jdatetime.datetime.fromgregorian(datetime=date_obj)
        return shamsi_date.strftime('%Y/%m/%d %H:%M:%S')
    return '-'







import jdatetime
from datetime import datetime

def generate_channel_report(channel):
    # استخراج داده‌ها
    chat_id = channel.channel.chat_id
    channel_name = channel.channel.name
    channel_link = channel.channel.link
    status = "فعال" if channel.is_active else "غیرفعال"
    member_count = channel.member_count
    member_joined = channel.member_joined
    before_member = channel.before_channel_member
    after_member = channel.after_channel_member
    hash_link_info = channel.invite_link

    # تبدیل تاریخ میلادی به شمسی با استفاده از jdatetime
    if isinstance(channel.creation_at, str):
        # اگر creation_at رشته است، آن را به datetime تبدیل می‌کنیم
        creation_date = datetime.strptime(channel.creation_at, '%Y-%m-%d %H:%M:%S')
    else:
        creation_date = channel.creation_at

    if isinstance(channel.update_at, str):
        # اگر update_at رشته است، آن را به datetime تبدیل می‌کنیم
        update_date = datetime.strptime(channel.update_at, '%Y-%m-%d %H:%M:%S')
    else:
        update_date = channel.update_at

    # تبدیل تاریخ‌ها به تاریخ شمسی و زمان
    creation_date_shamsi = jdatetime.datetime.fromgregorian(datetime=creation_date).strftime('%Y/%m/%d %H:%M:%S')
    update_date_shamsi = jdatetime.datetime.fromgregorian(datetime=update_date).strftime('%Y/%m/%d %H:%M:%S')

    # محاسبه تعداد ممبرهای باقی‌مانده
    remaining_members = int(member_count) - int(member_joined)

    # ترکیب متن با تاریخ شمسی و ساعت و استفاده از اموجی‌ها
    message = f"""
🆔 چت ایدی کانال : `{chat_id}`
📱 نام کانال : `{channel_name}`
🔗 لینک کانال : `{channel_link}`
📅 تاریخ شروع : `{creation_date_shamsi}`
🔄 آخرین بروزرسانی : `{update_date_shamsi}`
🟢 وضعیت : `{status}`

👥 میزان ممبر درخواستی : `{member_count}`
👥 میزان ممبر جوین شده : `{member_joined}`
🔴 ممبر های باقی مانده : `{remaining_members}`

👤 ممبر ها قبل جوین : `{before_member}`
👤 ممبر ها بعد جوین : `{after_member}`

🔑 لینک اطلاعات : {hash_link_info}
"""
    return message
