from django.contrib import admin
from .models import (
    User, Setting, PlanModel, PayModel, ChannelsModel,
    AdsModel, TextModel, WorkFlowModel, SendMessageModel
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'full_name', 'coin', 'is_admin', 'is_active', 'creation')
    search_fields = ('chat_id', 'full_name')
    list_filter = ('is_admin', 'is_active', 'lang')
    fieldsets = (
        ('اطلاعات کاربر', {
            'fields': ('chat_id', 'full_name', 'coin', 'lang')
        }),
        ('مجوزها', {
            'fields': ('is_admin', 'is_active', 'groups', 'user_permissions')
        }),
        ('اطلاعات اضافی', {
            'fields': ('creation',)
        }),
    )
    readonly_fields = ('creation',)
    ordering = ('-creation',)


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('bot_username', 'api_id', 'ocr_coin', 'summary_coin')
    search_fields = ('bot_username', 'bot_token')
    list_filter = ('ocr_coin', 'summary_coin', 'daili_coin')
    fieldsets = (
        ('تنظیمات ربات', {
            'fields': ('bot_username', 'bot_token', 'api_id', 'api_hash', 'session_string' , 'bot_logo' )
        }),
        ('تنظیمات مالی', {
            'fields': ('ocr_coin', 'summary_coin', 'daili_coin', 'invite_coin', 'zarinpal_key')
        }),
        ('تنظیمات کانال‌ها', {
            'fields': ('backup_channel', 'force_channels')
        }),
        ('تنظیمات متن', {
            'fields': ('default_text',)
        }),
        ('تنظیمات دیتابیس ردیس', {
            'fields': ('redis_host', 'redis_port', 'redis_db')
        }),
    )


@admin.register(PlanModel)
class PlanModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'coin', 'price_ir' ,'price_trx')
    search_fields = ('name',)
    ordering = ('price_ir',)


@admin.register(PayModel)
class PayModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'create_at')
    search_fields = ('user__full_name', 'plan__name')
    ordering = ('-create_at',)
    readonly_fields = ('create_at',)


@admin.register(ChannelsModel)
class ChannelsModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'chat_id')
    search_fields = ('name', 'url')
    ordering = ('name',)


@admin.register(AdsModel)
class AdsModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'text')
    search_fields = ('name', 'text')


@admin.register(TextModel)
class TextModelAdmin(admin.ModelAdmin):
    list_display = ('lang_code', 'lang_name')
    search_fields = ('lang_code', 'lang_name')
    ordering = ('lang_code',)


@admin.register(WorkFlowModel)
class WorkFlowModelAdmin(admin.ModelAdmin):
    list_display = ('type', 'token', 'wallet', 'update')
    search_fields = ('type', 'token')
    ordering = ('-update',)


@admin.register(SendMessageModel)
class SendMessageModelAdmin(admin.ModelAdmin):
    list_display = ('message', 'is_forward')
    search_fields = ('message',)
    list_filter = ('is_forward',)
