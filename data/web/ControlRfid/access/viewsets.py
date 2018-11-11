from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Device, Log, Door
from .serializers import UserSerializer, DeviceSerializer, LogSerializer, DoorSerializer
 
class UserViewSet(viewsets.ModelViewSet):
 
    serializer_class = UserSerializer
    queryset = User.objects.all()

class DoorViewSet(viewsets.ModelViewSet):
    queryset = Door.objects.all()
    serializer_class = DoorSerializer


class LogSerializer(viewsets.ModelViewSet):
 
    serializer_class = LogSerializer
    queryset = Log.objects.all()

class DeviceViewSet(viewsets.ModelViewSet):
 
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()

