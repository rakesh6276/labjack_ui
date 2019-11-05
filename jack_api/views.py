#from cupshelpers import Device
from django.shortcuts import render

import collections
import sys
import warnings

from u3 import FeedbackCommand
from labjack import ljm


try:
    import ConfigParser
except ImportError: # Python 3
    import configparser as ConfigParser

from struct import pack, unpack

from LabJackPython import (
    Device,
    deviceCount,
    LabJackException,
    LowlevelErrorException,
    lowlevelErrorToString,
    MAX_USB_PACKET_LENGTH,
    setChecksum8,
    toDouble,
    )

from httplib2 import Response
from django.http import JsonResponse
from django.http import HttpResponse


FIO0, FIO1, FIO2, FIO3, FIO4, FIO5, FIO6, FIO7, \
EIO0, EIO1, EIO2, EIO3, EIO4, EIO5, EIO6, EIO7, \
CIO0, CIO1, CIO2, CIO3 = range(20)



class NullHandleException(LabJackException):
    """Raised when the return value of OpenDevice is null."""
    def __init__(self):
        self.errorString = "Couldn't open device. Please check that the device you are trying to open is connected."



# def openAllU3():
#     """
#     A helpful function which will open all the connected U3s. Returns a
#     dictionary where the keys are the serialNumber, and the serialNumbervalue is the device
#     object.
#     """
#     returnDict = dict()
#
#     for i in range(deviceCount(3)):
#
#         #d = U3("1234")
#         d = U3(firstFound = False, devNumber = i+1)
#         #d = U3(self)
#         print (d)
#         returnDict[str(d.serialNumber)] = d
#
#     return JsonResponse(returnDict)

#class U3(Device):

def U3(self):
    import u3
    import json
    #details = dict()
    details = u3.U3()
    details = details.getCalibrationData()
    #dac0_value = details.voltageToDACBits(1.5, dacNumber=0, is16Bits=True)
    #details = details.getFeedback(u3.DAC16(Dac=0, Value=dac0_value))
    #print(details)

    #details =details.configU3()
    #details = "11q1q1w"
    #d.open()
    #print(details)
    return JsonResponse(details, safe ="False")


    # def get(self, request):
    #     return HttpResponse(self.details)

    # import u3
    # d = u3.U3(autoOpen=False)
    # d.open(LJSocket="localhost:6000")

    def __init__(self, debug = False, autoOpen = True, **kargs):

        Device.__init__(self, None, devType=3)
        self.debug = debug
        self.calData = None
        self.ledState = True

    if autoOpen:
        self.open(**kargs)

    __init__.section = 1

    Device.open(self, 3, firstFound=firstFound, serial=serial, localId=localId, devNumber=devNumber,
                handleOnly=handleOnly, LJSocket=LJSocket)
    open.section = 1



    def configU3(self,LocalID=None, TimerCounterConfig=None, FIOAnalog=None, FIODirection=None, FIOState=None,
                 EIOAnalog=None, EIODirection=None, EIOState=None, CIODirection=None, CIOState=None, DAC1Enable=None,
                 DAC0=None, DAC1=None, TimerClockConfig=None, TimerClockDivisor=None, CompatibilityOptions=None,
                 result=None):

        writeMask = 0

        if FIOAnalog is not None or FIODirection is not None or FIOState is not None or EIOAnalog is not None or EIODirection is not None or EIOState is not None or CIODirection is not None or CIOState is not None:
            writeMask |= 2

        if DAC1Enable is not None or DAC0 is not None or DAC1 is not None:
            writeMask |= 4

        if LocalID is not None:
            writeMask |= 8

        if TimerClockConfig is not None or TimerClockDivisor is not None:
            writeMask |= 16

        if CompatibilityOptions is not None:
            writeMask |= 32

        command = [0] * 26

        # command[0] = Checksum8
        command[1] = 0xF8
        command[2] = 0x0A
        command[3] = 0x08
        # command[4] = Checksum16 (LSB)
        # command[5] = Checksum16 (MSB)
        command[6] = writeMask
        # command[7] = WriteMask1

        if LocalID is not None:
            command[8] = LocalID

        if TimerCounterConfig is not None:
            command[9] = TimerCounterConfig

        if FIOAnalog is not None:
            command[10] = FIOAnalog

        if FIODirection is not None:
            command[11] = FIODirection

        if FIOState is not None:
            command[12] = FIOState

        if EIOAnalog is not None:
            command[13] = EIOAnalog

        if EIODirection is not None:
            command[14] = EIODirection

        if EIOState is not None:
            command[15] = EIOState

        if CIODirection is not None:
            command[16] = CIODirection

        if CIOState is not None:
            command[17] = CIOState

        if DAC1Enable is not None:
            command[18] = DAC1Enable

        if DAC0 is not None:
            command[19] = DAC0

        if DAC1 is not None:
            command[20] = DAC1

        if TimerClockConfig is not None:
            command[21] = TimerClockConfig

        if TimerClockDivisor is not None:
            command[22] = TimerClockDivisor

        if CompatibilityOptions is not None:
            command[23] = CompatibilityOptions

        result = self._writeRead(command, 38, [0xF8, 0x10, 0x08])

        # Error-free, time to parse the response
        self.firmwareVersion = "%d.%02d" % (result[10], result[9])
        self.bootloaderVersion = "%d.%02d" % (result[12], result[11])
        self.hardwareVersion = "%d.%02d" % (result[14], result[13])
        self.serialNumber = unpack("<I", pack(">BBBB", *result[15:19]))[0]
        self.productId = unpack("<H", pack(">BB", *result[19:21]))[0]
        self.localId = result[21]
        self.timerCounterMask = result[22]
        self.fioAnalog = result[23]
        self.fioDirection = result[24]
        self.fioState = result[25]
        self.eioAnalog = result[26]
        self.eioDirection = result[27]
        self.eioState = result[28]
        self.cioDirection = result[29]
        self.cioState = result[30]
        self.dac1Enable = result[31]
        self.dac0 = result[32]
        self.dac1 = result[33]
        self.timerClockConfig = result[34]
        self.timerClockDivisor = result[35]
        if result[35] == 0:
            self.timerClockDivisor = 256

        self.compatibilityOptions = result[36]

        def configU3(self, LocalID=None, TimerCounterConfig=None, FIOAnalog=None, FIODirection=None, FIOState=None,
                 EIOAnalog=None, EIODirection=None, EIOState=None, CIODirection=None, CIOState=None, DAC1Enable=None,
                 DAC0=None, DAC1=None, TimerClockConfig=None, TimerClockDivisor=None, CompatibilityOptions=None):

   # def __init__(self, debug=False, autoOpen=True, **kargs):
            self.versionInfo = result[37]
            self.deviceName = 'U3'
            self.isHV = False
        if  self.versionInfo == 1:
            self.deviceName += 'B'
        elif self.versionInfo == 2:
            self.deviceName += '-LV'
        elif self.versionInfo == 18:
            self.deviceName += '-HV'
            self.isHV = True

        return JsonResponse ({'FirmwareVersion': self.firmwareVersion, 'BootloaderVersion': self.bootloaderVersion,
                'HardwareVersion': self.hardwareVersion, 'SerialNumber': self.serialNumber, 'ProductID': self.productId,
                'LocalID': self.localId, 'TimerCounterMask': self.timerCounterMask, 'FIOAnalog': self.fioAnalog,
                'FIODirection': self.fioDirection, 'FIOState': self.fioState, 'EIOAnalog': self.eioAnalog,
                'EIODirection': self.eioDirection, 'EIOState': self.eioState, 'CIODirection': self.cioDirection,
                'CIOState': self.cioState, 'DAC1Enable': self.dac1Enable, 'DAC0': self.dac0, 'DAC1': self.dac1,
                'TimerClockConfig': self.timerClockConfig, 'TimerClockDivisor': self.timerClockDivisor,
                'CompatibilityOptions': self.compatibilityOptions, 'VersionInfo': self.versionInfo,
                'DeviceName': self.deviceName})

    configU3.section = 2


    #def configIO(self, TimerCounterPinOffset = None, EnableCounter1 = None, EnableCounter0 = None, NumberOfTimersEnabled = None, FIOAnalog = None, EIOAnalog = None, EnableUART = None):
def configIO(self):
    import u3
    d = u3.U3()
    content = (d.configIO(FIOAnalog=0, EIOAnalog=0))
    return JsonResponse(content)

    """
        Name: U3.configIO(TimerCounterPinOffset = None, EnableCounter1 = None,
                          EnableCounter0 = None, NumberOfTimersEnabled = None,
                          FIOAnalog = None, EIOAnalog = None,
                          EnableUART = None)
    import u3
    d = u3.U3()
    content =(d.configIO(FIOAnalog = 0, EIOAnalog = 0))
    return JsonResponse(content)


        Args: See section 5.2.3 of the user's guide.

        Desc: The configIO command.

        Examples:
        Simplest:
        # >>> import u3
        # >>> d = u3.U3()
        # >>> print(d.configIO())
        {
         'NumberOfTimersEnabled': 0,
         'TimerCounterPinOffset': 4,
         'DAC1Enable': 0,
         'FIOAnalog': 239,
         'EIOAnalog': 0,
         'TimerCounterConfig': 64,
         'EnableCounter1': False,
         'EnableCounter0': False
        }

        Set all FIOs and EIOs to digital (until power cycle):
        import u3
        # >>> d = u3.U3()
        # >>> print(d.configIO(FIOAnalog = 0, EIOAnalog = 0))
        {
         'NumberOfTimersEnabled': 0,
         'TimerCounterPinOffset': 4,
         'DAC1Enable': 0,
         'FIOAnalog': 0,
         'EIOAnalog': 0,
         'TimerCounterConfig': 64,
         'EnableCounter1': False,
         'EnableCounter0': False
        }

        """

        # writeMask = 0
        #
        # if EIOAnalog is not None:
        #     writeMask |= 1
        #     writeMask |= 8
        #
        # if FIOAnalog is not None:
        #     writeMask |= 1
        #     writeMask |= 4
        #
        # if EnableUART is not None:
        #     writeMask |= 1
        #     writeMask |= (1 << 5)
        #
        # if TimerCounterPinOffset is not None or EnableCounter1 is not None or EnableCounter0 is not None or NumberOfTimersEnabled is not None :
        #     writeMask |= 1
        #
        # command = [ 0 ] * 12
        #
        # #command[0] = Checksum8
        # command[1] = 0xF8
        # command[2] = 0x03
        # command[3] = 0x0B
        # #command[4] = Checksum16 (LSB)
        # #command[5] = Checksum16 (MSB)
        # command[6] = writeMask
        # #command[7] = Reserved
        # command[8] = 0
        #
        # if EnableUART is not None and EnableUART:
        #     command[9] = 1 << 2
        #
        # if TimerCounterPinOffset is None:
        #     command[8] |= ( 4 & 15 ) << 4
        # else:
        #     command[8] |= ( TimerCounterPinOffset & 15 ) << 4
        #
        # if EnableCounter1 is not None and EnableCounter1:
        #     command[8] |= 1 << 3
        # if EnableCounter0 is not None and EnableCounter0:
        #     command[8] |= 1 << 2
        # if NumberOfTimersEnabled is not None:
        #     command[8] |= ( NumberOfTimersEnabled & 3 )
        #
        # if FIOAnalog is not None:
        #     command[10] = FIOAnalog
        #
        # if EIOAnalog is not None:
        #     command[11] = EIOAnalog
        #
        # #result = self._writeRead(command, 12, [0xF8, 0x03, 0x0B])
        # result = self._writeRead(command, 12, [0xF8, 0x03, 0x0B])
        #
        #
        # self.timerCounterConfig = result[8]
        #
        # self.numberTimersEnabled = self.timerCounterConfig & 3
        # self.counter0Enabled = bool( (self.timerCounterConfig >> 2) & 1 )
        # self.counter1Enabled = bool( (self.timerCounterConfig >> 3) & 1 )
        # self.timerCounterPinOffset = ( self.timerCounterConfig >> 4 )
        #
        #
        # self.dac1Enable = result[9]
        # self.fioAnalog = result[10]
        # self.eioAnalog = result[11]
        #
        # return HttpResponse ({'TimerCounterConfig' : self.timerCounterConfig,
        #          'DAC1Enable' : self.dac1Enable,
        #          'FIOAnalog' : self.fioAnalog,
        #          'EIOAnalog' : self.eioAnalog,
        #          'NumberOfTimersEnabled' : self.numberTimersEnabled,
        #          'EnableCounter0' : self.counter0Enabled,
        #          'EnableCounter1' : self.counter1Enabled,
        #          'TimerCounterPinOffset' : self.timerCounterPinOffset})
        #
        # configIO.section = 2


#class Counter(FeedbackCommand):
def Counter(FeedbackCommand):
    import u3
    d = u3.U3()
    d.debug = True
    content = d.configIO(EnableCounter0=True, FIOAnalog=15)
    return JsonResponse(content)
    #print(content)
    '''
    Counter Feedback command

    Reads a hardware counter, optionally resetting it

    counter: 0 or 1
    Reset: True ( or 1 ) = Reset, False ( or 0 ) = Don't Reset

    Returns the current count from the counter if enabled.  If reset,
    this is the value before the reset.
    import u3
    d = u3.U3()
    d.debug = True
    d.configIO(EnableCounter0 = True, FIOAnalog = 15)
    Sent:  [0x5f, 0xf8, 0x3, 0xb, 0x58, 0x0, 0x5, 0x0, 0x44, 0x0, 0xf, 0x0]
    Response:  [0x5a, 0xf8, 0x3, 0xb, 0x53, 0x0, 0x0, 0x0, 0x44, 0x0, 0xf, 0x0]
    {'NumberOfTimersEnabled': 0, 'TimerCounterPinOffset': 4, 'DAC1Enable': 0, 'FIOAnalog': 15, 'EIOAnalog': 0, 'TimerCounterConfig': 68, 'EnableCounter1': False, 'EnableCounter0': True}
    >>> d.getFeedback(u3.Counter(counter = 0, Reset = False))
    Sent:  [0x31, 0xf8, 0x2, 0x0, 0x36, 0x0, 0x0, 0x36, 0x0, 0x0]
    Response:  [0xfc, 0xf8, 0x4, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]
    [0]
    >>> # Tap a ground wire to counter 0
    >>> d.getFeedback(u3.Counter(counter = 0, Reset = False))
    Sent:  [0x31, 0xf8, 0x2, 0x0, 0x36, 0x0, 0x0, 0x36, 0x0, 0x0]
    Response:  [0xe9, 0xf8, 0x4, 0x0, 0xec, 0x0, 0x0, 0x0, 0x0, 0xe8, 0x4, 0x0, 0x0, 0x0]
    [1256]
    '''
    def __init__(self, counter, Reset = False):
        self.counter = counter
        self.reset = Reset
        self.cmdBytes = [54 + (counter % 2), int(bool(Reset))]

    readLen = 4

    def __repr__(self):
        return "<u3.Counter( counter = %s, Reset = %s )>" % (self.counter, self.reset)

    def handle(self, input):
        inStr = pack('B' * len(input), *input)
        return unpack('<I', inStr)[0]



#class Counter1(Counter):


#class Counter0(Counter):
def Counter0(Counter):
    import u3
    d = u3.U3()
    d.debug = True
    content = d.configIO(EnableCounter0=True, FIOAnalog=15)

    def __init__(self, Reset=False):
        Counter.__init__(self, 0, Reset)

    def __repr__(self):
         return "<u3.Counter0( Reset = %s )>" % self.reset
    return JsonResponse(content)

'''
    Counter0 Feedback command

    Reads hardware counter0, optionally resetting it

    Reset: True ( or 1 ) = Reset, False ( or 0 ) = Don't Reset

    Returns the current count from the counter if enabled.  If reset,
    this is the value before the reset.

     import u3
     d = u3.U3()
    d.debug = True
    d.configIO(EnableCounter0 = True, FIOAnalog = 15)
    Sent:  [0x5f, 0xf8, 0x3, 0xb, 0x58, 0x0, 0x5, 0x0, 0x44, 0x0, 0xf, 0x0]
    Response:  [0x5a, 0xf8, 0x3, 0xb, 0x53, 0x0, 0x0, 0x0, 0x44, 0x0, 0xf, 0x0]
    {'NumberOfTimersEnabled': 0, 'TimerCounterPinOffset': 4, 'DAC1Enable': 0, 'FIOAnalog': 15, 'EIOAnalog': 0, 'TimerCounterConfig': 68, 'EnableCounter1': False, 'EnableCounter0': True}
    >>> d.getFeedback(u3.Counter0( Reset = False ) )
    Sent:  [0x31, 0xf8, 0x2, 0x0, 0x36, 0x0, 0x0, 0x36, 0x0, 0x0]
    Response:  [0xfc, 0xf8, 0x4, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]
    [0]
    >>> # Tap a ground wire to counter 0
    >>> d.getFeedback(u3.Counter0(Reset = False))
    Sent:  [0x31, 0xf8, 0x2, 0x0, 0x36, 0x0, 0x0, 0x36, 0x0, 0x0]
    Response:  [0xe, 0xf8, 0x4, 0x0, 0x11, 0x0, 0x0, 0x0, 0x0, 0x11, 0x0, 0x0, 0x0, 0x0]
    [17]
    >>> # Tap a ground wire to counter 0
    >>> d.getFeedback(u3.Counter0(Reset = False))
    Sent:  [0x31, 0xf8, 0x2, 0x0, 0x36, 0x0, 0x0, 0x36, 0x0, 0x0]
    Response:  [0x19, 0xf8, 0x4, 0x0, 0x1c, 0x0, 0x0, 0x0, 0x0, 0xb, 0x11, 0x0, 0x0, 0x0]
    [4363]
    '''
    # def __init__(self, Reset = False):
    #     Counter.__init__(self, 0, Reset)
    #
    # def __repr__(self):
    #     return "<u3.Counter0( Reset = %s )>" % self.reset

def Counter1(Counter):
    import u3
    d = u3.U3()
    d.debug = True
    content = d.configIO(EnableCounter1=True, FIOAnalog=15)
    #return JsonResponse(content)
    def __init__(self, Reset=False):
        Counter.__init__(self, 1, Reset)

    def __repr__(self):
        return "<u3.Counter0( Reset = %s )>" % self.reset
    # return JsonResponse(content)
#
#

# DEVICE_TYPES = {ljm.constants.dtT7: "T7",
#                 ljm.constants.dtT4: "T4",
#                 ljm.constants.dtDIGIT: "Digit"}
# CONN_TYPES = {ljm.constants.ctUSB: "USB",
#               ljm.constants.ctTCP: "TCP",
#               ljm.constants.ctETHERNET: "Ethernet",
#               ljm.constants.ctWIFI: "WiFi"}




    #info = self.info
    # """Displays the LabJack devices information from listAll or
    # listAllS.
    #
    # Args:
    #    functionName: The name of the function used
    #    info: tuple returned by listAll or listAllS

    """
    # print("\n%s found %i LabJacks:\n" % (functionName, info[0]))
    # fmt = ''.join(["{%i:<18}" % i for i in range(0, 4)])
    # print(fmt.format("Device Type", "Connection Type", "Serial Number",
    #                  "IP Address"))
    # for i in range(info[0]):
    #     print(fmt.format(DEVICE_TYPES.setdefault(info[1][i], str(info[1][i])),
    #                      CONN_TYPES.setdefault(info[2][i], str(info[2][i])),
    #                      str(info[3][i]), ljm.numberToIP(info[4][i])))



# listAll and listAllS returns the tuple (numFound, aDeviceTypes,
# aConnectionTypes, aSerialNumbers, aIPAddresses)

# Find and display LabJack devices with listAllS.
#     info = ljm.listAllS("ANY", "ANY")
#     displayDeviceInfo("listAllS", info)

"""
# Find and display LabJack devices with listAll.
# info = ljm.listAll(ljm.constants.ctANY, ljm.constants.ctANY)
# displayDeviceInfo("listAll", info)
# """


# from labjack import ljm
#
# # Open first found LabJack
# #handle = ljm.openS("ANY", "ANY", "ANY")
#
# # Call eReadName to read the serial number from the LabJack.
# name = "SERIAL_NUMBER"
# result = ljm.eReadName(handle, name)
#
# print("\neReadName result: ")
# print("    %s = %f" % (name, result))


def getCalibrationData(self):
    """
    Name: U3.getCalibrationData()

    Args: None

    Desc: Reads in the U3's calibrations, so they can be applied to
          readings. Section 2.6.2 of the User's Guide is helpful. Sets up
          an internal calData dict for any future calls that need
          calibration.
    """
    self.calData = dict()

    calData = self.readCal(0)

    self.calData['lvSESlope'] = toDouble(calData[0:8])
    self.calData['lvSEOffset'] = toDouble(calData[8:16])
    self.calData['lvDiffSlope'] = toDouble(calData[16:24])
    self.calData['lvDiffOffset'] = toDouble(calData[24:32])

    calData = self.readCal(1)

    self.calData['dac0Slope'] = toDouble(calData[0:8])
    self.calData['dac0Offset'] = toDouble(calData[8:16])
    self.calData['dac1Slope'] = toDouble(calData[16:24])
    self.calData['dac1Offset'] = toDouble(calData[24:32])

    calData = self.readCal(2)

    self.calData['tempSlope'] = toDouble(calData[0:8])
    self.calData['vRefAtCAl'] = toDouble(calData[8:16])
    self.calData['vRef1.5AtCal'] = toDouble(calData[16:24])
    self.calData['vRegAtCal'] = toDouble(calData[24:32])

    try:
        # these blocks do not exist on hardware revisions < 1.30
        calData = self.readCal(3)

        self.calData['hvAIN0Slope'] = toDouble(calData[0:8])
        self.calData['hvAIN1Slope'] = toDouble(calData[8:16])
        self.calData['hvAIN2Slope'] = toDouble(calData[16:24])
        self.calData['hvAIN3Slope'] = toDouble(calData[24:32])

        calData = self.readCal(4)

        self.calData['hvAIN0Offset'] = toDouble(calData[0:8])
        self.calData['hvAIN1Offset'] = toDouble(calData[8:16])
        self.calData['hvAIN2Offset'] = toDouble(calData[16:24])
        self.calData['hvAIN3Offset'] = toDouble(calData[24:32])
    except LowlevelErrorException:
        ex = sys.exc_info()[1]
        if ex.errorCode != 26:
            # not an invalid block error, so do not disregard
            raise ex

    return self.calData


getCalibrationData.section = 3


from labjack import ljm

def displayDeviceInfo(self):

# Open first found LabJack
    #handle = ljm.openS("ANY", "ANY", "ANY")  # Any device, Any connection, Any identifier
    handle = ljm.openS("T7", "ANY", "ANY")  # T7 device, Any connection, Any identifier
#handle = ljm.openS("T4", "ANY", "ANY")  # T4 device, Any connection, Any identifier
    #handle = ljm.open(ljm.constants.dtANY, ljm.constants.ctANY, "ANY")  # Any device, Any connection, Any identifier

    info = ljm.getHandleInfo(handle)
    print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
      "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
      (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))

# Setup and call eWriteName to write a value to the LabJack.
    name = "DAC0"
    value = 2.5  # 2.5 V
    ljm.eWriteName(handle, name, value)

    print("\neWriteName: ")
    print("    Name - %s, value : %f" % (name, value))

# Close handle
    ljm.close(handle)





