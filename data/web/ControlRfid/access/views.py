from django.shortcuts import render
from rest_framework import generics
from .models import Device, Log, Evento, Payment, Zona
from .serializers import DeviceResultSerializer, LogSerializer, ZonaSerializer, EventoSerializer
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from graphos.renderers import flot, gchart
from graphos.sources.simple import SimpleDataSource
from django.contrib import messages
from django import forms
from form import PostForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django_tables2 import RequestConfig
from .table import EventoTable, ZonaTable
from django.utils import timezone
from django.shortcuts import redirect




# Create your views here.

class DeviceIDList(generics.ListAPIView):

    serializer_class = DeviceResultSerializer

    def get_queryset(self, **kwargs):

        code_id = self.kwargs['code']
        
        Device.check_exists_device(code_id)
        
        return Device.objects.filter(code=code_id)

class ZonaIDList(generics.ListAPIView):
    queryset = Zona.objects.all()
    serializer_class = ZonaSerializer
    def put(self, request, *args, **kwargs):
            return self.update(request, *args, **kwargs)

class EventoIDList(generics.ListAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    def put(self, request, *args, **kwargs):
            return self.update(request, *args, **kwargs)


        
class LogIDList(generics.ListAPIView):

    serializer_class = LogSerializer

    def get_queryset(self, **kwargs):

        code_id = self.kwargs['ts_input']
        
        Log.check_exists_device(code_id)
        
        return Log.objects.filter()
        
@login_required(login_url='/')
def homepage(request):
    users_count = User.objects.count()
    users_in_count = Log.listUsersCount()
    return render(request, 'access/index.html', {'users_count': users_count, 'users_in_count': users_in_count})


@login_required(login_url='/')
def personal_info(request):
    return render(request, 'access/info.html')

@login_required(login_url='/')
def eventos_info(request):
    evento = EventoTable(Evento.objects.all())
    zona = ZonaTable(Zona.objects.all())
    RequestConfig(request, paginate={'per_page': 10}).configure(zona)
    RequestConfig(request, paginate={'per_page': 10}).configure(evento)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            messages.success(request, 'submission successful')
            return redirect('/accounts/profile/eventosADM')
    else:
        form = PostForm()
    return render(request, 'access/eventos.html', {'evento': evento, 'zona': zona, 'form': form})

@login_required(login_url='/')
def event_info(request):
    evento = EventoTable(Evento.objects.all())
    RequestConfig(request, paginate={'per_page': 10}).configure(evento)
    return render(request, 'access/event.html', {'evento': evento})

@login_required(login_url='/')
def device_info(request):
    device_list_user = Device.objects.filter(user=User).all()
    return render(request, 'access/devicelist.html', {'device_list_user': device_list_user})
    

@login_required(login_url='/')
def global_charts(request):
    
    qs = Log.objects.all()
    week = [qs.filter(ts_input__week_day=i).count() for i in range(7)]
    
    data =  [
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        week
    ]
    

    #data_source = ModelDataSource(queryset, fields=['year', 'sales'])

    chart = gchart.ColumnChart(SimpleDataSource(data=data), html_id="line_chart")
    
    return render(request, 'access/global_charts.html', {'chart': chart } )
    
            
    
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })
    
    
    
    
    