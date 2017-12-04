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
                outputfile,
                da_order,
                db_order
                ):
        
        if not self.isRunning():
            if data_per_second>0:
                self.delay=1/data_per_second
            else:
                self.delay=0
            self.output = outputfile
            self.da_order = da_order
            self.db_order = db_order
            self.start()
 
    def set_untis_order(self, data, da_order, db_order):
           
        # Set correct order for display B
        medorder=data[2][1][0][1] #Measure order
        if medorder == da_order:
            pass
        elif medorder < da_order:
            data[2][0] = data[2][0]*(da_order/medorder)
            
        elif medorder > da_order:
            data[2][0]=data[2][0]/(medorder/da_order)
            
        # Set correct order for display B
        medorder=data[3][1][0][1] #Measure order
        if medorder == db_order:
            pass
        elif medorder < db_order:
            data[3][0]=data[3][0]*(db_order/medorder)
            
        elif medorder > db_order:
            data[3][0]=data[3][0]/(medorder/db_order)
        
        return data

    def check_data_units_integrity(self, data):

        displayA=data[2]
        displayB=data[3]
        
        if displayA[1][0][0] and not displayA[1][1]:
            print ('error',displayA[1][0][0], 'and', displayA[1][1] )
            return False
        
        if displayB[1][0][0] and not displayB[1][1]:
            print ('error',displayB[1][0][0], 'and', displayB[1][1] )
            return False
        return True     
            
    def run (self):
        x_zero= time()
        self.ser.open()
        
        sep='\t'
        counter=0
        while not self.exiting:
            t = time()-x_zero
            self.ser.flushInput()
            values = self.ser.readline()
            values = self.ser.readline()
            if len(values)==33:
                freq=funciones.extraer_f(values)
                disp_a=funciones.extraer_A(values)
                disp_b=funciones.extraer_B(values)
            
                data=[t, freq, disp_a, disp_b]
            
                if self.check_data_units_integrity(data):
                    data = self.set_untis_order(data, self.da_order, self.db_order)
                    line = str(data[0])+sep+"{0:.4f}".format(data[1])+sep+"{0:.12f}".format(data[2][0])+sep+"{0:.12f}".format(data[3][0])+'\n'
                    # print (line)
                    fsock = open(self.output, 'a+')
                    fsock.write(line)      
                    fsock.close()
                    counter+=1
                    if counter == 2:
                        self.emit( QtCore.SIGNAL ( "readsignal()" ) )
                        counter=0
                
            else:
                print('Error en el largo de la cadena',len(values))
            sleep(self.delay)
        
        self.ser.close()
        self.exit()