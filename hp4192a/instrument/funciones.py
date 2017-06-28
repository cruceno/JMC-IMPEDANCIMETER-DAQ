'''
Created on 22 dic. 2016

@author: Marcos
'''

orders={'p':('p',10**-12),
        'n':('n',10**-9),
        'u':('u',10**-6), 
        'm':('m',10**-3),
        'base':('',1),
        'k':('k',10**3),
        'M':('M',10**6)
        }
def valor(siete_segmento):
    # print (siete_segmento)
    if siete_segmento > 128:
        siete_segmento -= 128        
    numero={63:0,
            6:1,
            91:2,
            79:3,
            102:4,
            109:5,
            125:6,
            7:7,
            127:8,
            111:9,
        }
       
    try:
        return numero[siete_segmento]
    except:
        return 0
    

def coma(siete_segmento):
    if siete_segmento > 128:
        coma = 1
    else: 
        coma = 0
    return coma

def extraer_f(cadena):
    cadena1 = bytearray(cadena)
    if cadena1[0] == 3:
        cadena1[0]=6
        f1=1
    elif cadena1[0] == 4:
        cadena1[0]=6  
        f1=-1   
    else:
        cadena1[0]=63
        f1=0
    if f1 != -1:    
        q= valor(cadena1[0])*10000000+valor(cadena1[1])*1000000+valor(cadena1[2])*100000+valor(cadena1[3])*10000+valor(cadena1[4])*1000+valor(cadena1[5])*100+valor(cadena1[6])*10+valor(cadena1[7])*1
        if coma(cadena1[0]):
            decimal = 100000000
        elif coma(cadena1[1]):
            decimal = 10000000
        elif coma(cadena1[2]):
            decimal = 1000000
        elif coma(cadena1[3]):
            decimal = 100000
        elif coma(cadena1[4]):
            decimal = 10000
        elif coma(cadena1[5]):
            decimal = 1000
        elif coma(cadena1[6]):
            decimal = 100
        elif coma(cadena1[7]):
            decimal = 10    
        else:
            decimal=1    
    
        frecuencia = q/decimal
    return frecuencia

def extraer_A(cadena):
    
    cadena1 = bytearray(cadena)
    print (len(cadena1))
    if cadena1[31] == 3:
        cadena1[31]=6
        f1=1
    elif cadena1[31] == 4:
        cadena1[31]=63  
        f1=-1
    elif cadena1[31]==7:
        cadena1[31]=6
        f1=-1   
    else:
        cadena1[31]=63
        f1=1
        
    q= valor(cadena1[31])*10000+valor(cadena1[16])*1000+valor(cadena1[17])*100+valor(cadena1[18])*10+valor(cadena1[19])*1
    if coma(cadena1[31]):
        decimal = 100000
    elif coma(cadena1[16]):
        decimal = 10000
    elif coma(cadena1[17]):
        decimal = 1000
    elif coma(cadena1[18]):
        decimal = 100
    elif coma(cadena1[19]):
        decimal = 10
    else:
        decimal=1    
    display_a = (q/decimal)*f1
    unidad = unidad_A(cadena)
    return (display_a, unidad) 

def extraer_B(cadena):
    cadena1 = bytearray(cadena)
    if cadena1[21] == 3:
        cadena1[21]=6
        f1=1
    elif cadena1[21] == 4:
        cadena1[21]=63  
        f1=-1   
    elif cadena1[21]==7:
        cadena1[21]= 6
        f1=-1
    else:
        cadena1[21]=63
        f1=1
    if f1 == 1:    
        s=1
    else:
        s=-1   
    if cadena1[22] == 0:
        cadena1[22]=63
        if cadena1[23] == 0:
            cadena1[23]=63        
    q= valor(cadena1[21])*10000+valor(cadena1[22])*1000+valor(cadena1[23])*100+valor(cadena1[24])*10+valor(cadena1[25])*1
    if coma(cadena1[21]):
        decimal = 100000
    elif coma(cadena1[22]):
        decimal = 10000
    elif coma(cadena1[23]):
        decimal = 1000
    elif coma(cadena1[24]):
        decimal = 100
    elif coma(cadena1[25]):
        decimal = 10
    else:
        decimal=1
    display_b = s*(q/decimal)
    unidad = unidad_B(cadena)
    return (display_b, unidad)        

def unidad_A(cadena):
    if cadena[28] & 0b00000001:
        unidad="S"
    elif cadena[28] & 0b00000010:
        unidad="dB"
    elif cadena[28] & 0b00000100:
        unidad="H"
    elif cadena[27] & 0b10000000:
        unidad="F"
    elif cadena[27] & 0b01000000:
        unidad="OHM"
    else:
        unidad=""
    
    if cadena[27] & 0b00000001:
        orden=orders['k']
    elif cadena[27] & 0b00000010:
        orden=orders['m']
    elif cadena[27] & 0b00000100:
        orden=orders['u']
    elif cadena[27] & 0b00001000:
        orden=orders['n']
    elif cadena[27] & 0b00010000:
        orden=orders['p']
    elif cadena[27] & 0b00100000:
        orden=orders['M']
    else:
        orden=orders['base']
    return (orden,unidad)
    
    
def unidad_B(cadena):
    if cadena[30] & 0b00000001:
        unidad="S"
    elif cadena[30] & 0b00000010:
        unidad="Q"
    elif cadena[30] & 0b00000100:
        unidad="Deg"
    elif cadena[30] & 0b00001000:
        unidad=""
    elif cadena[29] & 0b10000000:
        unidad="rad"
    elif cadena[29] & 0b01000000:
        unidad="OHM"
    elif cadena[29] & 0b00010000:
        unidad="s"
    elif cadena[29] & 0b00001000:
        unidad="D"
    else:
        unidad=""
    
    if cadena[29] & 0b00000001:
        orden = orders['k']
    elif cadena[29] & 0b00000010:
        orden = orders['m']
    elif cadena[29] & 0b00000100:
        orden = orders['u']
    else:
        orden=orders['base']
    return (orden,unidad)
    
    
    