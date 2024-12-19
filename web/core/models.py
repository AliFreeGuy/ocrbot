from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.utils import timezone
from datetime import timedelta
from datetime import datetime, timedelta
from django.utils.timezone import now


class User(AbstractBaseUser, PermissionsMixin):
    chat_id = models.BigIntegerField(unique=True, verbose_name="شناسه چت")
    full_name = models.CharField(max_length=128, null=True, blank=True, verbose_name="نام کامل")
    coin = models.PositiveBigIntegerField(default=0, verbose_name="اعتبار")
    lang = models.ForeignKey('core.TextModel', on_delete=models.CASCADE, related_name='users', null=True, blank=True, verbose_name="زبان")
    is_admin = models.BooleanField(default=False, verbose_name="آیا ادمین است؟")
    is_active = models.BooleanField(default=True, verbose_name="آیا فعال است؟")
    creation = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    last_coin_update = models.DateField(null=True, blank=True, verbose_name="آخرین به‌روزرسانی سکه‌ها") 

    USERNAME_FIELD = 'chat_id'
    REQUIRED_FIELDS = ['full_name', ]

    objects = UserManager()

    def __str__(self) -> str:
        return str(self.full_name)

    @property
    def is_staff(self):
        return self.is_admin

    def save(self, *args, **kwargs):
        from core.models import Setting  

        
        if not self.lang: 
            setting = Setting.objects.first()
            if setting and setting.default_text:
                self.lang = setting.default_text  

        setting = Setting.objects.first()
        daili_coin = setting.daili_coin if setting else 0

        is_new = self.pk is None  
        if is_new:
            self.coin += daili_coin 

        today = now().date()
        if not is_new and (self.last_coin_update != today):
            if now().hour >= 0:  
                self.coin += daili_coin
                self.last_coin_update = today

        super().save(*args, **kwargs) 


    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"



class Setting(models.Model):

    bot_username = models.CharField(max_length=128, verbose_name="نام کاربری ربات")
    bot_token = models.CharField(max_length=128, verbose_name="توکن ربات")
    api_id = models.CharField(max_length=128, verbose_name="شناسه API")
    api_hash = models.CharField(max_length=128, verbose_name="هش API")
    session_string = models.TextField(null=True, blank=True, verbose_name="رشته نشست")
    ocr_coin = models.PositiveBigIntegerField(default=1, verbose_name="اعتبار OCR")
    summary_coin = models.PositiveBigIntegerField(default=20, verbose_name="اعتبار خلاصه سازی")
    translate_coin = models.PositiveBigIntegerField(default=1 , verbose_name='اعتبار ترجمه')
    daili_coin = models.PositiveBigIntegerField(default=10, verbose_name="اعتبار روزانه")
    invite_coin = models.PositiveBigIntegerField(default=10, verbose_name="اعتبار دعوت")
    default_text = models.ForeignKey('TextModel', related_name='setting', on_delete=models.CASCADE, null=True, blank=True, verbose_name="متن پیش‌فرض")
    zarinpal_key = models.CharField(max_length=128, default='test', verbose_name="کلید زرین پال")
    redis_host = models.CharField(max_length=128, default='localhost', verbose_name="میزبان Redis")
    redis_port = models.PositiveIntegerField(default=6379, verbose_name="پورت Redis")
    redis_db = models.PositiveIntegerField(default=0, verbose_name="دیتابیس Redis")
    backup_channel = models.ForeignKey('core.ChannelsModel', on_delete=models.CASCADE, related_name='backup_settings', null=True, blank=True, verbose_name="کانال پشتیبان")
    force_channels = models.ManyToManyField('core.ChannelsModel', related_name='forced_settings', blank=True, verbose_name="کانال‌های اجباری")
    tron_wallet =models.CharField(max_length=128 , default='none' , verbose_name='آدرس کیف پول ترون')


    
    class Meta:
        verbose_name = "تنظیمات"
        verbose_name_plural = "تنظیمات"


class PlanModel(models.Model): 
    name = models.CharField(max_length=128, verbose_name="نام پلن")
    des = models.TextField(verbose_name="توضیحات")
    coin = models.PositiveBigIntegerField(verbose_name="اعتبار")
    price_ir = models.PositiveBigIntegerField(default=1000 , verbose_name="قیمت ریالی")
    price_trx = models.PositiveBigIntegerField(default=10 , verbose_name='قیمت ترونی')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "پلن"
        verbose_name_plural = "پلن‌ها"


class PayModel(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='pyaments', verbose_name="کاربر")
    plan = models.ForeignKey(PlanModel, on_delete=models.CASCADE, related_name='payments', verbose_name="پلن")
    key = models.CharField(max_length=128 , default='none')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ پرداخت")
    status =models.BooleanField(default=True , verbose_name='آیا پرداخت کرده ؟') 
    
    
    def __str__(self) -> str:
        return f'{str(self.user)} - {str(self.plan)}'

    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"


class ChannelsModel(models.Model): 
    name = models.CharField(max_length=128, verbose_name="نام کانال")
    url = models.URLField(verbose_name="آدرس URL")
    chat_id = models.BigIntegerField(verbose_name="شناسه چت")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "کانال"
        verbose_name_plural = "کانال‌ها"


class AdsModel(models.Model): 
    name = models.CharField(max_length=128, verbose_name="نام تبلیغ")
    text = models.TextField(verbose_name="متن تبلیغ" , default='none')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "تبلیغ"
        verbose_name_plural = "تبلیغات"


class TextModel(models.Model): 
    lang_code = models.SlugField(verbose_name="کد زبان")
    lang_name = models.CharField(max_length=128, verbose_name="نام زبان")
    start_text = models.TextField(default='none', verbose_name="متن شروع")
    help_text = models.TextField(default='none', verbose_name="متن راهنما")
    support_text = models.TextField(default='none', verbose_name="متن پشتیبانی")
    user_not_active_text = models.TextField(default='none', verbose_name="متن غیر فعال بودن کاربر")
    user_not_join_text = models.TextField(default='none', verbose_name="متن عدم عضویت کاربر")
    user_not_coin_text = models.TextField(default='none', verbose_name="متن عدم اعتبار")
    invite_text = models.TextField(default='none', verbose_name="متن دعوت")
    buy_text = models.TextField(default='none', verbose_name="متن خرید")

    profile_btn = models.CharField(max_length=128, verbose_name="دکمه پروفایل")
    setting_btn = models.CharField(max_length=128, verbose_name="دکمه تنظیمات")
    help_btn = models.CharField(max_length=128, verbose_name="دکمه راهنما")
    support_btn = models.CharField(max_length=128, verbose_name="دکمه پشتیبانی" , default='none')
    buy_btn = models.CharField(max_length=128, verbose_name="دکمه خرید")
    ocr_btn = models.CharField(max_length=128, verbose_name="دکمه OCR")
    summary_btn = models.CharField(max_length=128, verbose_name="دکمه خلاصه‌سازی")
    translate_btn = models.CharField(max_length=128 , verbose_name='دکمه خلاصه سازی')
    placeholder_text = models.CharField(max_length=128 , default='send message' , verbose_name='متن کمرنگ ارسال پیام کاربر')
    plan_activation_success_messagemodels = models.TextField(default='nonte', verbose_name='پیام زمان خرید سکه کاربر', help_text=f'$user : نام کاربر $plan : نام پلن')
    pay_with_rial_btn = models.CharField(max_length = 128 , default='none' , verbose_name='دکمه پرداخت با ریال')
    pay_with_tron_btn = models.CharField(max_length=128 , default='noen' , verbose_name='دکمه پرداخت با ترون')
    pay_with_tron_text = models.TextField(default='none' , verbose_name=f'$plan_name : اسم پلن $plan_price : قیمت پلن $wallet : ادرس ولت ' )
    pay_with_rial_text = models.TextField(default='none' , verbose_name=f'$plan_name : اسم پلن $plan_price : قیمت پلن $url : ادرس درگاه ' )
    payment_failed_head =models.TextField(default='none' , verbose_name=f'تایتل پیام صحفه پرداخت ناموفق')
    payment_failed_body =models.TextField(default='none' , verbose_name=f'پیام پیام صحفه پرداخت ناموفق')
    payment_success_head =models.TextField(default='none' , verbose_name=f'تایتل پیام صحفه پرداخت موفق')
    payment_success_body =models.TextField(default='none' , verbose_name=f'پیام پیام صحفه پرداخت موفق')
    plan_activation_success_message =models.TextField(default='nonte' , verbose_name='پیام پرداخت موفق و فعال شدن پلن' , help_text=f'&user : اسم کاربر $plan_name نام پلن')
    # فیلدهای مربوط به پیام‌های سکه
    inc_coin_text = models.TextField(default='nonte', verbose_name='پیام زمان کم شدن سکه از حساب', help_text='$user برای اسم کاربر، $new_coin برای سکه جدید، $old_coin برای سکه قبلی')
    dec_coin_text = models.TextField(default='nonte', verbose_name='پیام زمان زیاد شدن سکه از حساب', help_text='$user برای اسم کاربر، $new_coin برای سکه جدید، $old_coin برای سکه قبلی')


    joined_btn = models.CharField(max_length=128 , default='none' , verbose_name='دکمه عضو شدم ')
    
    
    def __str__(self):
        return f'{self.lang_code} - {self.lang_name}'

    class Meta:
        verbose_name = "متن"
        verbose_name_plural = "متن‌ها"


class WorkFlowModel(models.Model):
    class WorkflowType(models.TextChoices):
        IMAGE_TO_TEXT = 'Image to Text', 'عکس به متن'
        SUMMARIZATION = 'Summarization', 'خلاصه سازی'
        TRANSLATION = 'Translation', 'ترجمه'

    type = models.CharField(max_length=50, choices=WorkflowType.choices, default=WorkflowType.IMAGE_TO_TEXT, verbose_name="نوع")
    token = models.CharField(max_length=128, verbose_name="توکن")
    workflow_id = models.CharField(max_length=128, verbose_name="شناسه ورک‌فلو")
    wallet = models.PositiveBigIntegerField(default=0, verbose_name="کیف پول")
    update = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    is_active = models.BooleanField(default=True)
    
    
    class Meta:
        verbose_name = "ورک‌فلو"
        verbose_name_plural = "ورک‌فلوها"


class SendMessageModel(models.Model):
    message = models.TextField(verbose_name="پیام")
    users = models.ManyToManyField('User', blank=True, verbose_name="کاربران")
    is_forward = models.BooleanField(default=False, verbose_name="آیا فوروارد است؟")

    def __str__(self) -> str:
        return str(self.message[:20])

    class Meta:
        verbose_name = "ارسال پیام"
        verbose_name_plural = "ارسال پیام‌ها"
