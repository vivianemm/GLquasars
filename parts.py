"""
partition 103

SELECT
   p.objid,p.ra,p.dec,p.u,p.g,p.r,p.i,p.z,
   s.specobjid, s.class, s.z as redshift
FROM PhotoObj AS p
   JOIN SpecObj AS s ON s.bestobjid = p.objid

# header:
objid,ra,dec,u,g,r,i,z,specobjid,class,redshift


"""

import pandas as pd

dataframe = pd.read_csv("PhotoObjAll.csv", dtype={'bestObjId': int, 'specobjid' : int})


# separates the partitions in the file into a list
def sep_parts(partitions):
    file = open(partitions, "r")
    parts = []
    coords = []

    for line in file:
        l = line.split()
        if len(l) > 0 and l[0] == 'RA':
            coords.append(l[2].split(','))

        elif len(l) > 0 and l[0] == 'DEC=':
            coords.append(l[1].split(','))
            parts.append(coords)

    file.close()
    return parts


a = sep_parts("partitions.txt")
print(a)

#def z_count(data, parts):
