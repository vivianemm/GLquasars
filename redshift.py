import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np

start = time.time()

dataframe = pd.read_csv("sdss_z_test.csv", dtype={'objID': int})



# creates histogram of redshifts
def hist_z(data):

    correct_df = data[data.redshift != -9999.0]
    plt.style.use('seaborn')
    plt.figure()

    fig, axs = plt.subplots(2, 1)
    correct_df[['redshift', 'redshift_err']].plot(ax=axs[0], kind='hist', bins=100, alpha=0.85)  # or 'kde'

    correct_df.hist(ax=axs[1], column="redshift_err", bins=50, color='seagreen')

    plt.tight_layout()
    plt.savefig("test.png")
    return None


hist_z(dataframe)
hist_z()
#end = time.ti