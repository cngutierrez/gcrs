#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 18:16:33 2021

@author: christiracing
"""

"""
Este script agarra todos los archivos que se descargaron en la carpeta gcrs y 
los convierte en uno (o varios) archivos .csv para manipular mejor los datos
"""

import numpy as np
import pandas as pd


dias = np.arange(1386) # Creo el vector días, en donde el número del paréntesis indica hasta que archivo se va a abrir.
dataframe = [] # Creo la lista vacía dataframe, en donde voy a ir agregando TODOS los datos de TODOS los archivos que voy a ir abriendo.

for k in range(len(dias)): # Comienzo la iteración
    a = [] # Genero la lista vacia a
    with open("/media/christiracing/Elements/Doctorado/gcrs/data" + str(dias[k]) + ".txt","r") as fp: # Voy abriendo cada archivo
       line = fp.readline()
       cnt = 25
       while line:
#           print("Line {}: {}".format(cnt, line.strip()))
           a.append("Line {}: {}".format(cnt, line.strip()))
           line = fp.readline()
           cnt += 1
           
           
    a = a[25:-1] # En la lista a me guardo desde la línea 25 de cada archivo y saco la última. Esto es porque los datos arrancan desde la línea 25 y la última no son datos.
    
    
    string = [] # Creo la lista vacía string
    
    for i in range(len(a)): # Recorro todos los datos de a
        string.append(a[i]) # Comienzo a llenar la lista string con cada una de las filas de a
    
        j = 0 # Comienzo a iterar
        linea = string[i] # Me quedo con cada elemento de string para analizarlo por separado
        
        while linea[j] != ':': # Como los datos arrancan desde el ":" de cada string, busco la ubicación del ":" y comienzo a leer los datos desde ahí
            j += 1
        
        linea = linea[j+2:] #Comienzo a leer los datos desde ahí, ya que son de la forma (Línea XXX: XXXX-XX-XX XX:XX:XX;XXX.XX)
        linea = linea.replace('-', ',') # Reemplazo los "-" por "," para crear el .csv
        linea = linea.replace(':', ',') # Reemplazo los ":" por "," para crear el .csv
        linea = linea.replace(';', ',') # Reemplazo los ";" por "," para crear el .csv
        linea = linea.replace(' ', ',') # Reemplazo los " " por "," para crear el .csv
        
        string[i] = linea # Creo que está de más
        dataframe.append(linea) # Voy almacenando toda los datos de todos los archivos en la lista dataframe

año = [] # Creo la lista vacía año
mes = [] # Creo la lista vacía mes
dia = [] # Creo la lista vacía dia
hora = [] # Creo la lista vacía hora
minuto = [] # Creo la lista vacía minuto
segundo = [] # Creo la lista vacía segundo
relative_count = [] # Creo la lista vacía relative_count

for j in range(len(dataframe)): # Recorro la lista dataframe por completo
    dato = dataframe[j] # Me voy quedando con cada elemen to individual de la lista dataframe
    dato = dato.split(",") # Separo el dato por ",", Por lo que me quedan 7 elementos por cada dato.
    año.append(dato[0]) # Me voy quedando con los años
    mes.append(dato[1]) # Me voy quedando con los meses
    dia.append(dato[2]) # Me voy quedando con los dias
    hora.append(dato[3]) # Me voy quedando con las horas
    minuto.append(dato[4]) # Me voy quedando con los minutos
    segundo.append(dato[5]) # Me voy quedando con los segundos
    relative_count.append(dato[6]) # Me voy quedando con los gcrs
    
"""
data = {'año':  [año],
        'mes': [mes],
        'dia': [dia],
        'hora': [hora],
        'minuto': [minuto],
        'segundo': [segundo],
        'relative_count': [relative_count],
        }
"""

# Genero el dataframe pandas para luego guardar el .csv

df = pd.DataFrame({'año': año,
        'mes': mes,
        'dia': dia,
        'hora': hora,
        'minuto': minuto,
        'segundo': segundo,
        'relative_count': relative_count,
        })

df.to_csv("/media/christiracing/Elements/Doctorado/Materias/CosmicRayData.csv", index= False) # Guardo el archivo sin los índices