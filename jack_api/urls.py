from django.urls import path
# from rest_framework import routers

from jack_api import views

from jack_api import u3

from jack_api import LabJackPython

# router = routers.DefaultRouter()
# router.register(r'jack', views.U3)
#router.register(r'groups', views.GroupViewSet)
from jack_api.u3 import AIN, WaitShort, DAC0_8, U3, DAC8
from jack_api.views import getCalibrationData

urlpatterns = [
    #path('', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    path('getconfig', views.U3),
    path('confio',views.configIO),
    path('counter1', views.Counter1),
    path('counter0', views.Counter0),
    path('counter', views.Counter),
    path('displaydevice', views.displayDeviceInfo),
    path('labjackexception', views.LabJackException),
    # path('datau3', views.U3),
    #path('open', views.openAllU3),
    path('aa', WaitShort),
    path('dac0', DAC0_8),
    path('u8',DAC8)
    ]