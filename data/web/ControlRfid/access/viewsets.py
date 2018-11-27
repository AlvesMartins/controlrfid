from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Device, Log, Zona, Evento, Ambiente, Acesso
from .serializers import UserSerializer, DeviceSerializer, LogSerializer, ZonaSerializer, EventoSerializer, AmbienteSerializer, Acesso
 
class UserViewSet(viewsets.ModelViewSet):
 
    serializer_class = UserSerializer
    queryset = User.objects.all()

class AmbienteViewSet(viewsets.ModelViewSet):
    serializer_class = AmbienteSerializer
    queryset = Ambiente.objects.all()

class ZonaViewSet(viewsets.ModelViewSet):
    queryset = Zona.objects.all()
    serializer_class = ZonaSerializer

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

class AcessoViewSet(viewsets.ModelViewSet):
    queryset = Acesso.objects.all()
    serializer_class = AmbienteSerializer


class LogSerializer(viewsets.ModelViewSet):
 
    serializer_class = LogSerializer
    queryset = Log.objects.all()

class DeviceViewSet(viewsets.ModelViewSet):
 
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()

