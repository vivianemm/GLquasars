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

SELECT SpecObjId, z, ra, dec, class
FROM SpecObjAll s1
WHERE class = 'QSO' AND zWarning = 0 AND
exists
(SELECT z
FROM SpecObjAll s2
WHERE class = 'QSO' AND zWarning = 0 and
 s1.z = s2.z
GROUP BY z
HAVING count(*) >= 4)

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
from sklearn.metrics.pairwise import pairwise_distances
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


def separa2(dataf):
    data = dataf.values  # array with all the table rows
    i= 0
    j = 1
    group=[data[0]]
    all_groups = []
    while j < len(dataf):

        if data[i][1] == data[j][1]:
            group.append(data[j])  # add that row to the list of the group

        else:
            all_groups.append(group)  # add the group to the list of all groups
            i = j
            group=[]
            group.append(data[i])

        j+=1

    n = np.array(all_groups)
    return n  # pulando o ultimo do grupo


# s = separa2(quasars_test)
# print(type(s)) -> array


# Takes two arrays from the feature array
# returns distance between them
def metric_func(array1, array2):
    a = SkyCoord(array1[0], array1[1], unit="deg")
    b = SkyCoord(array2[0], array2[1], unit="deg")
    return a.separation(b).arcsecond


# creates the distance matrix
def D_matrix(dataf, f_metric):
    dataf_coords = dataf.drop(['SpecObjId', 'z'], axis=1) # keeping only ra and dec on dataframe
    coords_array = separa2(dataf_coords) # separating quasars into groups with same z
    dmatrix = pairwise_distances(coords_array, metric=f_metric) # distance matrix
    return dmatrix


dataf_coords = quasars_test.drop(['SpecObjId', 'z'], axis=1)  # keeping only ra and dec on dataframe
coords_array = separa2(dataf_coords)  # separating quasars into groups with same z
print(coords_array) # problema ->>>> listas separadas

#D_matrix(quasars_test, metric_func)


def dbscan(X, eps, min_samples):
    db = DBSCAN(eps, min_samples, metric="precomputed").fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    print('Estimated number of clusters: %d' % n_clusters_)
    print('Estimated number of noise points: %d' % n_noise_)


# adds key and value to dictionary
def add_dict(dict, key, value):
    dict[key] = value
    print('sl')


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

