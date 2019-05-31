"""

teste inicial sem spark

Query SQL in Skyserver:

SELECT bestObjId, z, ra, dec, class
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

######### margem para z e fluxos

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
quasars_test = pd.read_csv("testeflux.csv", dtype={'bestObjId': int})


# determines the separation between quasars of indexes i and j
def distance(data, i, j):
    a = SkyCoord(data.loc[i, 'ra'], data.loc[i, 'dec'], unit="deg")
    b = SkyCoord(data.loc[j, 'ra'], data.loc[j, 'dec'], unit="deg")
    return a.separation(b).arcsecond


# separates quasars into groups with same z
# returns array with arrays of each group
def z_groups(dataf):
    dataf = dataf.drop(['bestObjId', 'spectroFlux_u', 'spectroFlux_g', 'spectroFlux_r', 'spectroFlux_i', 'spectroFlux_z'], axis=1)
    data = dataf.values  # array with all the table rows
    i = 0
    j = 1
    first = np.delete(data[0], 0)
    group = [first]  # adds first row
    all_groups = []
    while j < len(dataf):

        if data[i][0] == data[j][0]:
            coords = np.delete(data[j], 0)
            group.append(coords)  # add that row to the list of the group

        else:
            all_groups.append(group)  # add the group to the list of all groups
            i = j
            group=[]
            first = np.delete(data[i], 0)
            group.append(first)

        j += 1

    n = np.array(all_groups)
    return n  # pulando o ultimo do grupo


#
# def flux_filter(groups):


# Takes two arrays from the feature array
# returns distance between them
def metric_func(array1, array2):
    a = SkyCoord(array1[0], array1[1], unit="deg")
    b = SkyCoord(array2[0], array2[1], unit="deg")
    return a.separation(b).arcsecond


# creates the distance matrix
def D_matrix(dataf, f_metric):
    groups = z_groups(dataf)
    all_matrices = []
    for group in groups:

        d_matrix = pairwise_distances(group, metric=f_metric)  # distance matrix for each z group
        all_matrices.append(d_matrix)  # adds group's matrix to list of matrices
    d_matrices = np.array(all_matrices)
    return d_matrices  # array with all matrices


# applies dbscan to the distance matrix
def dbscan(d_matrix, eps, min_samples):
    db = DBSCAN(eps, min_samples, metric="precomputed").fit(d_matrix)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    print('Estimated number of clusters: %d' % n_clusters_)
    print('Estimated number of noise points: %d' % n_noise_)


a = D_matrix(quasars_test, metric_func)
for x in a:
    dbscan(x, 5, 3)


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

