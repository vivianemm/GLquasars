from astropy.coordinates import SkyCoord
import pandas as pd
import numpy as np
from csv import *


#quasars = pd.read_csv("teste.csv", dtype={'SpecObjId': int})

# criando listas com as valores de ra e dec
#ras = quasars.ra
#decs = quasars.dec

# calculando distancias entre os quasares e adicionando a lista seps
#seps = []
#for i in range(0,len(ras)):
#    a = SkyCoord(ras[i], decs[i] , unit = "deg")
#    for j in range(i+1,len(ras)):
#        b = SkyCoord(ras[j], decs[j], unit="deg")
#        sep = a.separation(b).arcsecond
#        if sep <= 5:
#            seps.append(sep)

def csv_dict_list(variables_file):
    # Open variable-based csv, iterate over the rows and map values to a list of dictionaries containing key/value pairs

    reader = csv.DictReader(open(variables_file, 'rb'))
    dict_list = []
    for line in reader:
        dict_list.append(line)
    return dict_list

csv_dict_list("teste.csv")






#    b = SkyCoord()
#b = SkyCoord(23.631323, 30.353149 , unit = "deg")

#sep = a.separation(b).arcsecond
#print(sep)