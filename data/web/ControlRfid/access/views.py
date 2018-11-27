from django.shortcuts import render
from rest_framework import generics
from .models import Device, Log, Evento, Payment, Zona, Ambiente, Acesso
from .serializers import DeviceResultSerializer, LogSerializer, ZonaSerializer, EventoSerializer, AmbienteSerializer, AcessoSerializer
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from graphos.renderers import flot, gchart
from graphos.sources.simple import SimpleDataSource
from django.contrib import messages
from django import forms
from form import PostZonaForm, PostAmbienteForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django_tables2 import RequestConfig
from .table import EventoTable, ZonaTable, AmbienteTable
from django.utils import timezone
from django.shortcuts import redirect

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

class AcessoIDList(generics.ListAPIView):
    queryset = Acesso.objects.all()
    serializer_class = AcessoSerializer
    def put(self, request, *args, **kwargs):
            return self.update(request, *args, **kwargs)

class EventoIDList(generics.ListAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    def put(self, request, *args, **kwargs):
            return self.update(request, *args, **kwargs)

class AmbienteIDList(generics.ListAPIView):
    queryset = Ambiente.objects.all()
    serializer_class = AmbienteSerializer
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
    evento = EventoTable(Evento.objects.all())
    RequestConfig(request, paginate={'per_page': 10}).configure(evento)
    queryset = Evento.objects.all()
    evento_chart = [int(obj.evento) for obj in queryset]
    descri_chart = [obj.descri for obj in queryset]

    users_count = User.objects.count()
    evento_count_n = Evento.objects.filter(descri='Acesso Negado').count()
    evento_count_s = Evento.objects.filter(descri='Acesso liberado').count()
    evento_count = Evento.objects.count()
    
    users_in_count = Log.listUsersCount()
    return render(request, 'access/index.html', {'users_count': users_count, 'users_in_count': users_in_count, 
        'evento_count': evento_count, 'evento_count_n': evento_count_n, 
        'evento_count_s': evento_count_s, 'evento': evento, 'chart_evento': evento_chart, 'chart_descri': descri_chart})


@login_required(login_url='/')
def personal_info(request):
    return render(request, 'access/info.html')

@login_required(login_url='/')
def eventos_info(request):
    evento = EventoTable(Evento.objects.filter(descri='Acesso Negado'))
    zona = ZonaTable(Zona.objects.all())
    ambiente = AmbienteTable(Ambiente.objects.all())
    RequestConfig(request, paginate={'per_page': 5}).configure(zona)
    RequestConfig(request, paginate={'per_page': 10}).configure(evento)
    RequestConfig(request, paginate={'per_page': 5}).configure(ambiente)
    if request.method == "POST":
        form_zona = PostZonaForm(request.POST)
        form_ambiente = PostAmbienteForm(request.POST)

        if form_zona.is_valid():
            post = form_zona.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            messages.success(request, 'submission successful')
            return redirect('/accounts/profile/eventosADM')

        elif form_ambiente.is_valid():
            post = form_ambiente.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            messages.success(request, 'submission successful')
            return redirect('/accounts/profile/eventosADM')
    else:
         form_zona = PostZonaForm()
         form_ambiente = PostAmbienteForm()

    return render(request, 'access/eventos.html', {'evento': evento, 'zona': zona,
     'form_zona': form_zona, 'form_ambiente': form_ambiente, 'ambiente': ambiente})

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
    
    
    
    
    