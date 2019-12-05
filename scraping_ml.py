# coding: utf-8

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from sys import argv

df_list = pd.read_html("masterlens.html")  # list with dfs from tables

#for df in df_list:
#    print(df.columns.values)

# important dfs: 5,6,7,11,12,13,14,16,17,18,19,20,21


# ### Defining functions


def drop_nans(df):
    df.dropna(axis=0, how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    return None



def split_col(df, old_new_list):  # old_new_list = [[oldname, newname], ...]
    for pair in old_new_list:
        df[[pair[1], pair[1] + '_err']] = df[pair[0]].str.split("±", n = 1, expand = True)
        df.drop(pair[0], axis=1, inplace=True)
    return None



def get_table_links(table):
    href_list = []
    
    if isinstance(table, list):
        for row in table:
            href = row.find('a')['href']
            href_list.append(href)
    else:
        href_tags = table.find_all("a")
        for tag in href_tags:
            href = tag.get('href')
            href_list.append(href)
    return href_list


    # ### System table
    # ### (5, 6, 7, 11, 12, 20)


def __main__():
    
    if len(argv) == 0:
        print("APPNAME:\n\t[1] Dir path")
        exist(1)

    filename = argv[1]
    prefix, posfix = filename.replace(".html", ".csv").split("_")
    df_list = pd.read_html(filename)  # list with dfs from tables in file


    # joining 5,6,7,11
    frames =[df_list[5], df_list[6], df_list[7], df_list[11]]
    result_df = pd.concat(frames)
    result_df.reset_index(drop=True, inplace=True)

    system_df = result_df.drop(columns=0).T
    system_df.columns = list(result_df[0])


    # Splitting value ± error columns
    split_col(system_df, [['Einstein_R ["]','Einstein_R'], ['z_Lens', 'z_lens'], ['z_Source(s)', 'z_source'],
                        ['Stellar velocity disp', 'Stellar_v_disp']])



    # adding 12 and 20 to final
    system_df['Discovery Date'] = df_list[12][3][0]
    system_df['Name'] = df_list[12][1][0]
    system_df['N Images'] = df_list[20][1][0]


    # ### Coordinates table (13)


    coords_df = df_list[13].drop(2, axis=1)  # Manual coordinates
    coords_df = coords_df.set_index(0).T

    coords_df['Coordinates:'] = 'Manual'


    # ### Flux table (SDSS 16, HST 17)

    sdss_df = df_list[16].set_index('Band')
    sdss_df = sdss_df.drop(columns=['Unnamed: 1'])


    hst_df = df_list[17]
    hst_df = hst_df.drop(columns=['Unnamed: 1'])
    hst_df = hst_df.set_index('Band')



    flux_df = pd.concat([sdss_df, hst_df])


    drop_nans(flux_df)
    split_col(flux_df, [['Lens Magnitude', 'lens_mag'], ['Flux [nmaggie]', 'Flux (nmaggie)'],
                        ['Reff [″]', "ref (arcsec)"], ['axis ratio (AB)', 'axis_ratio (AB)'],
                        ['PA [° E of N]','PA (deg)']])


    # ### Redshift table (18, 19)


    df18 = df_list[18]['Lens Plane Images:']
    df18 = df18.set_index('No.')


    df19 = df_list[19]['Source Plane Images:']
    df19 = df19.set_index('No.')


    z_df = pd.concat([df18,df19], keys=['Lens', 'Source'])
    drop_nans(z_df)

    # ### Time delay table (21)


    time_df = df_list[21]['Time Delays:']

    # ### References table (14)

    soup = BeautifulSoup(open("masterlens.html"), "html.parser")
    tb = soup.find_all('table')[14] 

    links = get_table_links(tb)
    papers = links[1::2]

    ref_df = df_list[14].drop('Unnamed: 0', axis=1)
    ref_df['Links'] = papers
    ref_df.columns = ['Author', 'Title', 'Discovery', 'Links']
    ref_df


    # ### Saving csv files

    system_df.to_csv(prefix + "System" + posfix, index=False) #""system.csv", index=False) # prefix, posfix
    coords_df.to_csv(prefix + "coordinates.csv" + posfix, index=False)
    flux_df.to_csv(prefix + "flux.csv" + posfix)
    z_df.to_csv(prefix + "redshift.csv" + posfix)
    ref_df.to_csv(prefix + "references.csv" + posfix, index=False)

