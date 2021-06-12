#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 02:06:47 2020

@author: christian
"""

"""
Este código me genera .csv con los datos de B, Vx, Np y Tpr para todos los eventos ICME según el catálogo de Regnault
"""

import csv
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

    if (año_disturbance_float[i] == año_final_ejecta_float[i] and mes_disturbance_float[i] == mes_final_ejecta_float[i] and dia_disturbance_float[i] != dia_final_ejecta_float[i]): #En esta cadena de if se genera el vector "dif fecha" que se va a utilizar para ver la duración del evento y por lo tanto el intervalo de tiempo necesario para gráficar las variables
        dif_fecha[i] = dia_final_ejecta_float[i] - dia_disturbance_float[i]
    elif (año_disturbance_float[i] == año_final_ejecta_float[i] and mes_disturbance_float[i] != mes_final_ejecta_float[i]):
        if (mes_disturbance_float[i] == 1 or mes_disturbance_float[i] == 3 or mes_disturbance_float[i] == 5 or mes_disturbance_float[i] == 7 or mes_disturbance_float[i] == 8 or mes_disturbance_float[i] == 10 or mes_disturbance_float[i] == 12):
            dif_fecha[i] = 31 - dia_disturbance_float[i] + dia_final_ejecta_float[i]
        elif (mes_disturbance_float[i] == 4 or mes_disturbance_float[i] == 6 or mes_disturbance_float[i] == 9 or mes_disturbance_float[i] == 11):
            dif_fecha[i] = 30 - dia_disturbance_float[i] + dia_final_ejecta_float[i]
        else:
            dif_fecha[i] = 28 - dia_disturbance_float[i] + dia_final_ejecta_float[i]
    elif (año_disturbance_float[i] == año_final_ejecta_float[i] and mes_disturbance_float[i] == mes_final_ejecta_float[i] and dia_disturbance_float[i] == dia_final_ejecta_float[i]):
        dif_fecha[i] = 0
    else:
        dif_fecha[i] = 31 - dia_disturbance_float[i] + dia_final_ejecta_float[i]
            
eventos = []

for i in range(15, 473):
    eventos.append(i)
    
eventos = np.delete(eventos, 351)

############ Gráfico ############

with PdfPages('/home/christiracing/Desktop') as pp: #27 30 36 45Módulo de Python para generar distintas páginas en un único PDF
#    for i in range(15,17): #TERMINA EN 473 ESTA ES LA LINEA CLAVE DEL CÓDIGO YA QUE CAMBIANDO EL RANGE VARIO LA CANTIDAD DE EVENTOS A PLOTEAR, arranca del 15 y termina algunos eventos antes debido a que los archivos que contienen la velocidad del viento solar y la densidad de particulas arrancan desde el evento 6 y terminan antes.
#    for i in list(indice_lento3):
    for i in list(eventos): #ESTE ES PARA HACER LA TABLA          
        disturbance_datetime = datetime.datetime(int(año_disturbance_float[i]) , int(mes_disturbance_float[i]), int(dia_disturbance_float[i]), int(hora_disturbance_float[i]), int(minuto_disturbance_float[i])) #Calculo la fecha inicial del evento i en formato datetime para poder opera
        inicio_ejecta_datetime = datetime.datetime(int(año_inicio_ejecta[i]) , int(mes_inicio_ejecta[i]), int(dia_inicio_ejecta[i]), int(hora_inicio_ejecta[i]), int(minuto_inicio_ejecta[i])) #Calculo la fecha inicial del evento i en formato datetime para poder operar
        final_ejecta_datetime = datetime.datetime(int(año_final_ejecta_float[i]) , int(mes_final_ejecta_float[i]), int(dia_final_ejecta_float[i]), int(hora_final_ejecta_float[i]), int(minuto_final_ejecta_float[i])) #Calculo la fecha final del evento i en formato datetime para poder operar
        delta_t = final_ejecta_datetime - disturbance_datetime #Calculo el delta tiempo del evento, es decir el intervalo a graficar
        contador = int(delta_t.total_seconds()/(60*24*60)) + 1
        
        inicio_dominio = disturbance_datetime - delta_t
        final_dominio = final_ejecta_datetime + delta_t
        
        dia_inicio_dominio = inicio_dominio.day
        hora_inicio_dominio = inicio_dominio.hour
        dia_final_dominio = final_dominio.day
        hora_final_dominio = final_dominio.hour
        dia_disturbance_datetime = disturbance_datetime.day
        hora_disturbance_datetime = disturbance_datetime.hour
        
        vr_año =[] #Genero la "lista" vacia
        vr_mes = [] #Genero la "lista" vacia
        vr_dia = [] #Genero la "lista" vacia
        vr_hora = [] #Genero la "lista" vacia
        
#TODOS LOS IF QUE SIGUEN SON PARA CALCULAR LOS DIAS ANTERIORES Y POSTERIORES NECESARIOS PARA PLOTEAR LOS EVENTOS

        if dia_disturbance_float[i] - contador >= 10 and (mes_disturbance_float[i] == 1 or mes_disturbance_float[i] == 2 or mes_disturbance_float[i] == 3 or mes_disturbance_float[i] == 4 or mes_disturbance_float[i] == 5 or mes_disturbance_float[i] == 6 or mes_disturbance_float[i] == 7 or mes_disturbance_float[i] == 8 or mes_disturbance_float[i] == 9):
            cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]))+str(int(dia_disturbance_float[i] - contador))+'_v04.cdf')
            cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]))+str(int(dia_disturbance_float[i] - contador))+'_v06.cdf')
            for x in range(0,24):
                vr_hora.append(x)
                vr_año.append(año_disturbance_float[i])
                vr_mes.append(mes_disturbance_float[i])
                vr_dia.append(dia_disturbance_float[i] - contador)
        elif dia_disturbance_float[i] - contador >= 10 and (mes_disturbance_float[i] == 10 or mes_disturbance_float[i] == 11 or mes_disturbance_float[i] == 12):
            cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]))+str(int(dia_disturbance_float[i] - contador))+'_v04.cdf')
            cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]))+str(int(dia_disturbance_float[i] - contador))+'_v06.cdf')
            for x in range(0,24):
                vr_hora.append(x)
                vr_año.append(año_disturbance_float[i])
                vr_mes.append(mes_disturbance_float[i])
                vr_dia.append(dia_disturbance_float[i] - contador)
        elif dia_disturbance_float[i] - contador < 10 and dia_disturbance_float[i] - contador >= 1 and (mes_disturbance_float[i] == 1 or mes_disturbance_float[i] == 2 or mes_disturbance_float[i] == 3 or mes_disturbance_float[i] == 4 or mes_disturbance_float[i] == 5 or mes_disturbance_float[i] == 6 or mes_disturbance_float[i] == 7 or mes_disturbance_float[i] == 8 or mes_disturbance_float[i] == 9):
            cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]))+'0'+str(int(dia_disturbance_float[i] - contador))+'_v04.cdf')
            cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]))+'0'+str(int(dia_disturbance_float[i] - contador))+'_v06.cdf')
            for x in range(0,24):
                vr_hora.append(x)
                vr_año.append(año_disturbance_float[i])
                vr_mes.append(mes_disturbance_float[i])
                vr_dia.append(dia_disturbance_float[i] - contador)
        elif dia_disturbance_float[i] - contador < 10 and dia_disturbance_float[i] - contador >= 1 and (mes_disturbance_float[i] == 10 or mes_disturbance_float[i] == 11 or mes_disturbance_float[i] == 12):
            cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]))+'0'+str(int(dia_disturbance_float[i] - contador))+'_v04.cdf')
            cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]))+'0'+str(int(dia_disturbance_float[i] - contador))+'_v06.cdf')
            for x in range(0,24):
                vr_hora.append(x)
                vr_año.append(año_disturbance_float[i])
                vr_mes.append(mes_disturbance_float[i])
                vr_dia.append(dia_disturbance_float[i] - contador)
        elif dia_disturbance_float[i] - contador < 1 and (mes_disturbance_float[i] == 2 or mes_disturbance_float[i] == 4 or mes_disturbance_float[i] == 6 or mes_disturbance_float[i] == 8 or mes_disturbance_float[i] == 9):
            cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] - contador + 31))+'_v04.cdf')
            cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] - contador + 31))+'_v06.cdf')
            for x in range(0,24):
                vr_hora.append(x)
                vr_año.append(año_disturbance_float[i])
                vr_mes.append(mes_disturbance_float[i] - 1)
                vr_dia.append(dia_disturbance_float[i] - contador + 31)
        elif dia_disturbance_float[i] - contador < 1 and (mes_disturbance_float[i] == 5 or mes_disturbance_float[i] == 7 or mes_disturbance_float[i] == 10):
            cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] - contador + 30))+'_v04.cdf')
            cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] - contador + 30))+'_v06.cdf')
            for x in range(0,24):
                vr_hora.append(x)
                vr_año.append(año_disturbance_float[i])
                vr_mes.append(mes_disturbance_float[i] - 1)
                vr_dia.append(dia_disturbance_float[i] - contador + 30)
        elif dia_disturbance_float[i] - contador < 1 and mes_disturbance_float[i] == 11:
            cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] - contador + 31))+'_v04.cdf')
            cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] - contador + 31))+'_v06.cdf')
            for x in range(0,24):
                vr_hora.append(x)
                vr_año.append(año_disturbance_float[i])
                vr_mes.append(mes_disturbance_float[i] - 1)
                vr_dia.append(dia_disturbance_float[i] - contador + 31)
        elif dia_disturbance_float[i] - contador < 1 and mes_disturbance_float[i] == 12:
            cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] - contador + 30))+'_v04.cdf')
            cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] - contador + 30))+'_v06.cdf')
            for x in range(0,24):
                vr_hora.append(x)
                vr_año.append(año_disturbance_float[i])
                vr_mes.append(mes_disturbance_float[i] - 1)
                vr_dia.append(dia_disturbance_float[i] - contador + 30)
        elif dia_disturbance_float[i] - contador < 1 and mes_disturbance_float[i] == 3 and np.remainder(año_disturbance_float[i],4) != 0:
            cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] - contador + 28))+'_v04.cdf')
            cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] - contador + 28))+'_v06.cdf')
            for x in range(0,24):
                vr_hora.append(x)
                vr_año.append(año_disturbance_float[i])
                vr_mes.append(mes_disturbance_float[i] - 1)
                vr_dia.append(dia_disturbance_float[i] - contador + 28)
        elif dia_disturbance_float[i] - contador < 1 and mes_disturbance_float[i] == 3 and np.remainder(año_disturbance_float[i],4) == 0:
            cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] - contador + 29))+'_v04.cdf')
            cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] - contador + 29))+'_v06.cdf')
            for x in range(0,24):
                vr_hora.append(x)
                vr_año.append(año_disturbance_float[i])
                vr_mes.append(mes_disturbance_float[i] - 1)
                vr_dia.append(dia_disturbance_float[i] - contador + 29)
        elif dia_disturbance_float[i] - contador < 1 and mes_disturbance_float[i] == 1:
            cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]-1))+'12'+str(int(dia_disturbance_float[i] - contador + 31))+'_v04.cdf')
            cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]-1))+'12'+str(int(dia_disturbance_float[i] - contador + 31))+'_v06.cdf')
            for x in range(0,24):
                vr_hora.append(x)
                vr_año.append(año_disturbance_float[i] - 1)
                vr_mes.append(12)
                vr_dia.append(dia_disturbance_float[i] - contador + 31)
                             
        tv = cdf1['Epoch'][:] #En la primer iteración del for creo la matriz, luego en los siguientes se concatenará a esta matriz los datos correspondientes a los siguientes días.
        Vx = cdf1['V_GSE'][:,0] #En la primer iteración del for creo la matriz, luego en los siguientes se concatenará a esta matriz los datos correspondientes a los siguientes días
        Np = cdf1['Np'][:] #En la primer iteración del for creo la matriz, luego en los siguientes se concatenará a esta matriz los datos correspondientes a los siguientes días
        t = cdf['Epoch'][:] #En la primer iteración del for creo la matriz, luego en los siguientes se concatenará a esta matriz los datos correspondientes a los siguientes días
        Bx = cdf['BGSEc'][:,0] #En la primer iteración del for creo la matriz, luego en los siguientes se concatenará a esta matriz los datos correspondientes a los siguientes días
        By = cdf['BGSEc'][:,1] #En la primer iteración del for creo la matriz, luego en los siguientes se concatenará a esta matriz los datos correspondientes a los siguientes días
        Bz = cdf['BGSEc'][:,2] #En la primer iteración del for creo la matriz, luego en los siguientes se concatenará a esta matriz los datos correspondientes a los siguientes días
        Tpr = cdf1['Tpr'][:]
        
        for j in range(-contador + 1,contador+int(dif_fecha[i]+1)):
            if j < 0:
                if dia_disturbance_float[i] + j >= 10 and (mes_disturbance_float[i] == 1 or mes_disturbance_float[i] == 2 or mes_disturbance_float[i] == 3 or mes_disturbance_float[i] == 4 or mes_disturbance_float[i] == 5 or mes_disturbance_float[i] == 6 or mes_disturbance_float[i] == 7 or mes_disturbance_float[i] == 8 or mes_disturbance_float[i] == 9):
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]))+str(int(dia_disturbance_float[i] + j))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]))+str(int(dia_disturbance_float[i] + j))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_disturbance_float[i])
                        vr_mes.append(mes_disturbance_float[i])
                        vr_dia.append(dia_disturbance_float[i] + j)
                elif dia_disturbance_float[i] + j >= 10 and (mes_disturbance_float[i] == 10 or mes_disturbance_float[i] == 11 or mes_disturbance_float[i] == 12):
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]))+str(int(dia_disturbance_float[i] + j))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]))+str(int(dia_disturbance_float[i] + j))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_disturbance_float[i])
                        vr_mes.append(mes_disturbance_float[i])
                        vr_dia.append(dia_disturbance_float[i] + j)
                elif dia_disturbance_float[i] + j < 10 and dia_disturbance_float[i] + j >= 1 and (mes_disturbance_float[i] == 1 or mes_disturbance_float[i] == 2 or mes_disturbance_float[i] == 3 or mes_disturbance_float[i] == 4 or mes_disturbance_float[i] == 5 or mes_disturbance_float[i] == 6 or mes_disturbance_float[i] == 7 or mes_disturbance_float[i] == 8 or mes_disturbance_float[i] == 9):
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]))+'0'+str(int(dia_disturbance_float[i] + j))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]))+'0'+str(int(dia_disturbance_float[i] + j))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_disturbance_float[i])
                        vr_mes.append(mes_disturbance_float[i])
                        vr_dia.append(dia_disturbance_float[i] + j)
                elif dia_disturbance_float[i] + j < 10 and dia_disturbance_float[i] + j >= 1 and (mes_disturbance_float[i] == 10 or mes_disturbance_float[i] == 11 or mes_disturbance_float[i] == 12):
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]))+'0'+str(int(dia_disturbance_float[i] + j))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]))+'0'+str(int(dia_disturbance_float[i] + j))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_disturbance_float[i])
                        vr_mes.append(mes_disturbance_float[i])
                        vr_dia.append(dia_disturbance_float[i] + j)
                elif dia_disturbance_float[i] + j < 1 and (mes_disturbance_float[i] == 2 or mes_disturbance_float[i] == 4 or mes_disturbance_float[i] == 6 or mes_disturbance_float[i] == 8 or mes_disturbance_float[i] == 9):
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] + j + 31))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] + j + 31))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_disturbance_float[i])
                        vr_mes.append(mes_disturbance_float[i] - 1)
                        vr_dia.append(dia_disturbance_float[i] + j + 31)
                elif dia_disturbance_float[i] + j < 1 and (mes_disturbance_float[i] == 5 or mes_disturbance_float[i] == 7 or mes_disturbance_float[i] == 10):
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] + j + 30))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] + j + 30))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_disturbance_float[i])
                        vr_mes.append(mes_disturbance_float[i] - 1)
                        vr_dia.append(dia_disturbance_float[i] + j + 30)
                elif dia_disturbance_float[i] + j < 1 and mes_disturbance_float[i] == 11:
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] + j + 31))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] + j + 31))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_disturbance_float[i])
                        vr_mes.append(mes_disturbance_float[i] - 1)
                        vr_dia.append(dia_disturbance_float[i] + j + 31)
                elif dia_disturbance_float[i] + j < 1 and mes_disturbance_float[i] == 12:
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] + j + 30))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] + j + 30))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_disturbance_float[i])
                        vr_mes.append(mes_disturbance_float[i] - 1)
                        vr_dia.append(dia_disturbance_float[i] + j + 30)
                elif dia_disturbance_float[i] + j < 1 and mes_disturbance_float[i] == 3 and np.remainder(año_disturbance_float[i],4) != 0:
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] + j + 28))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] + j + 28))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_disturbance_float[i])
                        vr_mes.append(mes_disturbance_float[i] - 1)
                        vr_dia.append(dia_disturbance_float[i] + j + 28)
                elif dia_disturbance_float[i] + j < 1 and mes_disturbance_float[i] == 3 and np.remainder(año_disturbance_float[i],4) == 0:
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] + j + 29))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]-1))+str(int(dia_disturbance_float[i] + j + 29))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_disturbance_float[i])
                        vr_mes.append(mes_disturbance_float[i] - 1)
                        vr_dia.append(dia_disturbance_float[i] + j + 29)
                elif dia_disturbance_float[i] + j < 1 and mes_disturbance_float[i] == 1:
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]-1))+'12'+str(int(dia_disturbance_float[i] + j + 31))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]-1))+'12'+str(int(dia_disturbance_float[i] + j + 31))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_disturbance_float[i] - 1)
                        vr_mes.append(12)
                        vr_dia.append(dia_disturbance_float[i] + j + 31)

                tv = np.concatenate((tv,cdf1['Epoch'][:]),0)
                Vx = np.concatenate((Vx,cdf1['V_GSE'][:,0]),0)
                Np = np.concatenate((Np,cdf1['Np'][:]),0)
                t = np.concatenate((t,cdf['Epoch'][:]),0)
                Bx = np.concatenate((Bx,cdf['BGSEc'][:,0]),0)
                By = np.concatenate((By,cdf['BGSEc'][:,1]),0) 
                Bz = np.concatenate((Bz,cdf['BGSEc'][:,2]),0)
                Tpr = np.concatenate((Tpr,cdf1['Tpr'][:]),0)

            elif j == 0:
                
                cdf = pycdf.CDF(ubicacion_mag[i])
                cdf1 = pycdf.CDF(ubicacion_swepam[i])
                tv = np.concatenate((tv,cdf1['Epoch'][:]),0)
                Vx = np.concatenate((Vx,cdf1['V_GSE'][:,0]),0)
                Np = np.concatenate((Np,cdf1['Np'][:]),0)
                t = np.concatenate((t,cdf['Epoch'][:]),0)
                Bx = np.concatenate((Bx,cdf['BGSEc'][:,0]),0)
                By = np.concatenate((By,cdf['BGSEc'][:,1]),0) 
                Bz = np.concatenate((Bz,cdf['BGSEc'][:,2]),0)
                Tpr = np.concatenate((Tpr,cdf1['Tpr'][:]),0)
                
                for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_disturbance_float[i])
                        vr_mes.append(mes_disturbance_float[i])
                        vr_dia.append(dia_disturbance_float[i])

            else:
                if dia_disturbance_float[i] + j == 32 and (mes_disturbance_float[i] == 1 or mes_disturbance_float[i] == 3 or mes_disturbance_float[i] == 5 or mes_disturbance_float[i] == 7 or mes_disturbance_float[i] == 8):
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]+1))+'01'+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]+1))+'01'+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_disturbance_float[i])
                        vr_mes.append(mes_disturbance_float[i] + 1)
                        vr_dia.append(1)
                elif dia_disturbance_float[i] + j == 31 and (mes_disturbance_float[i] == 4 or mes_disturbance_float[i] == 6):
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]+1))+'01'+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]+1))+'01'+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_disturbance_float[i])
                        vr_mes.append(mes_disturbance_float[i] + 1)
                        vr_dia.append(1)
                elif dia_disturbance_float[i] + j == 32 and mes_disturbance_float[i] == 10:
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]+1))+'01'+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]+1))+'01'+'_v06.cdf')                
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_disturbance_float[i])
                        vr_mes.append(mes_disturbance_float[i] + 1)
                        vr_dia.append(1)
                elif dia_disturbance_float[i] + j == 31 and (mes_disturbance_float[i] == 9 or mes_disturbance_float[i] == 11):
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]+1))+'01'+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]+1))+'01'+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_disturbance_float[i])
                        vr_mes.append(mes_disturbance_float[i] + 1)
                        vr_dia.append(1)
                elif dia_disturbance_float[i] + j == 32 and mes_disturbance_float[i] == 12:
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i])+1)+'0101'+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i])+1)+'0101'+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_disturbance_float[i] + 1)
                        vr_mes.append(1)
                        vr_dia.append(1)
                elif dia_disturbance_float[i] + j == 29 and mes_disturbance_float[i] == 2 and np.remainder(año_disturbance_float[i],4) != 0:
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'0301'+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'0301'+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_disturbance_float[i])
                        vr_mes.append(3)
                        vr_dia.append(1)
                elif dia_disturbance_float[i] + j == 30 and mes_disturbance_float[i] == 2 and np.remainder(año_disturbance_float[i],4) == 0:
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'0301'+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'0301'+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_disturbance_float[i])
                        vr_mes.append(3)
                        vr_dia.append(1)
                elif dia_disturbance_float[i] + j < 10 and (mes_disturbance_float[i] == 1 or mes_disturbance_float[i] == 3 or mes_disturbance_float[i] == 5 or mes_disturbance_float[i] == 7 or mes_disturbance_float[i] == 8):
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]))+'0'+str(int(dia_disturbance_float[i]+j))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]))+'0'+str(int(dia_disturbance_float[i]+j))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_disturbance_float[i])
                        vr_mes.append(mes_disturbance_float[i])
                        vr_dia.append(dia_disturbance_float[i]+j)
                elif dia_disturbance_float[i] + j < 32 and dia_disturbance_float[i] + j >= 10 and (mes_disturbance_float[i] == 1 or mes_disturbance_float[i] == 3 or mes_disturbance_float[i] == 5 or mes_disturbance_float[i] == 7 or mes_disturbance_float[i] == 8):
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]))+str(int(dia_disturbance_float[i]+j))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]))+str(int(dia_disturbance_float[i]+j))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_disturbance_float[i])
                        vr_mes.append(mes_disturbance_float[i])
                        vr_dia.append(dia_disturbance_float[i]+j)
                elif dia_disturbance_float[i] + j < 31 and (mes_disturbance_float[i] == 4 or mes_disturbance_float[i] == 6 or mes_disturbance_float[i] == 9):
                    if dia_disturbance_float[i] + j < 10:
                        cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]))+'0'+str(int(dia_disturbance_float[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]))+'0'+str(int(dia_disturbance_float[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_disturbance_float[i])
                            vr_mes.append(mes_disturbance_float[i])
                            vr_dia.append(dia_disturbance_float[i]+j)
                    elif dia_disturbance_float[i] + j >= 10:
                        cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]))+str(int(dia_disturbance_float[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]))+str(int(dia_disturbance_float[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_disturbance_float[i])
                            vr_mes.append(mes_disturbance_float[i])
                            vr_dia.append(dia_disturbance_float[i]+j)
                elif dia_disturbance_float[i] + j < 32 and mes_disturbance_float[i] == 10:
                    if dia_disturbance_float[i] + j < 10:
                        cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]))+'0'+str(int(dia_disturbance_float[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]))+'0'+str(int(dia_disturbance_float[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_disturbance_float[i])
                            vr_mes.append(mes_disturbance_float[i])
                            vr_dia.append(dia_disturbance_float[i]+j)
                    elif dia_disturbance_float[i] + j >= 10:
                        cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]))+str(int(dia_disturbance_float[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]))+str(int(dia_disturbance_float[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_disturbance_float[i])
                            vr_mes.append(mes_disturbance_float[i])
                            vr_dia.append(dia_disturbance_float[i]+j)
                elif dia_disturbance_float[i] + j < 31 and (mes_disturbance_float[i] == 11):
                    if dia_disturbance_float[i] + j < 10:
                        cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]))+'0'+str(int(dia_disturbance_float[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]))+'0'+str(int(dia_disturbance_float[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_disturbance_float[i])
                            vr_mes.append(mes_disturbance_float[i])
                            vr_dia.append(dia_disturbance_float[i]+j)
                    elif dia_disturbance_float[i] + j >= 10:
                        cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]))+str(int(dia_disturbance_float[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]))+str(int(dia_disturbance_float[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_disturbance_float[i])
                            vr_mes.append(mes_disturbance_float[i])
                            vr_dia.append(dia_disturbance_float[i]+j)
                elif dia_disturbance_float[i] + j < 32 and mes_disturbance_float[i] == 12:
                    if dia_disturbance_float[i] + j < 10:
                        cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]))+'0'+str(int(dia_disturbance_float[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]))+'0'+str(int(dia_disturbance_float[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_disturbance_float[i])
                            vr_mes.append(mes_disturbance_float[i])
                            vr_dia.append(dia_disturbance_float[i]+j)
                    elif dia_disturbance_float[i] + j >= 10:
                        cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]))+str(int(dia_disturbance_float[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]))+str(int(dia_disturbance_float[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_disturbance_float[i])
                            vr_mes.append(mes_disturbance_float[i])
                            vr_dia.append(dia_disturbance_float[i]+j)
                elif dia_disturbance_float[i] + j < 29 and mes_disturbance_float[i] == 2 and np.remainder(año_disturbance_float[i],4) != 0:
                    if dia_disturbance_float[i] + j < 10:                        
                        cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'020'+str(int(dia_disturbance_float[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'020'+str(int(dia_disturbance_float[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_disturbance_float[i])
                            vr_mes.append(2)
                            vr_dia.append(dia_disturbance_float[i]+j)
                    elif dia_disturbance_float[i] + j >= 10:                        
                        cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'02'+str(int(dia_disturbance_float[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'02'+str(int(dia_disturbance_float[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_disturbance_float[i])
                            vr_mes.append(2)
                            vr_dia.append(dia_disturbance_float[i]+j)
                elif dia_disturbance_float[i] + j < 30 and mes_disturbance_float[i] == 2 and np.remainder(año_disturbance_float[i],4) == 0:
                    if dia_disturbance_float[i] + j < 10:                        
                        cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'020'+str(int(dia_disturbance_float[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'020'+str(int(dia_disturbance_float[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_disturbance_float[i])
                            vr_mes.append(2)
                            vr_dia.append(dia_disturbance_float[i]+j)
                    elif dia_disturbance_float[i] + j >= 10:                        
                        cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'02'+str(int(dia_disturbance_float[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'02'+str(int(dia_disturbance_float[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_disturbance_float[i])
                            vr_mes.append(2)
                            vr_dia.append(dia_disturbance_float[i]+j)
                elif dia_disturbance_float[i] + j > 32 and (mes_disturbance_float[i] == 1 or mes_disturbance_float[i] == 3 or mes_disturbance_float[i] == 5 or mes_disturbance_float[i] == 7 or mes_disturbance_float[i] == 8):
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]+1))+'0'+str(int(dia_disturbance_float[i]+j-31))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]+1))+'0'+str(int(dia_disturbance_float[i]+j-31))+'_v06.cdf')
                    for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_disturbance_float[i])
                            vr_mes.append(mes_disturbance_float[i] + 1)
                            vr_dia.append(dia_disturbance_float[i] + j - 31)
                elif dia_disturbance_float[i] + j > 31 and (mes_disturbance_float[i] == 4 or mes_disturbance_float[i] == 6):                    
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]+1))+'0'+str(int(dia_disturbance_float[i]+j-30))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'0'+str(int(mes_disturbance_float[i]+1))+'0'+str(int(dia_disturbance_float[i]+j-30))+'_v06.cdf')
                    for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_disturbance_float[i])
                            vr_mes.append(mes_disturbance_float[i] + 1)
                            vr_dia.append(dia_disturbance_float[i] + j - 30)
                elif dia_disturbance_float[i] + j > 32 and mes_disturbance_float[i] == 10:                    
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]+1))+'0'+str(int(dia_disturbance_float[i]+j-31))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]+1))+'0'+str(int(dia_disturbance_float[i]+j-31))+'_v06.cdf')
                    for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_disturbance_float[i])
                            vr_mes.append(mes_disturbance_float[i] + 1)
                            vr_dia.append(dia_disturbance_float[i] + j - 31)
                elif dia_disturbance_float[i] + j > 31 and (mes_disturbance_float[i] == 9 or mes_disturbance_float[i] == 11):
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]+1))+'0'+str(int(dia_disturbance_float[i]+j-30))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+str(int(mes_disturbance_float[i]+1))+'0'+str(int(dia_disturbance_float[i]+j-30))+'_v06.cdf')
                    for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_disturbance_float[i])
                            vr_mes.append(mes_disturbance_float[i] + 1)
                            vr_dia.append(dia_disturbance_float[i] + j - 30)
                elif dia_disturbance_float[i] + j > 32 and mes_disturbance_float[i] == 12:                    
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]+1))+'01'+'0'+str(int(dia_disturbance_float[i]+j-31))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]+1))+'01'+'0'+str(int(dia_disturbance_float[i]+j-31))+'_v06.cdf')
                    for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_disturbance_float[i] + 1)
                            vr_mes.append(1)
                            vr_dia.append(dia_disturbance_float[i] + j - 31)
                elif dia_disturbance_float[i] + j > 29 and mes_disturbance_float[i] == 2 and np.remainder(año_disturbance_float[i],4) != 0:                    
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'03'+'0'+str(int(dia_disturbance_float[i]+j-28))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'03'+'0'+str(int(dia_disturbance_float[i]+j-28))+'_v06.cdf')
                    for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_disturbance_float[i])
                            vr_mes.append(3)
                            vr_dia.append(dia_disturbance_float[i] + j - 28)
                elif dia_disturbance_float[i] + j > 30 and mes_disturbance_float[i] == 2 and np.remainder(año_disturbance_float[i],4) == 0:
                    cdf = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_disturbance_float[i]))+'03'+'0'+str(int(dia_disturbance_float[i]+j-29))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christiracing/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_disturbance_float[i]))+'03'+'0'+str(int(dia_disturbance_float[i]+j-29))+'_v06.cdf')
                    for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_disturbance_float[i])
                            vr_mes.append(3)
                            vr_dia.append(dia_disturbance_float[i] + j - 29)

                tv = np.concatenate((tv,cdf1['Epoch'][:]),0)
                Vx = np.concatenate((Vx,cdf1['V_GSE'][:,0]),0)
                Np = np.concatenate((Np,cdf1['Np'][:]),0)                                
                t = np.concatenate((t,cdf['Epoch'][:]),0)
                Bx = np.concatenate((Bx,cdf['BGSEc'][:,0]),0)
                By = np.concatenate((By,cdf['BGSEc'][:,1]),0) 
                Bz = np.concatenate((Bz,cdf['BGSEc'][:,2]),0)
                Tpr = np.concatenate((Tpr,cdf1['Tpr'][:]),0)

#ACÁ TERMINAN DE ABRIRSE Y CREARSE LAS MATRICES A PLOTEAR PARA CADA i EVENTO        

        errornp = np.where(Np == -1e+31) #Ubico los errores        
        errorvx = np.where(Vx == -1e+31) #Ubico los errores
        errortpr = np.where(Tpr == -1e+31) #Ubico los errores
        Np = np.delete(Np,errornp) #Borro los errores
        Vx = np.delete(Vx,errorvx) #Borro los errores
        Tpr = np.delete(Tpr,errortpr) #Borro los errores
        tnp = np.delete(tv, errornp) #Borro los errores
        tvx = np.delete(tv, errorvx) #Borro los errores
        ttpr = np.delete(tv, errortpr) #Borro los errores

        errory = np.where(By == -1e+31) #Ubico los errores
        errorz = np.where(Bz == -1e+31) #Ubico los errores        
        errorx = np.where(Bx == -1e+31) #Ubico los errores
        Bx = np.delete(Bx,errorx) #Borro los errores
        By = np.delete(By,errory) #Borro los errores
        Bz = np.delete(Bz,errorz) #Borro los errores
        tx = np.delete(t, errorx) #Borro los errores
        ty = np.delete(t, errory) #Borro los errores
        tz = np.delete(t, errorz) #Borro los errores     
                
        B = np.sqrt((Bx * Bx) + (By * By) + (Bz * Bz)) #Calculo el módulo de B, en otras palabras el B total
        
        
        df_mag = pd.DataFrame({'tiempo': tx,
        'Bx': Bx,
        'By': By,
        'Bz': Bz,
        'B': B,
        })

        df_mag.to_csv("/media/christiracing/Elements/Doctorado/mag_icme/mag_icme" + str(i) + ".csv", index= False) # Guardo el archivo sin los índices
        
        df_mag = pd.DataFrame({'tiempo': tvx,
        'Vx': Vx,
        })
        
        df_mag.to_csv("/media/christiracing/Elements/Doctorado/swepam_icme/vx_icme" + str(i) + ".csv", index= False) # Guardo el archivo sin los índices        
        
        df_mag = pd.DataFrame({'tiempo': tnp,
        'Np': Np,
        })
        
        df_mag.to_csv("/media/christiracing/Elements/Doctorado/swepam_icme/Np_icme" + str(i) + ".csv", index= False) # Guardo el archivo sin los índices        
        
        df_mag = pd.DataFrame({'tiempo': ttpr,
        'Tpr': Tpr,
        })
        
        df_mag.to_csv("/media/christiracing/Elements/Doctorado/swepam_icme/Tpr_icme" + str(i) + ".csv", index= False) # Guardo el archivo sin los índices
        print("Va por: " + str(i))