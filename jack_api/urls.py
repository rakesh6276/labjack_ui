
from django.urls import path
# from jack_api.viewss import getConfigData,getConfigIO,getCalibrateData,\

from jack_api.viewss import RegisterValue, barcode\
    #, SerialValues


urlpatterns = [
    path('register',RegisterValue),
    path('barcode', barcode),
    #path('serial', SerialValues)
]