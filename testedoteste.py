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


# adds key and value to dictionary
def add_dict(dict, key, value):
    dict[key] = value
    print('sl')


# converts pandas dataframe into dictionary
def pd_dict(data):
    return data.to_dict()


# dic = pd_dict(quasars_test)
# print(dic)
# print(dic['SpecObjId'][1])


# creates a list a dictionaries with keys z, ids of quasars for that z
# and separation between the pairs
def sep_dictionaries(data):
    dict_master = {}
    seps = {}

    for i in range(len(data)-1):
        add_dict(seps, 'id' + str(i), data.loc[i, 'SpecObjId'])  # adds quasar i
        cont = 1

        while data.loc[i, 'z'] == data.loc[i+cont, 'z']:
            sep = distance(data, i, i+cont)
            add_dict(seps, str(i) + '_' + str(i+cont), sep)  # adds separation
            cont += 1

        add_dict(dict_master, data.loc[i, 'z'], seps)  # adds dictionary of distances to master dictionary

    return dict_master