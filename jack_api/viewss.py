from django.http import HttpResponse, JsonResponse
import json
import u3
from pandas._libs import json
from pyzbar.pyzbar import decode
import cv2

device = None

def RegisterValue(self):
    global device
    global ainsRead
    global read
    global ser
    global json1
    global json_data

    if device is None:
        #initiate the connection for U3 library
        device = u3.U3(autoOpen=False)
        device.open(serial=320077464)

        #reading register values
        ainsRead = (device.getAIN(0),device.getAIN(1),device.getAIN(2),device.getAIN(3),device.getAIN(4),
                    device.getAIN(5),device.getAIN(6),device.getAIN(7),device.getAIN(8),device.getAIN(9),
                    device.getAIN(10),device.getAIN(11),device.getAIN(12),device.getAIN(13),device.getAIN(14),
                    device.getAIN(15))
        read = (ainsRead)

        #reading serial number
        serialnum = (device.configU3())
        #print(serialnum)
        ser = (serialnum)
        print(ser)
        #
        #reading calibrated data
        calibrate = (device.getCalibrationData())
        cal = (calibrate)
        print(cal)

        #adding hardcode values for low limit values
        lowlimit =[22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22]

        #adding hardcode for low limit keys
        #lowlimitkeys = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        #converting lowlimit/lowerlimit keys in dictinory format
        #dictionary = dict(zip(lowlimitkeys, lowlimit))

        #adding hardcode values for high limit values
        highlimit = [26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26]

        #adding hardcode for high limit keys
        #highlimitkeys = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        # converting highlimit/highlimit keys in dictinory format
       # dictionary1 = dict(zip(highlimitkeys, highlimit))

        #added test points for the registers
        testpoints = ["24V_DET","OUTPUT 1 LED","OUTPUT 2 LED","SYSTEM OK LED","VREF","FREQUNCY 1","FREQUNCY 2","MCLR","POWER OK LED","PULSE_A",
                      "OUTPUT_EN_BUF","PULSE_B","CH1_B","CH2_B","CH1_A","CH2_A"]

        #converting Json values for particular format
        json1 = [{'registervalues': read, "Min_LIMIT": lowlimit, "Max_LIMIT": highlimit, "Test_Points": testpoints} for read, lowlimit, highlimit, testpoints in zip(read, lowlimit, highlimit, testpoints)]

        #     ser_vref = [{"SerialNumber": ser, "Vref_value": cal }]


        #ser_vref = [{"SerialNumber": ser, "Vref_value": cal }]
        #print(ser_vref)
        #dumps the values for respective Json object
        json_data = json.dumps(json1)

        #return values in Json format
    return HttpResponse(json_data, content_type='application/json')



# def SerialValues(self):
#
#     global device
#     global ser_vref
#     #global ser_data
#
#     if device is None:
#         #initiate the connection for U3 library
#         device = u3.U3(autoOpen=False)
#         device.open(serial=320077464)
#
#         serialnum = (device.configU3())
#      # print(serialnum)
#         ser = (serialnum)
#         #print(ser)
#
#         # reading calibrated data
#         calibrate = (device.getCalibrationData())
#         cal = (calibrate)
#
#         ser_vref = {"SerialNumber": ser, "Vref_value": cal }
#                     #for ser, cal in zip(ser, cal)]
#
#        # ser_data = json.dumps(ser_vref)
#
#     return JsonResponse(ser_vref, safe = False)



    #return HttpResponse(ser_vref, content_type = 'application/json')
    #return HttpResponse(ser_vref, content_type = 'application/json')





#Api for reading barcode values in json format
def barcode(self):
    # filename = "barcodex.png"
    # img = cv2.imread(filename)
    # #img = np.full[filename(100, 80, 3), 12, np.uint8]
    # #print(img)

    img = cv2.imread('/home/asm/Desktop/labjack_Ui/labjack/jack_api/images/barcode_01.jpg')
    #print("image values are " + img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #print(gray_img)
    barcodes = decode(gray)
    return HttpResponse(barcodes, content_type='application/json')
        #print(barcodes)


