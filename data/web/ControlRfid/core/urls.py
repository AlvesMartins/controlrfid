
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from access.viewsets import UserViewSet, DeviceViewSet, LogSerializer, DoorSerializer, DoorViewSet
from access.views import DeviceIDList, homepage, personal_info, device_info, global_charts, register, LogIDList, DoorIDList
from django.contrib.auth.views import login, logout

router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'device', DeviceViewSet)
router.register(r'log', LogSerializer)
router.register(r'door', DoorViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/1/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/1/device/(?P<code>.+)$', DeviceIDList.as_view()),
    url(r'^api/1/log/(?P<code>.+)$', LogIDList.as_view()),
    url(r'^api/1/door/(?P<code>.+)$', DoorIDList.as_view()),
    url(r'^commons/', include('commons.urls')),
    url(r'^accounts/profile/$', homepage, name='homepage'),
    url(r'^accounts/profile/info$', personal_info , name='personal_info'),
    url(r'^accounts/profile/device$', device_info , name='device_info'),
    url(r'^charts$', global_charts , name='gobal_charts'),
    url(r'^registration$', register , name='register'),
    url(
        r'^$', login,
        name='login',
    ),
    url(r'^logout/$',
        logout,
        name='logout',
    ),
]