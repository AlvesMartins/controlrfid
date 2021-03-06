from rest_framework import serializers
from core.settings_local import VALUE_PAYMENT_TRUE, MAX_GRANTED_DAYS
from .models import Device, Payment, Log, Zona, Evento, Ambiente, Acesso
import datetime
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
            model = User
            fields = ('id', 'username', 'email', 'first_name', 'last_name')

class AmbienteSerializer(serializers.ModelSerializer):
    class Meta:
            model = Ambiente
            fields = ('fechadura', 'ambiente', 'descri')

class AcessoSerializer(serializers.ModelSerializer):
    class Meta:
            model = Acesso
            fields = ('ambiente', 'etiqueta', 'acesso')

class ZonaSerializer(serializers.ModelSerializer):
    class Meta:
            model = Zona
            fields = ('fechadura', 'etiqueta', 'acesso')


class EventoSerializer(serializers.ModelSerializer):
    class Meta:
            model = Evento
            fields = ('evento', 'fechadura', 'etiqueta', 'ocorrencia', 'comando', 'descri')

    

class LogSerializer(serializers.ModelSerializer):
    class Meta:
            model = Log
            fields = ('id', 'user', 'ts_input', 'ts_output', 'user_in')
            
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
            model = Device
            fields = ('user', 'kind', 'code')
            
class DeviceResultSerializer(serializers.ModelSerializer):
    
    result = serializers.SerializerMethodField('is_auth_user')
    
    def is_auth_user(self, Device):
        
        #Check if the user has monthly payments
        month_actual = datetime.datetime.now().month
        
        if Payment.objects.filter(user=Device.user, month=month_actual): 
            if  Payment.objects.filter(user=Device.user, month=month_actual)[0].amount >= VALUE_PAYMENT_TRUE:
                
                Log.checkentryLog(Device)
                Message.message_detect_tag(Device)
                return True;
        
        
        #Grace period for the first day of the month
        if not Device.kind == "tag":
            #The tags that have no assigned user are exempt from the days of courtesy.
            day_actual = datetime.datetime.now().day
            
            if datetime.datetime.now().day <= MAX_GRANTED_DAYS:
                
                Log.checkentryLog(Device)
                Message.message_detect_tag(Device)
                
                return True;
                
    class Meta:
            model = Device
            fields = ('id', 'user', 'kind', 'code', 'result')
            
    