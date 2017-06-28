'''
Created on 22 dic. 2016

@author: Marcos
'''
import serial
import time
from hp4192a.instrument.funciones import *
   
def funcion(puerto):
    ser = serial.Serial(puerto)     # open serial port
    ser.baudrate = 9600
    ser.flushInput()
    first=True
    while(1):
        if first:
            ser.readline()
            first=False
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
        data=[frecuencia,display_A, display_B]
        if data[1][1][0] and not data[1][1][1]:
            print ("Con errores")
        
        print('frecuencia: ', frecuencia, ' Display A', display_A, ' Display B', display_B)
    ser.close()
funcion("COM3")