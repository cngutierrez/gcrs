#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 22:25:56 2021

@author: christiracing
"""

"""
for posicion, yy in enumerate(vec_añ):
    print(yy)
"""    

"""
Este código lo que hace es generar archivos con los datos de GCRs para cada ICME del catálogo de Regnault
"""


import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import os
os.environ["CDF_LIB"] = "/home/christiracing/Escritorio/cdf-dist-all/cdf37_1-dist/lib"
from spacepy import pycdf
from matplotlib.backends.backend_pdf import PdfPages
from datetime import timedelta
import matplotlib.dates as mdates

filename = '/media/christiracing/Elements/Doctorado/Materias/IndicesGCRs.csv'
df_indices = pd.read_csv(filename)

filename = '/media/christiracing/Elements/Doctorado/Materias/CosmicRayData.csv'
df = pd.read_csv(filename)


#################### Abro los archivos #################### 

archivo_inicio_ejecta = open("/media/christiracing/Elements/tesis/datos/icm_inicio_rc_frances.txt","r") #Abro el archivo cuando arranca el evento
archivo_final_ejecta = open("/media/christiracing/Elements/tesis/datos/icm_final_rc_frances.txt","r") #Abro el archivo cuando finaliza el evento
archivo_disturbance = open("/media/christiracing/Elements/tesis/datos/disturbances.txt","r") #Abro el archivo con las fechas de las perturbaciones
archivo_flags = open("/media/christiracing/Elements/tesis/datos/flags.txt","r") #Abro el archivo con los flags
archivo_flags_nuevos = open("/media/christiracing/Elements/tesis/datos/flags_nuevos.txt","r")
archivo_gle = open("/media/christiracing/Elements/tesis/datos/GLE_indexs.txt","r")
archivo_lento = open("/media/christiracing/Elements/tesis/datos/indices_lento.txt","r")
archivo_medio = open("/media/christiracing/Elements/tesis/datos/indices_medio.txt","r")
archivo_rapido = open("/media/christiracing/Elements/tesis/datos/indices_rapido.txt","r")

####################  Defino las variables a utilizar #################### 
FDSS = []

event_index = []
event_no_sheat = []
event_mc = []
event_quality = []
event_Bmax = []
event_Bmean1 = []
event_Bmean2 = []
event_Bmeant = []
event_Vmax = []
event_Vmean1 = []
event_Vmean2 = []
event_Vmeant = []
event_Npmax = []
event_Npmean1 = []
event_Npmean2 = []
event_Npmeant = []
event_Tpmax = []
event_Tpmean1 = []
event_Tpmean2 = []
event_Tpmeant = []
event_max_decrease = []
event_pre_icme = []
event_post_icme = []
event_gle = []
event_status = []
event_considerated = []
event_type = []
event_step = []
event_min_location = []

text_inicio_ejecta = [] 
text_final_ejecta = [] 
text_disturbance = [] 
text_flags = []
text_flags_nuevos = [] 
text_gle = []
lento = [] 
medio = []
rapido = []
año_inicio_ejecta = [] 
mes_inicio_ejecta = [] 
dia_inicio_ejecta = [] 
hora_inicio_ejecta = []
minuto_inicio_ejecta = []
año_final_ejecta = [] 
mes_final_ejecta = [] 
dia_final_ejecta = [] 
hora_final_ejecta = [] 
minuto_final_ejecta = [] 
evento_inicio_ejecta = [] 
evento_final_ejecta = [] 
fecha_inicio_ejecta = [] 
fecha_final_ejecta = [] 
fecha_disturbance = []
ubicacion_swepam = [] 
ubicacion_mag = []  
disturbance = [] 
año_disturbance = []
mes_disturbance = [] 
dia_disturbance = [] 
hora_disturbance = [] 
minuto_disturbance = [] 
flags = []
flags_nuevos = [] 
no_sheat = [] 
mc = [] 
quality = [] 
gle = []
status = []
considerated = []
fd_type = []
step = []
min_location = []

for line in archivo_inicio_ejecta.readlines(): #recorro todas las lineas del txt
    text_inicio_ejecta.append(line) #a es una lista que tiene todas las lineas del archivo eventos (la fecha del inicio del evento)
    
for line in archivo_final_ejecta.readlines(): #recorro todas las lineas del txt
    text_final_ejecta.append(line) #b es una lista que tiene todas las lineas del archivo eventosf (la fecha del final del evento)

for line in archivo_disturbance.readlines(): #recorro todas las lineas del txt
    text_disturbance.append(line) #c es una lista que tiene todas las lineas del archivo eventosd (la fecha del final del evento)

for line in archivo_flags.readlines(): #recorro todas las lineas del txt
    text_flags.append(line) #d es una lista que tiene todas las lineas del archivo eventosf (la fecha del final del evento)

for line in archivo_flags_nuevos.readlines(): #recorro todas las lineas del txt
    text_flags_nuevos.append(line) #d es una lista que tiene todas las lineas del archivo eventosf (la fecha del final del evento)

for line in archivo_gle.readlines(): #recorro todas las lineas del txt
    text_gle.append(line) #d es una lista que tiene todas las lineas del archivo eventosf (la fecha del final del evento)

for line in archivo_lento.readlines(): #recorro todas las lineas del txt
    lento.append(line) #d es una lista que tiene todas las lineas del archivo eventosf (la fecha del final del evento)

for line in archivo_medio.readlines(): #recorro todas las lineas del txt
    medio.append(line) #d es una lista que tiene todas las lineas del archivo eventosf (la fecha del final del evento)

for line in archivo_rapido.readlines(): #recorro todas las lineas del txt
    rapido.append(line) #d es una lista que tiene todas las lineas del archivo eventosf (la fecha del final del evento)

for i in range(0,len(text_inicio_ejecta)):
    evento_inicio_ejecta = text_inicio_ejecta[i] #me voy quedando con cada linea de a
    evento_final_ejecta = text_final_ejecta[i] #me voy quedando con cada linea de b
    disturbance = text_disturbance[i]
    flags = text_flags[i]
    flags_nuevos = text_flags_nuevos[i]
    año_inicio_ejecta.append(evento_inicio_ejecta[0:4]) #me quedo con los primeras 4 caracteres de a que corresponden al año de inicio del evento
    mes_inicio_ejecta.append(evento_inicio_ejecta[5:7]) #me quedo con los caracteres de a que corresponden al mes del inicio del evento
    dia_inicio_ejecta.append(evento_inicio_ejecta[8:10]) #me quedo con los caracteres de a que corresponden al dia inicial del evento
    hora_inicio_ejecta.append(evento_inicio_ejecta[11:13]) #me quedo con los caracteres de a que corresponden a la hora inicial del evento
    minuto_inicio_ejecta.append(evento_inicio_ejecta[14:16]) #me quedo con los caracteres de a que corresponden al minuto inicial del evento
    año_final_ejecta.append(evento_final_ejecta[0:4]) #me quedo con los caracteres de b que corresponden al año del final del evento
    mes_final_ejecta.append(evento_final_ejecta[5:7]) #me quedo con los caracteres de b que corresponden al mes del final del evento
    dia_final_ejecta.append(evento_final_ejecta[8:10]) #me quedo con los caracteres de b que corresponden al día final del evento
    hora_final_ejecta.append(evento_final_ejecta[11:13]) #me quedo con los caracteres de b que corresponden a la hora final del evento
    minuto_final_ejecta.append(evento_final_ejecta[14:16]) #me quedo con los caracteres de b que corresponden al minuto final del evento    
    año_disturbance.append(disturbance[0:4]) #me quedo con los primeras 4 caracteres de a que corresponden al año de inicio del evento
    mes_disturbance.append(disturbance[5:7]) #me quedo con los caracteres de a que corresponden al mes del inicio del evento
    dia_disturbance.append(disturbance[8:10]) #me quedo con los caracteres de a que corresponden al dia inicial del evento
    hora_disturbance.append(disturbance[11:13]) #me quedo con los caracteres de a que corresponden a la hora inicial del evento
    minuto_disturbance.append(disturbance[14:16]) #me quedo con los caracteres de a que corresponden al minuto inicial del evento
    fecha_inicio_ejecta.append(año_inicio_ejecta[i]+mes_inicio_ejecta[i]+dia_inicio_ejecta[i]) #Genero la fecha inicial del evento en el formato del archivo CDF
    fecha_final_ejecta.append(año_final_ejecta[i]+mes_final_ejecta[i]+dia_final_ejecta[i]) #Genero la fecha final del evento en el formato del archivo CDF
    fecha_disturbance.append(año_disturbance[i]+mes_disturbance[i]+dia_disturbance[i]) #Genero la fecha final del evento en el formato del archivo CDF
    no_sheat.append(flags[0:1])
    mc.append(flags[2:3])
    quality.append(flags[4:5])
    status.append(flags_nuevos[0:1])
    considerated.append(flags_nuevos[2:3])
    fd_type.append(flags_nuevos[4:5])
    step.append(flags_nuevos[6:7])
    min_location.append(flags_nuevos[8:9])
    gle.append(text_gle[i])
    ubicacion_swepam.append('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+fecha_disturbance[i]+'_v06.cdf') #Genero todos los paths con los archivos a abrir para los inicios de los eventos.
    ubicacion_mag.append('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+fecha_disturbance[i]+'_v04.cdf') #Genero todos los paths con los archivos a abrir para los inicios de los eventos.    

#################### Genero los índices correspondientes a los eventos "rápidos", "medios" y "lentos" ####################
    
indice_lento = []
indice_medio = []
indice_rapido = []

for i in range(0,len(lento)):
    indice_lento.append(int(lento[i]))
for i in range(0,len(medio)):
    indice_medio.append(int(medio[i]))
for i in range(0,len(rapido)-1):
    indice_rapido.append(int(rapido[i]))
    
archivo_inicio_ejecta.close()
archivo_final_ejecta.close()
archivo_disturbance.close()
archivo_flags.close()
archivo_flags_nuevos.close()
archivo_lento.close()
archivo_medio.close()
archivo_rapido.close()

indice_lento1 = []
indice_lento2 = []
indice_lento3 = []

for i in range(0,len(indice_lento)):
    if i < 91:
        indice_lento1.append(indice_lento[i])
    elif i > 181:
        indice_lento3.append(indice_lento[i])
    else:
        indice_lento2.append(indice_lento[i])

###############################################################################

#prueba = []
#
#for i in range(87,len(indice_lento1)):
#    prueba.append(indice_lento3[i])

###############################################################################

indice_medio1 = []
indice_medio2 = []
        
for i in range(0,len(indice_medio)):
    if i < 71:
        indice_medio1.append(indice_medio[i])
    else:
        indice_medio2.append(indice_medio[i])

###############################################################################

#prueba = []

#for i in range(50,len(indice_medio1)):
#    prueba.append(indice_medio1[i])

###############################################################################
index = [] #Creo el vector indice

for z in range(17,25): #Esto es bastante cabeza, pero como faltaba el evento 25 en el catálogo se separo así (para no abrir otro archivo)
    index.append(z)

for z in range(26,499):
    index.append(z)

indice_lento3 = np.delete(indice_lento3, 18)    
#################### ####################
    
fecha_disturbance_float = np.zeros([len(text_inicio_ejecta),1]) #Creo vector vacío
fecha_final_ejecta_float = np.zeros([len(text_inicio_ejecta),1]) #Creo vector vacío
dif_fec = np.zeros([len(text_inicio_ejecta),1]) #Creo vector vacío
dif_fecha = np.zeros([len(text_inicio_ejecta),1]) #Creo vector vacío

año_disturbance_float = np.zeros([len(text_inicio_ejecta),1]) #Creo vector vacío
mes_disturbance_float = np.zeros([len(text_inicio_ejecta),1]) #Creo vector vacío
dia_disturbance_float = np.zeros([len(text_inicio_ejecta),1]) #Creo vector vacío
hora_disturbance_float = np.zeros([len(text_inicio_ejecta),1]) #Creo vector vacío
minuto_disturbance_float = np.zeros([len(text_inicio_ejecta),1]) #Creo vector vacío
año_final_ejecta_float = np.zeros([len(text_inicio_ejecta),1]) #Creo vector vacío
mes_final_ejecta_float = np.zeros([len(text_inicio_ejecta),1]) #Creo vector vacío
dia_final_ejecta_float = np.zeros([len(text_inicio_ejecta),1]) #Creo vector vacío
hora_final_ejecta_float = np.zeros([len(text_inicio_ejecta),1]) #Creo vector vacío
minuto_final_ejecta_float = np.zeros([len(text_inicio_ejecta),1]) #Creo vector vacío

for i in range(0,len(text_inicio_ejecta)): #En este for se convierten todos los strings anteriores a floats para poder operar.
    fecha_disturbance_float[i] = float(fecha_disturbance[i])
    fecha_final_ejecta_float[i] = float(fecha_final_ejecta[i])
    dif_fec[i] = fecha_final_ejecta_float[i] - fecha_disturbance_float[i]
    
    dia_disturbance_float[i] = float(dia_disturbance[i])
    mes_disturbance_float[i] = float(mes_disturbance[i])
    año_disturbance_float[i] = float(año_disturbance[i])
    dia_final_ejecta_float[i] = float(dia_final_ejecta[i])
    mes_final_ejecta_float[i] = float(mes_final_ejecta[i])
    año_final_ejecta_float[i] = float(año_final_ejecta[i])
    
    hora_disturbance_float[i] = float(hora_disturbance[i])
    hora_final_ejecta_float[i] = float(hora_final_ejecta[i])
    minuto_disturbance_float[i] = float(minuto_disturbance[i])
    minuto_final_ejecta_float[i] = float(minuto_final_ejecta[i])        

############ CONVIERTO TODAS LAS VARIABLES A FLOAT ############

vr_año =[] #Genero la "lista" vacia
vr_mes = [] #Genero la "lista" vacia
vr_dia = [] #Genero la "lista" vacia
vr_hora = [] #Genero la "lista" vacia

eventos = []

for i in range(15, 473):
    eventos.append(i)
    
eventos = np.delete(eventos, 351)

############ Gráfico ############

with PdfPages('/home/christiracing/Desktop') as pp: #27 30 36 45Módulo de Python para generar distintas páginas en un único PDF
    for i in range(15,473): #TERMINA EN 473 ESTA ES LA LINEA CLAVE DEL CÓDIGO YA QUE CAMBIANDO EL RANGE VARIO LA CANTIDAD DE EVENTOS A PLOTEAR, arranca del 15 y termina algunos eventos antes debido a que los archivos que contienen la velocidad del viento solar y la densidad de particulas arrancan desde el evento 6 y terminan antes.
#    for i in list(indice_lento3):
#    for i in list(eventos): #ESTE ES PARA HACER LA TABLA          
        disturbance_datetime = datetime.datetime(int(año_disturbance_float[i]) , int(mes_disturbance_float[i]), int(dia_disturbance_float[i]), int(hora_disturbance_float[i]), int(minuto_disturbance_float[i])) #Calculo la fecha inicial del evento i en formato datetime para poder opera
        inicio_ejecta_datetime = datetime.datetime(int(año_inicio_ejecta[i]) , int(mes_inicio_ejecta[i]), int(dia_inicio_ejecta[i]), int(hora_inicio_ejecta[i]), int(minuto_inicio_ejecta[i])) #Calculo la fecha inicial del evento i en formato datetime para poder operar
        final_ejecta_datetime = datetime.datetime(int(año_final_ejecta_float[i]) , int(mes_final_ejecta_float[i]), int(dia_final_ejecta_float[i]), int(hora_final_ejecta_float[i]), int(minuto_final_ejecta_float[i])) #Calculo la fecha final del evento i en formato datetime para poder operar
        delta_t = final_ejecta_datetime - disturbance_datetime #Calculo el delta tiempo del evento, es decir el intervalo a graficar
        contador = int(delta_t.total_seconds()/(60*24*60)) + 1
        
        inicio_dominio = disturbance_datetime - delta_t
        final_dominio = final_ejecta_datetime + delta_t
            
        for j in range(np.shape(df_indices)[0]):
            if inicio_dominio.year == df_indices.año[j] and inicio_dominio.month == df_indices.mes[j]:
                indice_inicio = df_indices.indice[j - 1]
            if final_dominio.year == df_indices.año[j] and final_dominio.month == df_indices.mes[j]:    
                indice_final = df_indices.indice[j + 1]
        
        gcr = []
        fecha_gcr = []        

        for j in range(indice_inicio, indice_final):
            if inicio_dominio <= datetime.datetime(df.año[j], df.mes[j], df.dia[j], df.hora[j],df.minuto[j], df.segundo[j]) and final_dominio >= datetime.datetime(df.año[j], df.mes[j], df.dia[j],df.hora[j], df.minuto[j], df.segundo[j]):
                gcr.append(df.relative_count[j])
                fecha_gcr.append(datetime.datetime(df.año[j], df.mes[j], df.dia[j], df.hora[j] ,df.minuto[j], df.segundo[j]))
                
        df_icme = pd.DataFrame({'fecha': fecha_gcr,
        'gcrs': gcr,
        })

        df_icme.to_csv("/media/christiracing/Elements/Doctorado/gcrs_icme/icme" + str(i) + ".csv", index= False) # Guardo el archivo sin los índices