from django.urls import path 
from . import views


app_name = 'core'


urlpatterns = [
    path('setting/' , views.SettingAPIView.as_view() , name='setting') , 
    path('user/' , views.UserAPIView.as_view() , name='update_user') ,
    
     
    path('payment/<int:chat_id>/<int:plan_id>/' , views.PaymentView.as_view() , name = 'payment'),
    path('verify/', views.verify , name='verify'),
     
]
