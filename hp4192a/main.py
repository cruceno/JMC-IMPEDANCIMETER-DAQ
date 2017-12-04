# -*- coding: utf-8 -*-
'''
Created on 19 abr. 2017

@author: cruce
'''
# Importar librerias del sistema
import os
import sys
import time
# Importar libreria para manejo de archivos de configuracion
from configobj import ConfigObj
# importar libreria para el manejo de datos numericos
import numpy as np
# Importar backends y librerias necesarias para graficar los datos
# Importar librerias de interfaz grafica
from PyQt4 import QtGui, QtCore

from hp4192a.gui.mainwindow import Ui_HP4192A
from hp4192a.ploter.qtmatplotlib import canvas as PlotCanvas
from hp4192a.instrument.serialutil import scan_serial_ports
from hp4192a.worker.scanner import daq_worker


class HP4192AuiAPP(QtGui.QMainWindow, Ui_HP4192A):
    """La ventana principal de la aplicacion."""

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        # Cargamos la interfaz grafica
        # Create a pixmap - not needed if you have your own.
        from hp4192a.gui.splash import SplashScreen
        pixmap = QtGui.QPixmap('./gui/images/splash.png')
        self.splash = SplashScreen(pixmap)
        self.splash.setTitle('HP 4192a LF')
        self.splash.moveTitle(46*self.splash.width()/100,
                              10*self.splash.height()/100,
                              50*self.splash.width()/100,
                              30*self.splash.height()/100)
        self.splash.show()
        self.splash.connect(self,
                   QtCore.SIGNAL('splashUpdate(QString, int)'),
                   self.splash.showMessage)
        self.setupUi(self)
        self.set_ui_display_orders()
        self.gb_capacitance.setEnabled(False)
        self.gb_impedance.setEnabled(False)
        self.gb_error_filters.setEnabled(False)
        
        # Cargamos archivo de configuracion predeterminado
        # Estudiar caso en que el archivo de configuracion no exista
        self.config = ConfigObj('hp4192a.ini')
        from hp4192a.ploter.qtmatplotlib import NavigationToolbar
        # Inicializando base de ploteo para daq mainplot Data Analisys Tab
        self.vbl_tab_plot_a = QtGui.QVBoxLayout(self.tab_plot_a)
        self.plota_canvas = PlotCanvas(self.tab_plot_a)
        self.vbl_tab_plot_a.insertWidget(0, self.plota_canvas)
        self.plot_a_tb = NavigationToolbar(self.plota_canvas, self.tab_plot_a)
        self.vbl_tab_plot_a.insertWidget(1, self.plot_a_tb)
        self.cbx_x_plot_a.setCurrentIndex(2)
        self.cbx_y_plot_a.setCurrentIndex(0)
        # Inicializando base de ploteo para daq mainplot Data Analisys Tab
        self.vbl_tab_plot_b = QtGui.QVBoxLayout(self.tab_plot_b)
        self.plotb_canvas = PlotCanvas(self.tab_plot_b)
        self.vbl_tab_plot_b.insertWidget(0, self.plotb_canvas)
        self.plot_b_tb = NavigationToolbar(self.plotb_canvas, self.tab_plot_b)
        self.vbl_tab_plot_b.insertWidget(1, self.plot_b_tb)
        self.cbx_x_plot_b.setCurrentIndex(2)
        self.cbx_y_plot_b.setCurrentIndex(1)
        
    def connect_thread(self):
        
        self.emit(QtCore.SIGNAL("splashUpdate(QString, int)"),
                  'Connect to thread . . .',
                  132)
        self.scaner= daq_worker()
        # Configurar subproceso encargado de la comunicacion con el OMA
        self.thread = QtCore.QThread()
        self.thread.started.connect(self.scaner.adquire)
        self.connect(self.scaner, QtCore.SIGNAL("finished()"), self.thread.quit)
        # Conectar señales y funciones
        self.connect(self.scaner, QtCore.SIGNAL("readsignal()"), self.incoming_data)
        #self.connect(self.scaner, QtCore.SIGNAL("msgsignal(PyQt_PyObject)"), self.change_messagge)

        self.scaner.moveToThread(self.thread)
        
    def get_serial_config(self):
        self.emit(QtCore.SIGNAL("splashUpdate(QString, int)"),
                  'Loading conected devices . . .',
                  132)
        
        # Obtener listado de puertos serie presentes en el equipo
        ports = scan_serial_ports(30,False )
        self.set_ui_serial_controls(ports)
        # Acceder a la configuracion guardada
        serialConfig = self.config['serialConfig']
        # Instanciar objeto serial

        if(serialConfig['port'] != '' and serialConfig['port'] in ports):
            self.scaner.ser.port = serialConfig['port']
            self.cbx_serial_port.setCurrentIndex(self.cbx_serial_port.findText(serialConfig['port']))
        else:
            self.scaner.ser.port = ports[0][1]
            self.cbx_serial_port.setCurrentIndex(self.cbx_serial_port.findText(self.scaner.ser.name))
        if(serialConfig['baudrate'] != '' and serialConfig['baudrate'] in self.scaner.ser.BAUDRATES):
            self.scaner.ser.baudrate = serialConfig['baudrate']
            self.cbx_serial_baudrates.setCurrentIndex(self.cbx_serial_baudrates.findData(serialConfig['baudrate']))
        else:
            self.cbx_serial_baudrates.setCurrentIndex(self.cbx_serial_baudrates.findData(self.scaner.ser.baudrate))
        if(serialConfig['parity'] != '' and serialConfig['parity'] in self.scaner.ser.PARITIES):
            self.scaner.ser.parity = serialConfig['parity']
            self.cbx_serial_parities.setCurrentIndex(self.cbx_serial_parities.findData(serialConfig['parity']))
        else:
            self.cbx_serial_parities.setCurrentIndex(self.cbx_serial_parities.findData(self.scaner.ser.parity))
        if(serialConfig['stopbits'] != '' and serialConfig['stopbits'] in self.scaner.ser.STOPBITS):
            self.scaner.ser.stopbits = serialConfig['stopbits']
            self.cbx_serial_stopbits.setCurrentIndex(self.cbx_serial_stopbits.findData(serialConfig['stopbits']))
        else:
            self.cbx_serial_stopbits.setCurrentIndex(self.cbx_serial_stopbits.findData(self.scaner.ser.stopbits))
        if(serialConfig['bytesize'] != '' and serialConfig['bytesize'] in self.scaner.ser.BYTESIZES):
            self.scaner.ser.byteSize = serialConfig['bytesize']
            self.cbx_serial_bytesizes.setCurrentIndex(self.cbx_serial_bytesizes.findData(serialConfig['bytesize']))
        else:
            self.cbx_serial_bytesizes.setCurrentIndex(self.cbx_serial_bytesizes.findData(self.scaner.ser.bytesize))
        self.sp_serial_timeout.setValue(int(serialConfig['timeout']))
        
    def set_ui_serial_controls(self, ports=[]):
    
            ''' Esta funcion es la encargada de autocompletar la informacion necesaria
            en la interfaz grafica para la configuracion de la comunicacion por puerto serie
            '''
            from serial import SerialBase
    
            # Pasar listado de puertos serie disponibles a campo de seleccion en la interfaz gr�fica
            for i in range(self.cbx_serial_port.count()):
                # Si hay algun item en el combobox removerlo
                self.cbx_serial_port.removeItem(i)
            for port in ports:
                # Agregar cada puerto serie disponible como item del combobox
                self.cbx_serial_port.addItem(port[1])
    
            # Listar configuraciones de baudrates posibles
            for i in range(self.cbx_serial_baudrates.count()):
                # Si hay algun item en el combobox removerlo
                self.cbx_serial_baudrates.removeItem(i)
            for baudrate in SerialBase.BAUDRATES:
                # Agregar configuraciones disponibles al campo de seleccion
                self.cbx_serial_baudrates.addItem(str(baudrate), baudrate)
    
            # Listar configuraciones de paridad posibles
            for i in range(self.cbx_serial_parities.count()):
                # Si hay algun item en el combobox removerlo
                self.cbx_serial_parities.removeItem(i)
    
            parities_texts = {'N': 'None', 'E': 'Even', 'O': 'Odd', 'M': 'Mark', 'S': 'Space'}
            for parity in SerialBase.PARITIES:
                # Agregar configuraciones disponibles al campo de seleccion
                self.cbx_serial_parities.addItem(parities_texts[parity], parity)
    
            # Listar configuraciones de stopbits posibles
            for i in range(self.cbx_serial_stopbits.count()):
                # Si hay algun item en el combobox removerlo
                self.cbx_serial_stopbits.removeItem(i)
            for stopbit in SerialBase.STOPBITS:
                # Agregar configuraciones disponibles al campo de seleccion
                self.cbx_serial_stopbits.addItem(str(stopbit), stopbit)
    
            # Listar configuraciones de bytsizes posibles
            for i in range(self.cbx_serial_bytesizes.count()):
                # Si hay algun item en el combobox removerlo
                self.cbx_serial_bytesizes.removeItem(i)
            for bytesize in SerialBase.BYTESIZES:
                # Agregar configuraciones disponibles al campo de seleccion
                self.cbx_serial_bytesizes.addItem(str(bytesize), bytesize)
    
    def set_ui_display_orders(self):
        from hp4192a.instrument.funciones import orders as orders
        self.cbx_file_display_a_order.addItem('Pico', orders['p'][1])
        self.cbx_file_display_b_order.addItem('Pico', orders['p'][1])
        self.cbx_file_display_a_order.addItem('Nano', orders['n'][1])
        self.cbx_file_display_b_order.addItem('Nano', orders['n'][1])
        self.cbx_file_display_a_order.addItem('Micro', orders['u'][1])
        self.cbx_file_display_b_order.addItem('Micro', orders['u'][1])
        self.cbx_file_display_a_order.addItem('Mili', orders['m'][1])
        self.cbx_file_display_b_order.addItem('Mili', orders['m'][1])
        self.cbx_file_display_a_order.addItem('Base', orders['base'][1])
        self.cbx_file_display_a_order.setCurrentIndex(4)
        self.cbx_file_display_b_order.addItem('Base', orders['base'][1])
        self.cbx_file_display_b_order.setCurrentIndex(4)
        self.cbx_file_display_a_order.addItem('Kilo', orders['k'][1])
        self.cbx_file_display_b_order.addItem('Kilo', orders['k'][1])        
        self.cbx_file_display_a_order.addItem('Mega', orders['M'][1])
        self.cbx_file_display_b_order.addItem('Mega', orders['M'][1])
        
    @QtCore.pyqtSlot()
    def on_cbx_serial_port_currentIndexChanged(self):
        port = self.cbx_serial_port.itemData(self.cbx_serial_port_currentIndex())
        self.config['serialConfig']['port'] = port
        self.scaner.ser.port(port)

    @QtCore.pyqtSlot()
    def on_cbx_serial_baudrates_currentIndexChanged(self):
        baudrate = self.cbx_serial_baudrates.itemData(self.cbx_serial_baudrates_currentIndex())
        self.config['serialConfig']['baudrate'] = baudrate
        self.scaner.ser.baudrate(baudrate)

    @QtCore.pyqtSlot()
    def on_cbx_serial_parities_currentIndexChanged(self):
        parity = self.cbx_serial_parities.itemData(self.cbx_serial_parities_currentIndex())
        self.config['serialConfig']['parity']=parity
        self.scaner.ser.parity(parity)

    @QtCore.pyqtSlot()
    def on_cbx_serial_bytesizes_currentIndexChanged(self):
        bytesize = self.cbx_serial_bytesizes.itemData(self.cbx_serial_bytesizes_currentIndex())
        self.config['serialConfig']['bytesize']=bytesize
        self.scaner.ser.bytesize(bytesize)

    @QtCore.pyqtSlot()
    def on_cbx_serial_stopbits_currentIndexChanged(self):
        stopbits=self.cbx_serial_stopbits.itemData(self.cbx_serial_stopbits_currentIndex())
        self.config['serialConfig']['stopbits']=stopbits
        self.scaner.ser.stopbits(stopbits)
    @QtCore.pyqtSlot()
    def on_gb_capacitance_clicked(self):
        if self.gb_capacitance.isChecked():
            self.gb_impedance.setChecked(False)
    
    @QtCore.pyqtSlot()
    def on_gb_impedance_clicked(self):
        if self.gb_impedance.isChecked():
            self.gb_capacitance.setChecked(False)
            
    @QtCore.pyqtSlot()
    def update_ui(self):

        pass
    
    @QtCore.pyqtSlot()
    def incoming_data(self):
        sep = '\t' if self.config['fileFormat']['column_sep'] == 'Tab' else ','
        rawpath=self.le_outputfile.text()+'.raw'
        
        if os.path.isfile(rawpath):
            rawfile=open(rawpath, 'r')
            
            if len(rawfile.readlines()) >= 5:
    
                t, f, da, db = np.genfromtxt(rawpath,
                                             dtype='float',
                                             delimiter=sep,
                                             usecols=(0,1,2,3),
                                             unpack=True
                                             )
            
                vars_to_plot={'t':t,'a':da, 'f':f, 'b':db}  
                #self.plota_canvas.axes.cla()
                
                self.plota_canvas.plot(vars_to_plot[self.cbx_x_plot_a.itemData(self.cbx_x_plot_a.currentIndex())],
                                        vars_to_plot[self.cbx_y_plot_a.itemData(self.cbx_y_plot_a.currentIndex())])
                #self.plotb_canvas.axes.cla()
                self.plotb_canvas.plot(vars_to_plot[self.cbx_x_plot_b.itemData(self.cbx_x_plot_b.currentIndex())],
                                        vars_to_plot[self.cbx_y_plot_b.itemData(self.cbx_y_plot_b.currentIndex())])
            
    #          if self.check_data_units_integrity(data):
    #                 data = self.set_untis_order(data)
    #                 if self.check_for_error_values([data[1],data[2][0],data[3][0]], [f[-1],da[-1],db[-1]]):
    #                     rawfile = open(rawpath,'a')
    #                     line = str(data[0])+sep+"{0:.4f}".format(data[1])+sep+"{0:.12f}".format(data[2][0])+sep+"{0:.12f}".format(data[3][0])+'\n'
    #                     rawfile.write(line)
            else:
                self.change_message('Esperando datos validos para plotear')
    
            rawfile.close()
        
    def check_for_error_values(self, data, data2):
        f_start = self.dsb_f_start.value()
        f_stop = self.dsb_f_stop.value()
        f_steep = self.dsb_f_step.value()
         
        if abs (abs(data[0])-abs(data2[0])) < (10*abs(data[0])/100):
            pass
        else:
            msg='Medicion con errores frecuencia:'+'{0:.4f}'.format(data[0])+' , '+'{0:.12f}'.format(data2[0])+' , {0:.12f}'.format(10*data[0]/100)
            print (msg)
            self.change_message(msg)
            return False
        if abs(abs(data[1])-abs(data2[1])) < (10*abs(data[1])/100):
            pass
        else:
            msg='Medicion con errores frecuencia:'+'{0:.4f}'.format(data[1])+' , '+'{0:.12f}'.format(data2[1])+' , {0:.12f}'.format(10*data[1]/100)
            print (msg)
            self.change_message(msg)
            return False
        if abs (abs(data[2])-abs(data2[2])) < (10*abs(data[2])/100):
            pass
        else:
            msg='Medicion con errores frecuencia:'+'{0:.4f}'.format(data[2])+' , '+'{0:.12f}'.format(data2[2])+' , {0:.12f}'.format(10*data[2]/100)
            print (msg)
            self.change_message(msg)
            return False        
        return True
    
    def enable_ui_controls(self, enable):
        
        self.plot_settings.setEnabled(enable)
        self.save_data_settings.setEnabled(enable)
        self.config_inputs.setEnabled(enable)
        
    def change_message(self, msg):
        self.statusBar().showMessage(msg, 5000) 
           
    @QtCore.pyqtSlot()
    def on_pb_start_pressed(self):
        if self.pb_start.text() == 'Start':
            self.plota_canvas.axes.cla()
            self.plotb_canvas.axes.cla()
            try:
                outputfile=self.le_outputfile.text()+'.raw'
                ofile = open(outputfile,'w')
                
            except:
                self.change_message('Seleccione un archivo de salida válido')
                return False
#             if self.dsb_f_start.value() == self.dsb_f_stop.value():
#                 self.change_message('Corregir Sweep de Frecuencio START = END')
#                 return False
#             if self.dsb_f_start.value() > self.dsb_f_stop.value():
#                 self.change_message('Corregir Sweep de Frecuencio START > END')
#                 return False
#             if self.dsb_f_step.value() == 0 :
#                 self.change_message('Corregir Sweep de Frecuencio STEEP = 0')
#                 return False
            self.pb_start.setEnabled(False)
            self.pb_start.setText('Stop')
            da_order = self.cbx_file_display_a_order.itemData(self.cbx_file_display_a_order.currentIndex())
            db_order = self.cbx_file_display_b_order.itemData(self.cbx_file_display_b_order.currentIndex())
            self.scaner.adquire(4, outputfile, da_order, db_order)
            self.enable_ui_controls(False)
            self.pb_start.setEnabled(True)
            
        elif self.pb_start.text()=='Stop':
            self.pb_start.setEnabled(False)
            self.scaner.exiting=True
            while self.scaner.isRunning():
                self.change_message('Terminando última medicion')
            self.scaner.terminate()
            self.connect_thread()
            self.get_serial_config()
            self.enable_ui_controls(True)
            self.pb_start.setText('Start')
            self.pb_start.setEnabled(True)
            
        
    @QtCore.pyqtSlot()
    def on_tlb_output_file_released(self):
        filepath=QtGui.QFileDialog.getSaveFileName(self, 'Select Output File', os.path.expanduser('~'))
        self.le_outputfile.setText(filepath)
        
def main():
    app = QtGui.QApplication(sys.argv)
    app.processEvents()
    DAQ = HP4192AuiAPP()
    for i in range(0, 101):
        DAQ.splash.progressBar.setValue(i)
        # Do something which takes some time.
        t = time.time()
        if i == 10:
            DAQ.connect_thread()
            
        if i == 80:
            DAQ.get_serial_config()
        while time.time() < t + 0.03:
            app.processEvents()
    DAQ.show()
    DAQ.splash.finish(DAQ)
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()