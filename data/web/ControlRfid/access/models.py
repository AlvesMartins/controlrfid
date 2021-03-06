# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import datetime
from core.settings_local import TOKEN_IBOARDBOT, DOMOTICZ_LOCALIP, DOMOTICZ_IDX, DOMOTICZ_USUER, DOMOTICZ_PASS
import urllib3


# Create your models here.

class Device(models.Model):
    __tablename__ = 'cp_device'
    
    TAG = 'tag'
    DEVICE_CHOICES = (
        (TAG, 'TAG'),
    )

    user = models.ForeignKey(User)
    kind = models.CharField(max_length=3,
                                      choices=DEVICE_CHOICES,
                                      default=TAG,
                                      blank=False,
                                      )
    code = models.CharField(max_length=64, blank=False)
    
    def __str__(self):
        return 'Device {}:{} - {}'.format(self.user, self.kind, self.code)
        
    @staticmethod   
    def check_exists_device(code_id):
        #If there is no device code creates a new one.
        #With this you have saved the new devices and then assign them to your user.
        
        if not Device.objects.filter(code=code_id):
            caronte = User.objects.filter(username="lucas").first()
            device_create = Device.objects.create(user=caronte, kind='tag', code=code_id)

class Ambiente(models.Model):
    __tablename__ = 'cp_ambiente'

    fechadura = models.IntegerField(primary_key=True)
    ambiente = models.CharField(max_length=150)
    descri = models.CharField(max_length=150)
    class Meta:
        unique_together = ["fechadura"]
    def __unicode__(self):
        return unicode(self.fechadura)


class Acesso(models.Model):
    __tablename__ = 'cp_acessos'

    ambiente = models.ManyToManyField(Ambiente)
    etiqueta = models.CharField(max_length=12)
    acesso = models.DateTimeField(auto_now_add=True)
    def get_ambiente(self):
        return "\n".join([p.ambiente for p in self.ambiente.all()])


class Zona(models.Model):
    __tablename__ = 'cp_zonas'

    fechadura = models.ForeignKey(Ambiente)
    etiqueta = models.CharField(max_length=12)
    acesso = models.DateTimeField(auto_now_add=True)
    class Meta:
        def __str__(self):
            return self.id()

class Evento(models.Model):
    __tablename__ = 'cp_eventos'

    Liberado = 'Acesso liberado'
    Negado = 'Acesso Negado'
    DEVICE_CHOICES = (
        (Liberado, 'Liberado'),
        (Negado , 'Negado')
    )
    evento = models.AutoField(primary_key=True)
    fechadura = models.IntegerField()
    etiqueta = models.CharField(max_length=12)
    ocorrencia = models.DateTimeField(auto_now_add=True)
    comando = models.IntegerField()
    descri = models.CharField(max_length=150,
                                      choices=DEVICE_CHOICES,
                                      default=Negado,
                                      blank=False,
                                      )
    class Meta:
        def __str__(self):
            return self.id()



class Log(models.Model):
    __tablename__ = 'cp_log'

    user = models.ForeignKey(User)
    ts_input = models.DateTimeField()
    ts_output = models.DateTimeField()
    user_in = models.BooleanField(default=False)
    
    def __str__(self):
        return 'Log {}: {} - {}'.format(self.user, self.ts_input, self.ts_output)
    
   
    @staticmethod   
    def checkentryLog(Device):

        def domoticz_armed(armed='On'):
            # Domoticz armed Security
            http = urllib3.PoolManager()
            url = 'http://'+DOMOTICZ_LOCALIP+'/json.htm?type=command&param=switchlight&idx='+DOMOTICZ_IDX+'&switchcmd='
            headers = urllib3.util.make_headers(basic_auth=DOMOTICZ_USUER+':'+DOMOTICZ_PASS)
            r = http.request('GET', url+armed, headers=headers)
 
        date = datetime.datetime.now()

        log_obj = Log.objects.filter(user=Device.user).last()
        
        log_user_in_initial = len(Log.objects.filter(user_in=True).all())

        if not log_obj:

            log_create = Log.objects.create(user=Device.user, ts_input=date, ts_output=date, user_in=True)
            send_log_msg(True, str(Device.user.username))
            
        elif(log_obj.user_in == True):
                    
            log_obj.ts_output = datetime.datetime.now()
            log_obj.user_in = False
            log_obj.save()
            send_log_msg(False, str(Device.user.username))

        else:
            log_create = Log.objects.create(user=Device.user, ts_input=date, ts_output=date, user_in=True)    
            send_log_msg(True, str(Device.user.username))
     
        log_user_in_end = len(Log.objects.filter(user_in=True).all())
        
        
        if(log_user_in_initial == 0 and log_user_in_end == 1):
            send_group_msg(True, str(Device.user.username))
            # Site domoticz state On
            domoticz_armed('On')
            
        elif(log_user_in_initial == 1 and log_user_in_end == 0):
            send_group_msg(False, str(Device.user.username))
            # Site domoticz state Off
            domoticz_armed('Off')
           
            
    @staticmethod   
    def listUsersInside():
        
        users = Log.objects.filter(user_in=True).all()
        
        if users:
            users_in_msg = 'People registered here are: {}'.format(
            ', '.join([str(users[i].user.username) for i in range(len(users))])
             )
        else:
             users_in_msg = 'Nobody inside'
                
        
        return users_in_msg


    @staticmethod    
    def listUsersCount():

        return Log.objects.filter(user_in=True).count()
            
class Payment(models.Model):
    __tablename__ = 'cp_payment'

    year = models.IntegerField()
    month = models.IntegerField()
    user = models.ForeignKey(User)
    f_payment = models.DateTimeField()
    amount = models.FloatField(default=0.0)
    
    def __str__(self):
        return '{}: {} - {}'.format(self.user, self.amount, self.f_payment)
 
        
