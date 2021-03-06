# -*- coding: utf-8 -*-
from django.contrib import admin

from access.models import Payment, Device, Log, Zona, Evento, Ambiente, Acesso

from django.utils.safestring import mark_safe
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin


class ZonaAdmin(admin.ModelAdmin): 
  list_display = ('fechadura', 'etiqueta', 'acesso')
  search_fields = ('fechadura', 'etiqueta', 'acesso')
  list_filter = ('fechadura',) 

class AcessoAdmin(admin.ModelAdmin): 
  list_display = ('get_ambiente', 'etiqueta', 'acesso')
  search_fields = ('ambiente', 'etiqueta', 'acesso')
  list_filter = ('ambiente',) 

class AmbienteAdmin(admin.ModelAdmin): 
  list_display = ('fechadura', 'ambiente', 'descri')
  search_fields = ('fechadura', 'ambiente', 'descri')
  list_filter = ('fechadura', 'ambiente',) 
  pass

class EventoAdmin(admin.ModelAdmin): 
  list_display = ('evento', 'fechadura', 'etiqueta', 'ocorrencia', 'comando', 'descri')
  search_fields = ('evento', 'fechadura', 'etiqueta', 'ocorrencia', 'comando', 'descri')
  list_filter = ('evento',) 

class DeviceAdmin(admin.ModelAdmin): 
  list_display = ('kind', 'user', 'code') 
  search_fields = ('user', 'code')
  list_filter = ('kind',) 
  
class LogAdmin(admin.ModelAdmin): 
  list_display = ('user', 'ts_input', 'ts_output', 'day', 'user_in') 
  search_fields = ('user', 'ts_input', 'ts_output')
  list_filter = ('ts_input', 'user_in')
  
  def day(self, obj):
    return obj.ts_input.strftime('%A')

class PaymentAdmin(admin.ModelAdmin): 
  list_display = ('user', 'month', 'year', 'f_payment', 'amount') 
  search_fields = ('user', 'month', 'year') 
  list_filter = ('month',)

  
def roles(self):
    #short_name = unicode # function to get group name
    short_name = lambda x:unicode(x)[:1].upper() # first letter of a group
    p = sorted([u"<a title='%s'>%s</a>" % (x, short_name(x)) for x in self.groups.all()])
    if self.user_permissions.count(): p += ['+']
    value = ', '.join(p)
    return mark_safe("<nobr>%s</nobr>" % value)
roles.allow_tags = True
roles.short_description = u'Groups'

def adm(self):
    return self.is_superuser
adm.boolean = True
adm.admin_order_field = 'is_superuser'

def staff(self):
    return self.is_staff
staff.boolean = True
staff.admin_order_field = 'is_staff'

from django.core.urlresolvers import reverse
def persons(self):
    return ', '.join(['<a href="%s">%s</a>' % (reverse('admin:auth_user_change', args=(x.id,)), x.username) for x in self.user_set.all().order_by('username')])
persons.allow_tags = True

class UserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', staff, adm, roles]
    list_filter = ['groups', 'is_staff', 'is_superuser', 'is_active']

class GroupAdmin(GroupAdmin):
    list_display = ['name', persons]
    list_display_links = ['name']


# Register your models here.
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Ambiente, AmbienteAdmin)
#admin.site.register(Acesso, AcessoAdmin)
admin.site.register(Group, GroupAdmin)
#admin.site.register(Device, DeviceAdmin)
#admin.site.register(Log, LogAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(Zona, ZonaAdmin)

