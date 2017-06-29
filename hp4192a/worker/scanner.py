'''
Created on 21 jun. 2017

@author: User
'''

from PyQt4 import QtCore
from time import time, sleep
from hp4192a.instrument import funciones
import serial

class daq_worker(QtCore.QThread):
    def __init__(self):
        super(daq_worker,self).__init__()
        self.exiting=False
        self.ser= serial.Serial()
    def adquire(self,
                data_per_second, 
                outfile
                ):
        
        if not self.isRunning():
            self.outfile=outfile+'raw.dat'
            if data_per_second>0:
                self.delay=1/data_per_second
            else:
                self.delay=0

            self.start()
 
                   
    def run (self):
        x_zero= time()
        self.ser.open()
        ofile= open(self.outfile, 'a')
        sep='\t'
        while not self.exiting:
            
            self.ser.open()
            t = time()-x_zero
            
            values = self.ser.readline()
            
            freq=funciones.extraer_f(values)
            disp_a=funciones.extraer_A(values)
            disp_b=funciones.extraer_B(values)
            
            data=[t, freq, disp_a, disp_b]

            line = str(t)+sep+str(freq)+str(disp_a[0])+str 
            self.emit( QtCore.SIGNAL ( "readsignal(PyQt_PyObject)" ), data )
            sleep(self.delay)
        
        ofile.close()
        self.ser.close()
        self.exit()