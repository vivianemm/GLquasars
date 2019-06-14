import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np

start = time.time()

dataframe = pd.read_csv("sdss_z_test.csv", dtype={'objID': int})



# creates histogram of redshifts
def hist_z(data):

    correct_df = data[data.redshift != -9999.0]
    correct_df.hist(column="redshift", bins=1000)
    hist = np.histogram(correct_df["redshift"], bins=100)
    print(hist[1])
    plt.show()
    return None


hist_z(dataframe)

#end = time.ti