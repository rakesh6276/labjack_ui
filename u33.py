import random

import pandas
import u3
import json
import pandas as pd
#import u6
#import ue9
#from pandas.tests.io.excel.test_xlrd import xlwt
import xlwt
#from IPython.utils import data
from urllib3.filepost import writer

if __name__ == '__main__':
    #print("This program shows how to work with Modbus and your LabJack U3, U6 or UE9. Registers are taken directly from the Modbus map (https://labjack.com/support/software/api/modbus/ud-modbus).\n")

    # print("Opening device.\n")
    # # Comment and uncomment below code based on the LabJack you are using.
    # # By default the U3 is opened.
    d = u3.U3()  # Opens first found U3 over USB
    # #d = u6.U6()  # Opens first found U6 over USB
    # #d = ue9.UE9()  # Opens first found UE9 over USB
    # # Opens a UE9 at IP Address 192.168.1.129
    # d = u3.U3(wifi=False, ipAddress="192.168.6.200")
    # print("config here",d)
    # print("configrations are below.\n")
    print(d.configU3())

    #def U3(self):
    import u3
    #data = []
    d = d.getCalibrationData()
    #a = d.configU3()
    #print(a)
    data =[d]
    print(data)
    with open('data3.json','w+',encoding='utf-8') as fp:
        #print(d)
        json.dump(data,fp)
    #
    import pandas
    pandas.read_json('data3.json').to_excel('output2.xlsx')
    #fp.close()

    # df =pd.read_json("data1.json")
    # print(df)
    #import pandas as pd
    #f =open("data2.json",'r')
    #message =f.read()
    #print(message)
    # with open('data2.json') as f:
    #     data4 =json.loads(f.read())
        #print(data4)
        #print(data[0]['text'])
        #json_data = json.load(open('data2.json'))
    import pandas as pd
    # import json
    #
    # import pandas
    # pandas.read_json("data2.json").to_excel("output.xlsx")
    #json_data = json.loads(open('data2.json'))
    #data = pd.read_json(json_data)
    #excel_file = pd.ExcelWriter('output.xlsx')
    #data.to_excel(writer, 'sheet1')
    #writer.save()
    # df = pd.DataFrame(json.load(open('data2.json')))
    # writer=pd.ExcelWriter('output.xlsx',engine='xlsxwriter')
    # df.to_excel(writer,sheet_name='sheet1')
    # writer.save()

    # book = request.FILES['excel_file']
    # df = pd.read_excel(book)
    # with open("data2.json") as datafile:
    #     data = json.load(datafile)
    # dataframe = pd.DataFrame(data)
    # print(dataframe)
    #import pandas
        #print(data)


    #print(d)
    #pandas.read_json("data.json",d).to_excel("output.xlsx")
    #print(pandas.read_excel('data.json'))
    # import codecs
    # import pandas as pd
    # pd.read_json(codecs.open('json_file', 'r', 'utf-8'))


# def dict_format(dictionary):
#     DataList = []
#     for d in range(len(dictionary[list(dictionary.keys())[0]])):
#         temp_dict = {}
#         for data in dictionary: temp_dict[data] = dictionary[data][d]
#         DataList.append(temp_dict)
#     return DataList
    #print(d.configU3())
    # d = u3.U3()
    # config = d.configU3()
    # print(config)
 #return JsonResponse(details, safe="False")
    #
    # isU3 = False
    # if isinstance(d, u3.U3):
    #     isU3 = True
    #     print(d)
    #
    # if isU3:
    #     print("Setting FIO0-3 to analog, and the rest to digital.\n")
    #     d.writeRegister(50590, 15)
    #
    # # Reading Analog Inputs.
    # print("Analog Inputs:")
    # for i in range(4):
    #     register = 0 + i*2  # Starting register 0, 2 registers at a time
    #     print("AIN%s (register %s): %s volts" % (i, register, d.readRegister(register)))
    #
    # # Reading Digital I/O
    # print("\nDigital I/O:\n")
    # for i in range(4):
    #     dirRegister = 6100 + i  # Starting register 6100, 1 register at a time
    #     stateRegister = 6000 + i  # Starting register 6000, 1 register at a time
    #     fio = i
    #     if isU3:
    #     state = d.readRegister(stateRegister)
    #     print("FIO%s (register %s) State: %s" % (fio, stateRegister, state))
    #
    #     if state == 0:
    #         state = 1
    #         wordState = "high"
    #     else:
    #         state = 0
    #         wordState = "low"
    #
    #     print("Setting FIO%s to output %s (register %s = %s)." % (fio, wordState, stateRegister, state))
    #     d.writeRegister(stateRegister, state)
    #
    #     print("FIO%s (register %s) Direction: %s" % (fio, dirRegister, d.readRegister(dirRegister)))
    #     print("FIO%s (register %s) State: %s\n" % (fio, stateRegister, d.readRegister(stateRegister)))
    #
    # # Seed the random number generator. Has nothing to do with Modbus.
    # random.seed()
    #
    # # Reading and writing to a DAC
    # print("Reading and writing to DACs:\n")
    # for i in range(2):
    #     dacRegister = 5000 + i*2  # Starting register 5000, 2 registers at a time
    #     print("DAC%s (register %s) reads %s volts." % (i, dacRegister, d.readRegister(dacRegister)))
    #
    #     voltage = float("%s.%s" % (random.randint(0, 4), random.randint(0, 9)))
    #     print("Setting DAC%s to %s volts." % (i, voltage))
    #     d.writeRegister(dacRegister, voltage)
    #     print("DAC%s (register %s) reads %s volts.\n" % (i, dacRegister, d.readRegister(dacRegister)))
    #
    #         fio = i+4
    #         dirRegister = 6100 + 4 + i
    #         stateRegister = 6000 + 4 + i
    #
    #     print("FIO%s (register %s) Direction: %s" % (fio, dirRegister, d.readRegister(dirRegister)))
    #
    #     state = d.readRegister(stateRegister)
    #     print("FIO%s (register %s) State: %s" % (fio, stateRegister, state))
    #
    #     if state == 0:
    #         state = 1
    #         wordState = "high"
    #     else:
    #         state = 0
    #         wordState = "low"
    #
    #     print("Setting FIO%s to output %s (register %s = %s)." % (fio, wordState, stateRegister, state))
    #     d.writeRegister(stateRegister, state)
    #
    #     print("FIO%s (register %s) Direction: %s" % (fio, dirRegister, d.readRegister(dirRegister)))
    #     print("FIO%s (register %s) State: %s\n" % (fio, stateRegister, d.readRegister(stateRegister)))
    #
    # # Seed the random number generator. Has nothing to do with Modbus.
    # random.seed()
    #
    # # Reading and writing to a DAC
    # print("Reading and writing to DACs:\n")
    # for i in range(2):
    #     dacRegister = 5000 + i*2  # Starting register 5000, 2 registers at a time
    #     print("DAC%s (register %s) reads %s volts." % (i, dacRegister, d.readRegister(dacRegister)))
    #
    #     voltage = float("%s.%s" % (random.randint(0, 4), random.randint(0, 9)))
    #     print("Setting DAC%s to %s volts." % (i, voltage))
    #     d.writeRegister(dacRegister, voltage)
    #     print("DAC%s (register %s) reads %s volts.\n" % (i, dacRegister, d.readRegister(dacRegister)))


