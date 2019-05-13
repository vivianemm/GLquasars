"""

teste inicial sem spark

Query SQL in Skyserver:

SELECT SpecObjId, z, ra, dec
FROM SpecObjAll
WHERE class = 'QSO' AND zWarning = 0 AND EXISTS

(SELECT z, count(*)
FROM SpecObjAll
WHERE class = 'QSO' AND zWarning = 0
GROUP BY z
HAVING count(*) > 2)

ORDER BY z

"""

# arquivo csv
#
# header
# SpecObjId, z, ra, dec (deg)

import pandas as pd
import numpy as np
from astropy.coordinates import SkyCoord
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import astropy.units as u


# importing data
quasars = pd.read_csv("Quasars_SpecObjAll.csv", dtype={'SpecObjId': int})
quasars_test = pd.read_csv("teste.csv", dtype={'SpecObjId': int})


# determines the separation between quasars of indexes i and j
def distance(data, i, j):
    a = SkyCoord(data.loc[i, 'ra'], data.loc[i, 'dec'], unit="deg")
    b = SkyCoord(data.loc[j, 'ra'], data.loc[j, 'dec'], unit="deg")
    return a.separation(b).arcsecond


# adds key and value to dictionary
def add_dict(dict, key, value):
    dict[key] = value


# converts pandas dataframe into dictionary
def pd_dict(data):
    return data.to_dict()

#dic = pd_dict(quasars_test)
#print(dic)
#print(dic['SpecObjId'][1])



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
            add_dict(seps, str(i) + '_' + str(i+cont), sep) # adds separation
            cont += 1

        add_dict(dict_master, data.loc[i, 'z'], seps) # adds dictionary of distances to master dictionary

    return dict_master

def sep_dictionaries2(data): # usando pd to dict
    dict_master = {}
    seps = {}

    for i in range(len(data)-1):
        add_dict(seps, 'id' + str(i), data.loc[i, 'SpecObjId'])  # adds quasar i
        cont = 1

        while data.loc[i, 'z'] == data.loc[i+cont, 'z']:
            sep = distance(data, i, i+cont)
            add_dict(seps, str(i) + '_' + str(i+cont), sep) # adds separation
            cont += 1

        add_dict(dict_master, data.loc[i, 'z'], seps) # adds dictionary of distances to master dictionary

    return dict_master



def dbscan(X, eps, min_samples):
    db = DBSCAN(eps, min_samples).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    print('Estimated number of clusters: %d' % n_clusters_)
    print('Estimated number of noise points: %d' % n_noise_)



# Aitoff projection of quasars
def aitoff(data):
    c = SkyCoord(data.ra, data.dec, unit="deg")
    ra_rad = c.ra.wrap_at(180 * u.deg).radian
    dec_rad = c.dec.radian

    plt.figure(figsize=(8, 4.2))
    plt.subplot(111, projection="aitoff")
    plt.title("Aitoff projection")
    plt.grid(True)
    plt.plot(ra_rad, dec_rad, 'o', markersize=1, alpha=0.3)
    plt.show()
    print(c)

#result = sep_dictionaries(quasars_test)
#print(result)

# pairwise distances






