from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Setting, PlanModel, PayModel, ChannelsModel, AdsModel, TextModel, WorkFlowModel, SendMessageModel,User
from .serializers import (
    SettingSerializer, PlanModelSerializer, PayModelSerializer, 
    ChannelsModelSerializer, AdsModelSerializer, TextModelSerializer, 
    WorkFlowModelSerializer, SendMessageModelSerializer,UserSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer



class SettingAPIView(APIView):
    def get(self, request):
        # گرفتن اولین تنظیم از مدل Setting
        setting = Setting.objects.first()
        setting_data = SettingSerializer(setting).data if setting else None

        plans = PlanModel.objects.all()
        channels = ChannelsModel.objects.all()
        ads = AdsModel.objects.all()
        texts = TextModel.objects.all()
        workflows = WorkFlowModel.objects.all()

        plans_data = PlanModelSerializer(plans, many=True).data
        channels_data = ChannelsModelSerializer(channels, many=True).data
        ads_data = AdsModelSerializer(ads, many=True).data
        texts_data = TextModelSerializer(texts, many=True).data
        workflows_data = WorkFlowModelSerializer(workflows, many=True).data

        response_data = {
            "setting": setting_data,
            "plans": plans_data,
            "channels": channels_data,
            "ads": ads_data,
            "texts": texts_data,
            "workflows": workflows_data,
        }

        return Response(response_data)
















class UserAPIView(APIView):

    def post(self, request, *args, **kwargs):
        chat_id = request.data.get("chat_id")
        if not chat_id:
            return Response({"error": "chat_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(chat_id=chat_id)

        updatable_fields = ['full_name', 'lang', 'is_admin', 'is_active', 'coin', 'last_coin_update']

        for field in updatable_fields:
            if field in request.data:
                setattr(user, field, request.data[field])

        user.save()

        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(UserSerializer(user).data, status=status_code)


