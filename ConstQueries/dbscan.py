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
import time
from scipy.spatial.distance import squareform
from scipy.spatial.distance import pdist



# importing data
quasars_test = pd.read_csv("testeflux.csv", dtype={'bestObjId': int})
quasars_test2 = pd.read_csv("sdss_z_test.csv", dtype={'bestObjId': int})


# determines the separation between quasars of indexes i and j
def distance(data, i, j):
    a = SkyCoord(data.loc[i, 'ra'], data.loc[i, 'dec'], unit="deg")
    b = SkyCoord(data.loc[j, 'ra'], data.loc[j, 'dec'], unit="deg")
    return a.separation(b).arcsecond


# determines the separation between objs u and v
def metric_func2(u, v):
    a = SkyCoord(u['ra'], u['dec'], unit="deg")
    b = SkyCoord(v['ra'], v['dec'], unit="deg")
    return a.separation(b).arcsecond



# modify to use dataframe instead of arrays
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



#def zgroups2(dataf):
#    dataf = dataf[dataf.redshift != -9999.0]
#    sorted_df = dataf.sort_values(by='redshift')

    ###### remove NANs
#    df = sorted_df.dropna(subset=['redshift'])

 #   all_groups_df = df.loc[abs(df['redshift'] - df['redshift'][0]) <= 0.25]  # print(df['redshift'][0] ??????

#    for row in dataf.itertuples(index=True, name='Pandas'):
#        group_df = df.loc[abs(df['redshift'] - getattr(row, 'redshift')) <= 0.25]
#        group_df['center'] = getattr(row, 'objID')
#        #pd.concat([all_groups_df, group_df], names=['', getattr(row, 'objID')])
#        pd.concat([all_groups_df, group_df]
#
#    return all_groups_df



# def flux_filter(groups):


# Takes two arrays from the feature array
# returns distance between them
def metric_func(array1, array2):
    a = SkyCoord(array1[0], array1[1], unit="deg")
    b = SkyCoord(array2[0], array2[1], unit="deg")
    return a.separation(b).arcsecond


def metric_func3(u, v):

    cos = np.cos(90-u[1])*np.cos(90-v[1]) + np.sin(90-u[1])*np.sin(90-v[1])*np.cos(u[0]-v[0])
    sep = np.arccos(cos)

    #a = SkyCoord(u[0], u[1], unit="deg")
    #b = SkyCoord(v[0], v[1], unit="deg")
    #return a.separation(b).arcsecond
    return sep


# creates the distance matrix
def D_matrix(dataf, f_metric):
    groups = z_groups(dataf)
    all_matrices = []
    for group in groups:

        d_matrix = pairwise_distances(group, metric=f_metric)  # distance matrix for each z group
        all_matrices.append(d_matrix)  # adds group's matrix to list of matrices
    d_matrices = np.array(all_matrices)
    return d_matrices  # array with all matrices


def D_matrix2(dataf, f_metric):

    dataf = dataf[dataf.redshift != -9999.0]
    #sorted_df = dataf.sort_values(by='redshift')

    ###### remove NANs
    df = dataf.dropna(subset=['redshift'])
    t = 1
    d=1
    all_matrices = []
    for row in df.itertuples(index=True, name='Pandas'):
        group_df = df.loc[abs(df['redshift'] - getattr(row, 'redshift')) <= 0.25]  # z group with center i
        print('group' + str(t))
        t += 1
        print(str(group_df.shape))


        d_matrix = pairwise_distances(group_df[['ra', 'dec']].values, metric=f_metric)  # distance matrix for each z group
        print('d matrix' + str(d))
        d += 1
        all_matrices.append(d_matrix)  # adds group's matrix to list of matrices

    d_matrices = np.array(all_matrices)
    return d_matrices  # array with all matrices


def D_matrix3(dataf, f_metric):

    dataf = dataf[dataf.redshift != -9999.0]
    #sorted_df = dataf.sort_values(by='redshift')

    ###### remove NANs
    df = dataf.dropna(subset=['redshift'])
    t = 1
    d=1
    all_matrices = []
    for row in df.itertuples(index=True, name='Pandas'):
        group_df = df.loc[abs(df['redshift'] - getattr(row, 'redshift')) <= 0.25]  # z group with center i
        print('group' + str(t))
        t += 1
        print(str(group_df.shape))

        d_array = pdist(group_df[['ra', 'dec']], f_metric)
        d_matrix = squareform(d_array)

        print('d matrix' + str(d))
        d += 1
        all_matrices.append(d_matrix)  # adds group's matrix to list of matrices

    d_matrices = np.array(all_matrices)
    return d_matrices  # array with all matrices


def D_matrix3(dataf, f_metric):

    dataf = dataf[dataf.redshift != -9999.0]
    sorted_df = dataf.sort_values(by='redshift')

    ###### remove NANs
    df = sorted_df.dropna(subset=['redshift'])

    all_matrices = []
    for row in df.itertuples(index=True, name='Pandas'):
        for row2 in df.itertuples():
            if abs(getattr(row, 'redshift') - getattr(row2, 'redshift'))<=abs(getattr(row, 'redshift_err') + getattr(row2, 'redshift_err')):
                pass
            else:
                sorted_df = sorted_df[:]


        d_array = pdist(group_df[['ra', 'dec']], f_metric)
        d_matrix = squareform(d_array)

        print('d matrix' + str(d))
        d += 1
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


start = time.time()

a = D_matrix3(quasars_test2, metric_func3)
cont = 0
for x in a:
    dbscan(x, 5, 3)
    print(cont)
    cont+=1

end = time.time()
time = end - start
print(time)




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

