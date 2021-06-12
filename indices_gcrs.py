#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 00:27:54 2021

@author: christiracing
"""

import numpy as np
import pandas as pd

filename = '/media/christiracing/Elements/Doctorado/Materias/CosmicRayData.csv'
df = pd.read_csv(filename)

j = 0
indices = []

vector_años = np.arange(1998, 2016, step=1)
for k in vector_años:
    for i in range(12):
        while df.año[j] <= k and df.mes[j] == i + 1: 
            j += 1    
        indices.append(j)
        print(k)

data_años = []
data_meses = []
 
for j in range(18):
    for i in range(12):
        data_años.append(j + 1998)
        data_meses.append(i+1)

df = pd.DataFrame({'año': data_años,
        'mes': data_meses,
        'indice': indices,
        })

df.to_csv("/media/christiracing/Elements/Doctorado/Materias/IndicesGCRs.csv", index= False) # Guardo el archivo sin los índices