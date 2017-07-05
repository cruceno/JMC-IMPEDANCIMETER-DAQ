'''
Created on 22 dic. 2016

@author: Marcos
'''
import serial
import time
from hp4192a.instrument.funciones import *
   
def funcion(puerto, da_order, db_order):
    ser = serial.Serial(puerto)     # open serial port
    ser.baudrate = 9600
    ser.flushInput()
    first=True
    sep='\t'
    while(1):

        if first:
            ofile=open('test_raw.txt', 'w')
            ofile.close()
            ser.readline()
            first=False
            zero_time=time.time()
        ofile=open('test_raw.txt', 'a')
        cadena = ser.readline()
        try:
            frecuencia = extraer_f(cadena)
        except:
            frecuencia = 'E'
        try:
            display_A = extraer_A(cadena)

        except:
            display_A = 'E'
 
        try:  
            display_B = extraer_B(cadena)

        except:
            display_B = 'E'
        data=[time.time()-zero_time,frecuencia,display_A, display_B]
        
        if data[2][1][0][0] and not data[2][1][1]:
            error=True
        if data[2][1][0][1] == da_order:
            pass
        elif data[2][1][0][1] < da_order:
            data[2][0]=data[2][0]*(da_order/data[2][1][0][1])
            
        elif data[2][1][0][1] > 1:
            data[2][0]=data[2][0]/(data[2][1][0][1]/da_order)
            
        if data[3][1][0][0] and not data[3][1][1]:
            error=True
        if data[3][1][0][1] == db_order:
            pass
        elif data[3][1][0][1] < db_order:
            data[3][0]=data[3][0]*(db_order/data[3][1][0][1])
            
        elif data[3][1][0][1] > db_order:
            data[3][0]=data[3][0]/(data[3][1][0][1]/db_order)
            
        line = str(data[0])+sep+"{0:.6f}".format(data[1])+sep+"{0:.12f}".format(data[2][0])+sep+"{0:.12f}".format(data[3][0])+'\n'
        print (line)
        ofile.write(line)
        ofile.close()
        
        #print('frecuencia: {0:.6f} '.format(data[1]), ' Display A', "{0:.12f}".format(data[2][0]), ' Display B', "{0:.12f}".format(data[3][0]))
    ser.close()
funcion("COM3", 1, 1)