from rest_framework import serializers
from .models import Setting, PlanModel, PayModel, ChannelsModel, AdsModel, TextModel, WorkFlowModel, SendMessageModel ,User

class ChannelsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelsModel
        fields = '__all__'

class TextModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextModel
        fields = '__all__'

class PlanModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanModel
        fields = '__all__'

class PayModelSerializer(serializers.ModelSerializer):
    plan = PlanModelSerializer()

    class Meta:
        model = PayModel
        fields = '__all__'

class AdsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdsModel
        fields = '__all__'

class WorkFlowModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkFlowModel
        fields = '__all__'

class SendMessageModelSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = SendMessageModel
        fields = '__all__'

class SettingSerializer(serializers.ModelSerializer):
    default_text = TextModelSerializer()
    backup_channel = ChannelsModelSerializer()
    force_channels = ChannelsModelSerializer(many=True)
    
    class Meta:
        model = Setting
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    lang = TextModelSerializer(read_only=True)  # استفاده از سریالایزر زبان

    class Meta:
        model = User
        fields = [
            'chat_id', 
            'full_name', 
            'coin', 
            'lang',  # نمایش اطلاعات کامل زبان
            'is_admin', 
            'is_active', 
            'creation', 
            'last_coin_update'
        ]