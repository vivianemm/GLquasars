from astropy.coordinates import SkyCoord
import pandas as pd


quasars = pd.read_csv("teste.csv", dtype={'SpecObjId': int})

# criando listas com as valores de ra e dec
ras = quasars.ra
decs = quasars.dec
z = quasars.z

def distance(i, j):
    a = SkyCoord(quasars.loc[i, 'ra'], quasars.loc[i, 'dec'], unit="deg")
    b = SkyCoord(quasars.loc[j, 'ra'], quasars.loc[j, 'dec'], unit="deg")
    return a.separation(b).arcsecond

def add_dict(dict, key, value):
    dict[key] = value



# calculando distancias entre os quasares e adicionando a lista seps
sep_list = []

cont = 1
for i in range(0, len(quasars)):
    seps = {}
    add_dict(seps, 'z', quasars.loc[i, 'z'])  # adds group's z
    add_dict(seps, 'id' + str(i), quasars.loc[i, 'SpecObjId']) # adds first quasar
    #seps['id' + str(i)] = quasars.loc[i, 'SpecObjId']
    while quasars.loc[i, 'z'] == quasars.loc[cont, 'z']:
        print('ok')
#    while z[i] == z[cont]:
#        sep = distance(i, cont)
#        add_dict(seps, 'id' + str(cont), sep)
#        seps['id' + str(cont)] = quasars.loc[i, 'SpecObjId']
        cont = cont + 1
#
 #   sep_list.append(seps)
#print(sep_list)



#for i in range(0,len(ras)):
#    a = SkyCoord(ras[i], decs[i] , unit = "deg")
#    for j in range(i+1,len(ras)):
#        b = SkyCoord(ras[j], decs[j], unit="deg")
#        sep = a.separation(b).arcsecond
#        if sep <= 5:
#            seps.append(sep)
