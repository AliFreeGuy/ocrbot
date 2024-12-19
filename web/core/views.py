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
from .models import User , Setting , PayModel
from .serializers import UserSerializer
import logging
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json
import requests
from django.http import JsonResponse
from core.tasks import send_message_for_user
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


logger = logging.getLogger('core')


sandbox = 'www'
ZP_API_REQUEST = settings.ZP_API_REQUEST
ZP_API_VERIFY = settings.ZP_API_VERIFY
ZP_API_STARTPAY = settings.ZP_API_STARTPAY
CALLBACK_URL =settings.CALLBACK_URL




@method_decorator(csrf_exempt, name='dispatch')
class PaymentView(View):
    def get(self, request , chat_id , plan_id):
        user = User.objects.get(chat_id = chat_id)
        setting = Setting.objects.first()
        plan = PlanModel.objects.get(id = plan_id)
        
        description_text = f'{str(chat_id)} - {plan.name}'
        data = {
            "MerchantID": setting.zarinpal_key,
            "Amount": int(plan.price_ir),
            "Description": description_text,
            "Phone": '09123456789',
            "CallbackURL": CALLBACK_URL,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
    
        try:
            response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
            if response.status_code == 200:
                response_data = response.json()
                
                if response_data['Status'] == 100:
                    PayModel.objects.create(
                        user = user ,
                        plan = plan ,
                        key = str(response_data['Authority']),
                        )
                    return JsonResponse({'status': True, 'url':ZP_API_STARTPAY + str(response_data['Authority']), 'authority': response_data['Authority']})
                else:
                    PayModel.objects.create(
                        user = user ,
                        plan = plan ,
                        key = str(response_data['Authority']),
                        )
                    return JsonResponse({'status': False, 'code': str(response_data['Status'])})
                
            return JsonResponse({'status': False, 'code': 'unexpected error'})
        except requests.exceptions.Timeout:
            return JsonResponse({'status': False, 'code': 'timeout'})
        except requests.exceptions.ConnectionError:
            return JsonResponse({'status': False, 'code': 'connection error'})
            








def verify(request):
    authority = request.GET.get('Authority')
    if not authority:
        return render(request, 'unsuccess.html', {'error': 'Authority is missing.'})

    payment_data = PayModel.objects.filter(key=authority).first()
    if not payment_data:
        return render(request, 'unsuccess.html', {'error': 'Invalid authority key.'})

    setting = Setting.objects.first()
    if not setting or not setting.zarinpal_key:
        return render(request, 'unsuccess.html', {'error': 'Payment gateway is not configured properly.'})

    data = {
        "MerchantID": setting.zarinpal_key,
        "Amount": int(payment_data.plan.price_ir),
        "Authority": authority,
    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    
    try:
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        response.raise_for_status()  # بررسی خطاهای احتمالی HTTP
        response_data = response.json()
    except requests.RequestException as e:
        return render(request, 'unsuccess.html', {'error': f'Error connecting to payment gateway: {str(e)}'})

    if response_data.get('Status') == 100:
        payment_data.status = True
        payment_data.save()

        user = payment_data.user
        user.plan = payment_data.plan
        user.save()

        send_message_for_user.delay_on_commit(
            chat_id=user.chat_id,
            text=payment_data.user.lang.plan_activation_success_message
        )
        return render(request, 'success.html', {'user': payment_data.user})
    else:
        return render(request, 'unsuccess.html', {'user': payment_data.user, 'error': 'Payment verification failed.'})


































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
            if field == 'lang' : 
                user_lang = TextModel.objects.filter(lang_code = request.data.get(field,None) )
                if user_lang :  user.lang = user_lang.first()
                    
            elif field in request.data:
                setattr(user, field, request.data[field])

        user.save()

        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(UserSerializer(user).data, status=status_code)


