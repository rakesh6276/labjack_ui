#import simplejson
import numpy as np
from django.http import HttpResponse, JsonResponse
import json
import u3
import datetime
from datetime import datetime

from pandas._libs import json


from django.shortcuts import render
import os
import dbr

device = None

def getConfigIO(self):
    global device
    if device is None:
        device = u3.U3(autoOpen=False)
        device.open(serial=320077464)
        device.configIO()
    device.configIO()
    return JsonResponse(device.configIO())

#class GetCalibrate:
def getCalibrateData(self):
    global device
    datetimeObj = datetime.now()
    timeObj = datetimeObj.time()
    print(timeObj.strftime("%c"))
    if device is None:
        device = u3.U3(autoOpen=False)
        device.open(serial=320077464)
        v = device.getCalibrationData(self.vRefAtCAl )
        print(v)
    return JsonResponse(device.getCalibrationData())


def getConfigData(self):
    global device
    if device is None:
        device = u3.U3(autoOpen=False)
        device.open(serial=320077464)
        device.configU3(FIOAnalog=255, EIOAnalog=255)
    device.configU3()
    return JsonResponse(device.configU3())


def RegisterValue(self, SerialNumber=None):
    global device
    global ainsRead
    global read
    global ser
    global json1
    global  json2
    if device is None:
        device = u3.U3(autoOpen=False)
        device.open(serial=320077464)
        ainsRead = (device.getAIN(0),device.getAIN(1),device.getAIN(2),device.getAIN(3),device.getAIN(4),
                    device.getAIN(5),device.getAIN(6),device.getAIN(7),device.getAIN(8),device.getAIN(9),
                    device.getAIN(10),device.getAIN(11),device.getAIN(12),device.getAIN(13),device.getAIN(14),
                    device.getAIN(15))
        read = (ainsRead)
        serialnum = (device.configU3())
        ser = (serialnum)
        calibrate = (device.getCalibrationData())
        cal = (calibrate)
        lowlimit =[22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22]
        lowlimitkeys = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        dictionary = dict(zip(lowlimitkeys, lowlimit))
        # for q, a in zip(lowlimit, lowlimitkeys):
        #     print([qa])
        #dict([key,l_limit[]) for key in lowlimit])
        # t ="l_limit"
        # r = {k:t for k in lowlimit}
        highlimit = [26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26]
        highlimitkeys = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        dictionary1 = dict(zip(highlimitkeys, highlimit))
        #print(dictionary1[2])

        testpoints = ["24V_DET","OUTPUT 1 LED","OUTPUT 2 LED","SYSTEM OK LED","VREF","FREQUNCY 1","FREQUNCY 2","MCLR","POWER OK LED","PULSE_A",
                      "OUTPUT_EN_BUF","PULSE_B","CH1_B","CH2_B","CH1_A","CH2_A"]
        #registervalues
       # Dict ={}
        #print(ser)
    #return JsonResponse(read,ser, safe = False)
        # d = {}
        # for i in read:
        #      d[i] =["values"]
        # d = read[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        # json1 = [json1]

    #return HttpResponse(json.dumps({"registervalues":read, "serialnumber":ser, "Maxvalues":maxvalues}), content_type="application/json")
        json1 = [{'registervalues': read, 'serialnumber': ser, "LOW_LIMIT": dictionary, "High_LIMIT": dictionary1, "Test_Points": testpoints, "Calibrate_data": cal} for read, ser, dictionary, dictionary1, testpoints, cal in zip(read, ser, dictionary, dictionary1, testpoints, cal)]

        json2 = json.dumps(json1)
        # json1= json.dumps({
        #     "registervalues":[
        #
        #     {
        #         "values" : read,
        #         "serialnumber" : ser,
        #         "Maxvalues" : dictionary,
        #     },
        #     # {
        #     #     "values": read,
        #     #     "serialnumber": ser,
        #     #     "Maxvalues": dictionary,
        #     # },
        #     # {
        #     #     "values": read,
        #     #     "serialnumber": ser,
        #     #     "Maxvalues": dictionary,
        #     # }
        # ]
        # }
        # )
    return HttpResponse(json2, content_type='application/json')

# with open('example.json', 'w+', encoding='utf-8') as fp:
#     json.dump(read, fp
#
# import pandas
# data = pandas.read_json('example.json').to_csv('example.csv')


#
# def barcode(request):
#     #instantiate a drawing object
#     import barcode
#     d = barcode.MyBarcodeDrawing("HELLO WORLD")
#     binaryStuff = d.asString('gif')
#     return HttpResponse(binaryStuff, 'image/gif')


# Create your views here.
# def home(request):
#     return render(request, 'index.htm', {'what':'Online Barcode Reader with Django'})

# def upload(request):
#     if request.method == 'POST':
#         uploadedFile = handle_uploaded_file(request.FILES['RemoteFile'], str(request.FILES['RemoteFile']))
#         results = dbr.decodeFile(uploadedFile)
#         return HttpResponse(results)
#
#     return HttpResponse("Failed")
#
# @upload
# def handle_uploaded_file(file, filename):
#     if not os.path.exists('upload/'):
#         os.mkdir('upload/')
#
#     filePath = 'upload/' + filename
#
#     with open(filePath, 'wb+') as destination:
#         for chunk in file.chunks():
#             destination.write(chunk)
#
#     return filePath

#from qrtools import qrtools

from pyzbar.pyzbar import decode
import cv2
import numpy as np

def barcode(self):
    # filename = "barcodex.png"
    # img = cv2.imread(filename)
    # #img = np.full[filename(100, 80, 3), 12, np.uint8]
    # #print(img)

    img = cv2.imread('/home/asm/Desktop/labjack_Ui/labjack/jack_api/download.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #print(gray_img)
    barcodes = decode(gray)
    return HttpResponse(barcodes)
        #print(barcodes)

