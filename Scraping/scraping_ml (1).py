#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from sys import argv

# ### Defining functions

def pick_table(key):
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
        if pair[0] in df.columns:
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
    if len(df) > 0:
        df.to_csv(filename, index = i)
    return None


# ### System table
# ### (5, 6, 7, 11, 12, 20)


def system():
    # joining 5,6,7,11
    frames =[pick_table('Discovery'), pick_table('Lens Kind'), pick_table('Lens Grade'), pick_table('Description')]
    result_df = pd.concat(frames)
    result_df.reset_index(drop=True, inplace=True)
    system_df = result_df.drop(columns=0).T
    system_df.columns = list(result_df[0])
    drop_nans(system_df)

    # Splitting value ± error columns
    split_col(system_df, [['Einstein_R ["]','Einstein_R'], ['z_Lens', 'z_lens'], ['z_Source(s)', 'z_source'],
                          ['Stellar velocity disp', 'Stellar_v_disp']])

    # adding other 2 tables
    date_df = pick_table('Discovery Date:')
    n_df = pick_table('Number of Source Plane Images')

    system_df['Discovery Date'] = date_df[3][0]
    system_df['Name'] = date_df[1][0]
    system_df['N Images'] = n_df[1][0]

    return system_df


#### Coordinates table (13)
def coordinates():
    coords_df = pick_table('Coordinates:').drop(2, axis=1)  # Manual coordinates
    coords_df = coords_df.set_index(0).T
    coords_df['Coordinates:'] = 'Manual'
    return coords_df


#### External links
def external():
    external_df = pick_table('External Links:')
    #external_df.columns = [''] * len(external_df.columns)
    external_df = external_df.set_index('External Links:').T
    drop_nans(external_df)
    external_df = external_df.T
    external_df.drop('External Links:.1', axis=1, inplace=True)


    tb = soup.find_all('table')[9]
    links = get_table_links(tb)

    external_df['links'] = links

    return external_df


#### Flux table (SDSS 16, HST 17)
def sdss():
    df = pick_table('Filter')
    if 'SDSS' in df.columns.values:
        sdss_df = df.set_index('Band')
        sdss_df = sdss_df.drop(columns=['Unnamed: 1'])
    else:
        sdss_df = pd.DataFrame()

    return sdss_df


def hst():
    hst_df = pick_table('HST')
    hst_df = hst_df.drop(columns=['Unnamed: 1'])
    hst_df = hst_df.set_index('Band')
    return hst_df


def flux():
    sdss_df = sdss()
    hst_df = hst()

    flux_df = pd.concat([sdss_df, hst_df])

    drop_nans(flux_df)
    split_col(flux_df, [['Lens Magnitude', 'lens_mag'], ['Flux [nmaggie]', 'Flux (nmaggie)'],
                    ['Reff [″]', "ref (arcsec)"], ['axis ratio (AB)', 'axis_ratio (AB)'],
                    ['PA [° E of N]','PA (deg)']])
    return flux_df


#### Redshift table (18, 19)
def redshift():
    z_lens_df = pick_table('Lens Plane Images:')['Lens Plane Images:']
    #z_lens_df = z_lens_df.set_index('No.')

    z_source_df = pick_table('Source Plane Images:')['Source Plane Images:']
    #z_source_df = z_source_df.set_index('No.')

    z_df = pd.concat([z_lens_df, z_source_df], keys=['Lens', 'Source'])
    drop_nans(z_df)

    return z_df


#### Time delay table (21)
def time():
    time_df = pick_table('Time Delays:')
    return time_df


#### References table (14)
def refs():
    soup = BeautifulSoup(open("/home/viviane/GravLens/Scraping/masterlens/masterlens_1.html"), "html.parser")
    tb = soup.find_all('table')[14]
    # links = [np.where(tag.has_attr('href'),tag.get('href'),"no link") for tag in tb.find_all('a')]

    links = get_table_links(tb)
    papers = links[1::2]

    ref_df = df_list[14].drop('Unnamed: 0', axis=1)
    ref_df['Links'] = papers
    ref_df.columns = ['Author', 'Title', 'Discovery', 'Links']
    return ref_df


#### Main code

def main():

    if len(argv) == 0:
        print("APPNAME:\n\t[1] Dir path")
        exist(1)

    filename = argv[1]
    prefix, posfix = filename.replace(".html", ".csv").split("_")
    df_list = pd.read_html(filename)  # list with dfs from tables in file


    system_df = system()
    coords_df = coordinates()
    flux_df = flux()
    z_df = redshift()
    ref_df = refs()
    external_df = external()

    # saving in csv format
    save(system_df, prefix + 'system' + posfix)
    save(coords_df, prefix + 'coordinates' + posfix)
    save(flux_df, prefix + 'flux' + posfix, i=True)
    save(z_df, prefix + 'redshift' + posfix, i=True)
    save(ref_df, prefix + 'references' + posfix)
    save(external_df, prefix + 'external' + posfix,i=True)


    if not np.isnan(list(time()['Time Delay (days)'])).all():
        save(time_df, 'time_d.csv')

if __name__== "__main__" :
    main()
