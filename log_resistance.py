"""
Read from Agilent datalogger, write to Compactlogix tag
Nick Hotto 2021
"""

import pyvisa
import time
import csv
import os
import sys
from pylogix import PLC
sys.path.append('..')

#Address of Agilent Unit
visa_address = 'TCPIP0::172.30.21.181::inst0::INSTR'

VisaAddress = visa_address

rm=pyvisa.ResourceManager()
inst = rm.open_resource(VisaAddress)

#Initalize Variables
DUT = 0
a = 0
period = 0
t_period = 0

#Instrument Identity
inst.write("*IDN?")

"""
#External Datalogger - Resistance Measurements
#Enable Elog Resistance Measurement
inst.write("SENS:ELOG:FUNC:RES ON,(03)")
#Enable Elog Resistance Min/Max Measurement
inst.write("SENS:ELOG:FUNC:RES:MINM ON,(03)")
#Set Elog Integration period to 1ms
inst.write("SENS:ELOG:PER .01, (03)")
#Query integration period that data is fetched
inst.write("SENS:ELOG:PER? (03)")
period = inst.read()
t_period = period
#Select Trigger Source - Bus
inst.write("TRIG:TRAN:SOUR BUS,(03)")
#Initiate Elog
inst.write("INIT:ELOG (03)")
#Delay by .1s
time.sleep(0.1)
#Trigger Elog
inst.write("TRIG:ELOG (03)")
#Check for error
#inst.write("SYST:ERR?")
#print(inst.read())
"""
#Measurement Functions
#Config
#inst.write("SENS:FUNC:ON?")
#MAX RES
# MEASure:{RESistance|FRESistance}? [{<range>|AUTO|MIN|MAX|DEF} [, {<resolution>|MIN|MAX|DEF}]]

with PLC() as comm:
    comm.IPAddress = '172.30.21.130'
    write = True
    while write:
        meas_resistance = inst.write("MEAS:RES?")
        comm.Write('ResistanceA', meas_resistance)
        time.sleep(0.1)

"""
#Retrieve External Datalogger Output

#Periodically retrieve current measurements

with open('Elog_Current_Measurement.csv', mode='w',newline='')as f:
    f_writer = csv.writer(f)
    #Create column headers on csv file
    f_writer.writerow([' Time(s)', 'Current(A)', 'Imax(A)', 'Imin(A)'])
    #Retrieve measurements of maximum 1000 records
    print('External Data Logger is initiated and running')

    #Log measurements for a duration of 1 second
    for i in range(0, 1):
        inst.write("FETC:ELOG? 1000, (03)")
        DUT=inst.read()
        x = DUT.split(",")
        while (a<len(x)):
            #Write measurement results to csv file
            f_writer.writerow([t_period,x[a], x[a+1], x[a+2], x[a+3]])
            a = a + 4;
            t_period = float(t_period) = float(period);
        a=0;
        time.sleep(0.8)
        print('Data is logging...')

    #Abort Elog
    inst.write("ABOR:ELOG (03)")
    print("External Datalog Completed")
"""
