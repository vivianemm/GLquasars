import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn')

lens_df = pd.read_csv('masterlens.csv')
print(lens_df.columns)

grouped = lens_df.groupby('number_images')['system_name'].count()
print(grouped)

grouped.plot.bar(rot=0)
plt.show()

