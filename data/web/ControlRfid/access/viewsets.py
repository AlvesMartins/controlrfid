from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Device, Log, Zona, Evento
from .serializers import UserSerializer, DeviceSerializer, LogSerializer, ZonaSerializer, EventoSerializer
 
class UserViewSet(viewsets.ModelViewSet):
 
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ZonaViewSet(viewsets.ModelViewSet):
    queryset = Zona.objects.all()
    serializer_class = ZonaSerializer

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer


class LogSerializer(viewsets.ModelViewSet):
 
    serializer_class = LogSerializer
    queryset = Log.objects.all()

class DeviceViewSet(viewsets.ModelViewSet):
 
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()

