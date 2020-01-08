#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from sys import argv

# ### Defining functions

def pick_table(df_list, key):
    for df in df_list:
        list_labels = list(df.columns.values)
        if any(isinstance(i, tuple) for i in list_labels):  # if labels is nested list
            labels = [item for t in list_labels for item in t]  # flatten
        else:
            labels = list_labels

        list_values = df.values.tolist()
        if any(isinstance(i, list) for i in list_values):  # if values is nested list
            values = [item for t in list_values for item in t]  # flatten
        else:
            values = list_values

        if key in values or key in labels:
            #df_list.remove(df)
            return df


def drop_nans(df):
    df.dropna(axis=0, how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    return None


def split_col(df, old_new_list):  # old_new_list = [[oldname, newname], ...]
    for pair in old_new_list:
        if pair[0] in df.columns and type(list(df[pair[0]])[0]) == str and "±" in list(df[pair[0]])[0]:
            df[[pair[1], pair[1] + '_err']] = df[pair[0]].str.split("±", n = 1, expand = True)
            df.drop(pair[0], axis=1, inplace=True)
        else:
            pass
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


def save(df, filename, i=False):
    if df is not None and len(df) > 0:
        df.to_csv(filename, index = i)
    return None


# ### System table
# ### (5, 6, 7, 11, 12, 20)


def system(df_list):
    # joining 5,6,7,11
    frames =[pick_table(df_list, 'Discovery'), pick_table(df_list, 'Lens Kind'),pick_table(df_list, 'Lens Grade'), pick_table(df_list, 'Description')]
    result_df = pd.concat(frames)
    result_df.reset_index(drop=True, inplace=True)
    system_df = result_df.drop(columns=0).T
    system_df.columns = list(result_df[0])
    drop_nans(system_df)

    # Splitting value ± error columns
    split_col(system_df, [['Einstein_R ["]','Einstein_R'], ['z_Lens', 'z_lens'], ['z_Source(s)', 'z_source'],
                          ['Stellar velocity disp', 'Stellar_v_disp']])

    # adding other 2 tables
    date_df = pick_table(df_list, 'Discovery Date:')
    n_df = pick_table(df_list, 'Number of Source Plane Images')

    system_df['Discovery Date'] = date_df[3][0]
    system_df['Name'] = date_df[1][0]
    system_df['N Images'] = n_df[1][0]

    return system_df


#### Coordinates table (13)
def coordinates(df_list):
    coords_df = pick_table(df_list, 'Coordinates:') #.drop(2, axis=1)  # Manual coordinates
    coords_df.drop(2, axis=1, inplace=True)    
    coords_df = coords_df.set_index(0).T
    coords_df['Coordinates:'] = 'Manual'
    coords_df = coords_df.set_index('Coordinates:')

    return coords_df


#### External links
def external(df_list, filename):    
    #external_df.columns = [''] * len(external_df.columns)
    #external_df.drop('External Links:.1', axis=1, inplace=True)
    
    soup = BeautifulSoup(open(filename), "lxml")
    external_df = pick_table(df_list, 'External Links:')
    for table in soup.find_all('table'):
            
        if table.th is not None and table.th.text == 'External Links:':
            refs = get_table_links(table)
        else:
            pass
            
            #if external_df is not None:
    external_df.columns = ['database', 'link']
    external_df = external_df.set_index('database')
    drop_nans(external_df)
    external_df['links'] = refs
    external_df.drop('link', axis=1, inplace=True)
    
    return external_df


#### Flux table (SDSS 16, HST 17)
def sdss(df_list):
    df = pick_table(df_list,'Filter')
    if df is not None and 'SDSS' in df.columns.values:
        sdss_df = df.set_index('Band')
        sdss_df = sdss_df.drop(columns=['Unnamed: 1'])
    else:
        sdss_df = pd.DataFrame()

    return sdss_df


def hst(df_list):
    hst_df = pick_table(df_list,'HST')

    if hst_df is not None:
        hst_df = hst_df.drop(columns=['Unnamed: 1'])
        hst_df = hst_df.set_index('Band')
    else:
        hst_df = pd.DataFrame()
    return hst_df


def flux(df_list):
    sdss_df = sdss(df_list)
    hst_df = hst(df_list)

    flux_df = pd.concat([sdss_df, hst_df])
    
    #flux_df['release'] = list(sdss_df['SDSS']) + list(hst_df['HST'])
    #flux_df = flux_df.drop(columns=['SDSS','HST'])

    drop_nans(flux_df)
    split_col(flux_df, [['Lens Magnitude', 'lens_mag'], ['Flux [nmaggie]', 'Flux (nmaggie)'],
                    ['Reff [″]', "ref (arcsec)"], ['axis ratio (AB)', 'axis_ratio (AB)'],
                    ['PA [° E of N]','PA (deg)']])
    return flux_df


#### Redshift table (18, 19)
def redshift(df_list):

    z_lens_df = pick_table(df_list, 'Lens Plane Images:')
    if z_lens_df is not None:
        z_lens_df = z_lens_df['Lens Plane Images:']
        #z_lens_df = z_lens_df.set_index('No.')
    else:
        z_lens_df = pd.DataFrame()

    z_source_df = pick_table(df_list, 'Source Plane Images:')
    if z_source_df is not None:
        z_source_df = z_source_df['Source Plane Images:']
        #z_source_df = z_source_df.set_index('No.')
    else:
        z_source_df = pd.DataFrame()

    z_df = pd.concat([z_lens_df, z_source_df], keys=['Lens', 'Source'])
    drop_nans(z_df)

    return z_df


#### Time delay table (21)
def time(df_list):
    time_df = pick_table(df_list, 'Time Delays:')

    if time_df is not None:
        times = list(time_df['Time Delays:']['Time Delay (days)'])
    #print(times)
        if np.isnan(times).all():
            time_df = None

    return time_df

#### References table (14)
def refs(filename, df_list):
    soup = BeautifulSoup(open(filename), "html.parser")

    for table in soup.find_all('table'):
    # links = [np.where(tag.has_attr('href'),tag.get('href'),"no link") for tag in tb.find_all('a')]

        links = get_table_links(table)
        #print(links)

        if len(links) >= 2 and 'citation' in links[1]:
            papers = links[1::2]

    ref_df = pick_table(df_list, 'Discovery\xa0Paper')
    ref_df = ref_df.drop('Unnamed: 0', axis=1)

    ref_df['Links'] = papers
    ref_df.columns = ['Author', 'Title', 'Discovery', 'Links']
    return ref_df

#### Main code

def main():
    
    import warnings
    warnings.filterwarnings("ignore")

    if len(argv) == 0:
        print("APPNAME:\n\t[1] Dir path")
        exist(1)

    filename = argv[1]
    prefix, posfix = filename.replace(".html", ".csv").split("_")
    df_list = pd.read_html(filename)  # list with dfs from tables in file


    system_df = system(df_list)
    coords_df = coordinates(df_list)
    flux_df = flux(df_list)
    z_df = redshift(df_list)
    ref_df = refs(filename, df_list)
    external_df = external(df_list, filename)
    time_df = time(df_list)

    # saving in csv format
    save(system_df, prefix + 'system' + posfix)
    save(coords_df, prefix + 'coordinates' + posfix)
    save(flux_df, prefix + 'flux' + posfix, i=True)
    save(z_df, prefix + 'redshift' + posfix, i=True)
    save(ref_df, prefix + 'references' + posfix)
    save(external_df, prefix + 'external' + posfix,i=True)
    save(time_df, 'time_d.csv')

if __name__== "__main__" :
    main()
