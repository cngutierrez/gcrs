#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 16:53:52 2021

@author: christiracing
"""

"""
Código para scrapear la página web de nmdb, sirve para sacar info de las distintas
estaciones de NM, en este caso se sacaron datos de MCMurdo, pero cambiando la parte de
stations[]=XXX se puede obtener información de cualquier otra estación.
Cada archivo que voy a generar tiene datos de 5 días, ya que si se alarga el intervalo
temporal los datos dejan de ser por minuto.
"""

import requests
from bs4 import BeautifulSoup as BS 

from datetime import datetime  
from datetime import timedelta  

fechas = [] # Genero la lista fechas 
fechas.append(datetime(1998,1,1)) # Ingreso la fecha inicial en la que se va a empezar a bajar los datos.

j = 0 # Comienzo la iteración

while fechas[j].year < 2017: # Termino en 2017 porque los datos de ICMEs que tengo terminan en esa fecha, pero podrían terminar cuando yo quiera cambiando el año 2017 por otro.
    fechas.append(fechas[j] + timedelta(days=5)) # Voy llenando la lista fechas cada 6 días. Es decir, voy a bajar datos del día 1 al 6 en el primer archivo, del 6 al 11 en el otro, y así sucesivamente.
    j += 1
    
for j in range(10): # Itero según cuanto archivos quiero guardar, para guardar todos debería poner len(fechas)
    if j == 0: # Hay que hacer una salvedad en la primera iteración y es que la primera vez el tiempo debe iniciar en el minuto CERO, mientras que apartir de la segunda tiene que arrancar siempre del minuto UNO, ya que el cero va a quedar guardado en el archivo anterior!!!!!!!
        url = "https://www.nmdb.eu/nest/draw_graph.php?formchk=1&stations[]=MCMU&output=ascii&tabchoice=ori&dtype=corr_for_preassure&date_choice=bydate&start_year=" + str(fechas[j].year) + "&start_month=" + str(fechas[j].month) + "&start_day=" + str(fechas[j].day) + "&start_hour=00&start_min=00&end_year=" + str(fechas[j + 1].year) + "&end_month=" + str(fechas[j + 1].month) + "&end_day=" + str(fechas[j + 1].day) + "&end_hour=00&end_min=00&yunits=0"
    else:
        url = "https://www.nmdb.eu/nest/draw_graph.php?formchk=1&stations[]=MCMU&output=ascii&tabchoice=ori&dtype=corr_for_preassure&date_choice=bydate&start_year=" + str(fechas[j].year) + "&start_month=" + str(fechas[j].month) + "&start_day=" + str(fechas[j].day) + "&start_hour=00&start_min=01&end_year=" + str(fechas[j + 1].year) + "&end_month=" + str(fechas[j + 1].month) + "&end_day=" + str(fechas[j + 1].day) + "&end_hour=00&end_min=00&yunits=0"

    response = requests.get(url) # Abro la pàgina correspondiente

    soup = BS(response.content) # Genero el elemento soup

    GCRs = soup.find_all("code") # Filtro por code, para quedarme con la parte que me interesa

    f = open("/media/christiracing/Elements/Doctorado/gcrs/data" + str(j) + ".txt", "w") # Voy generando los archivos necesarios.
    f.write(str(GCRs))
    f.close


