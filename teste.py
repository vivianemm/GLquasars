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
from astropy.coordinates import SkyCoord
from astropy import *


# importando dados
quasars = pd.read_csv("Quasars_SpecObjAll.csv", dtype={'SpecObjId': int})
# print(quasars.head(5))

#calculando distancia entre qsos de mesmo z

# quasars.ra quasars.dec
for i in quasars:
    a = SkyCoord(i.ra, i.dec, unit = "deg")









