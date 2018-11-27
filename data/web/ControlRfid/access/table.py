import django_tables2 as tables
from .models import Evento, Zona, Ambiente
from django_filters.views import FilterView


class EventoTable(tables.Table):
    class Meta:
        model = Evento
        exclude = ('comando', 'evento',)
        template_name = 'django_tables2/bootstrap.html'
    
class ZonaTable(tables.Table):
    class Meta:
        model = Zona
        exclude = ('id',)
        template_name = 'django_tables2/bootstrap.html'

class AmbienteTable(tables.Table):
    class Meta:
        model = Ambiente
        template_name = 'django_tables2/bootstrap.html'