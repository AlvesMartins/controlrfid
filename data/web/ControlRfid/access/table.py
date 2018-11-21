import django_tables2 as tables
from .models import Evento, Zona

class EventoTable(tables.Table):
    class Meta:
        model = Evento
        template_name = 'django_tables2/bootstrap.html'
    
class ZonaTable(tables.Table):
    class Meta:
        model = Zona
        template_name = 'django_tables2/bootstrap.html'