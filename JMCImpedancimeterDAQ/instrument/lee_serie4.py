'''
Created on 22 dic. 2016

@author: Marcos
'''
import serial
import time
from JMCImpedancimeterDAQ.instrument.funciones import *
   
def funcion(puerto):
    ser = serial.Serial(puerto)     # open serial port
    ser.baudrate = 9600
    ser.flushInput()
    first=True
    while(1):
        if first:
            ser.readline()
            first=False
        cadena = ser.read(31)
        print (cadena)
        try:
            frecuencia = extraer_f(cadena)
        except:
            frecuencia = 'E'
        try:
            display_A = extraer_A(cadena)
            unidad_AA = unidad_A(cadena)
        except:
            display_A = 'E'
            unidad_AA = 'E' 
        try:  
            display_B = extraer_B(cadena)
            unidad_BB = unidad_B(cadena)
        except:
            display_B = 'E'
            unidad_BB = 'E'
        print('frecuencia: ', frecuencia, ' Display A', display_A, unidad_AA, ' Display B', display_B, unidad_BB)
    ser.close()
    
funcion("/dev/ttyUSB0")