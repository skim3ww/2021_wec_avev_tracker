#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import numpy as np
import datetime
import glob
import re 
import os
import time
from csv import reader


# In[2]:


#makes floats diplay commas and two decimals
pd.options.display.float_format = '{:,.2f}'.format

# makes ints display commas 
class _IntArrayFormatter(pd.io.formats.format.GenericArrayFormatter):

    def _format_strings(self):
        formatter = self.formatter or (lambda x: ' {:,}'.format(x))
        fmt_values = [formatter(x) for x in self.values]
        return fmt_values

pd.io.formats.format.IntArrayFormatter = _IntArrayFormatter

pd.set_option('display.max_columns', None)


# ## Scraping the Registered Voter Population
# I'm scraping all of the Voter Registration Statistics table rows and putting the date, title, and link into the vr_tbl.csv file. I'm going to use the file to loop through the links to get to the files.

# In[4]:


from requests_html import HTML, HTMLSession
import csv
import urllib


# In[5]:


# Go to https://elections.wi.gov/index.php/publications/statistics/registration
session = HTMLSession()
r = session.get('https://elections.wi.gov/index.php/publications/statistics/registration')


# In[6]:


# Capture the table of Registered Voter Population Statistics over the past
table = r.html.find('tbody', first=True)
rows = table.find('tr')

# Capture the most recent, top entry
most_recent_date = rows[0].find('time', first=True).text
most_recent = rows[0].find('a', first=True).attrs['href']


# ### Get County and Wards Files

# In[8]:


# stores url to get to the page with the files
starter_url = 'https://elections.wi.gov'
url = starter_url + most_recent

# turns American style date to normal dates like this: 20210301
date_pattern = re.compile(r'(\d{2})/(\d{2})/(\d{4})')
date = date_pattern.sub(r'\3\1\2', most_recent_date)


# In[9]:


# Captures the tables with the files
month = session.get(url)
table = month.html.find('tbody', first=True)
file_rows = table.find('tr')


# In[10]:


for file_row in file_rows:
    title = file_row.find('a', first=True).text
    file = file_row.find('a', first=True).attrs['href']
    
    if re.search(r'[c|C]ounty', title):
        #print(title)
        f = session.get(file)
        with open('scrapped_files/vr_county_{}.xlsx'.format(date), 'wb') as outfile:
            outfile.write(f.content)
    elif re.search(r'[w|W]ard', title):
        #print(title)
        f = session.get(file)
        with open('scrapped_files/vr_muni_{}.xlsx'.format(date), 'wb') as outfile:
            outfile.write(f.content)
    time.sleep(1)


# ## Scraping the Absentee Ballot Stats

# In[11]:


# Go the page with all of the AVEV entries
avev_url = 'https://elections.wi.gov/publications/statistics/absentee'
avev = session.get(avev_url)

# Captures the table with all of the AVEV entries
avev_tbl = avev.html.find('tbody', first=True)
rows = avev_tbl.find('tr')


# In[12]:


for row in rows: # loop through all of the AVEV entries
    row_title = row.find('a', first=True).text
    row_link = row.find('a', first=True).attrs['href']
    row_date = row.find('time', first=True).text
    
    if re.search(r'February 16, 2021 Spring Primary', row_title): # Checks if the entry is for Feb 2021
        avev_link = starter_url+row_link
        date = date_pattern.sub(r'\3\1\2', row_date)
        
        # Captures the table with the files
        day = session.get(avev_link)
        day_tbl = day.html.find('tbody', first=True)
        file_rows = day_tbl.find('tr')
        
        for file_row in file_rows: # Loops through the two files
            title = file_row.find('a', first=True).text
            file = file_row.find('a', first=True).attrs['href']

            if re.search(r'[c|C]ounty', title):
                #print(title)
                f = session.get(file)
                with open('scrapped_files/avev_county_{}.csv'.format(date), 'wb') as outfile:
                    outfile.write(f.content)
            elif re.search(r'[m|M]uni', title):
                #print(title)
                f = session.get(file)
                with open('scrapped_files/avev_muni_{}.csv'.format(date), 'wb') as outfile:
                    outfile.write(f.content)
            time.sleep(1)
    else: # don't want to loop through all of the AVEV entries not for Feb 2021
        break
    
    time.sleep(1)


# # Munging

# In[17]:


files = glob.glob('scrapped_files/*')


# ## Dataframe the Files

# In[32]:


avev_ctys = []
avev_munis = []

for file in files:
    file_name = re.sub('scrapped_files/','',file)
    file_name = re.sub(r'\.(csv|xlsx)','',file_name)
    features = re.split("\_", file_name)
    
    layer = features[0]
    geo = features[1]
    date = features[2]
    
    if layer == 'vr':
        if geo == 'county':
            cty = pd.read_excel(file, dtype={'CountyCode':str})
            cty.dropna(axis='columns', how='all', inplace=True)
            cty.dropna(axis='rows', how='all', inplace=True)
            cty['vr_date'] = date
        elif geo == 'muni':
            muni = pd.read_excel(file, header=1, dtype={'Hindi':str})
            muni = muni.groupby(['Hindi']).aggregate({muni.columns[-1]:'sum'})
            muni['vr_date'] = date
    else:
        if geo == 'county':
            avev_cty = pd.read_csv(file, dtype={'HINDI':str})
            avev_cty['avev_date'] = date
            
            avev_ctys.append(avev_cty)
        elif geo == 'muni':
            avev_muni = pd.read_csv(file, dtype={'HINDI':str})
            avev_muni['avev_date'] = date
            
            avev_munis.append(avev_muni)


# In[36]:


avev_ctys_df = pd.concat(avev_ctys)


# In[38]:


avev_munis_df = pd.concat(avev_munis)


# ## Join the Dataframes

# ### Counties

# In[40]:


cty.columns = ['HINDI', 'County', 'Registered Voters', 'vr_date']


# In[54]:


cty.loc[73, 'HINDI'] = '99999'


# In[47]:


cty = cty[['HINDI', 'Registered Voters', 'vr_date']]


# In[42]:


avev_ctys_df


# In[57]:


county = pd.merge(avev_ctys_df, cty, how='left', on='HINDI')


# In[64]:


county.fillna(0, inplace=True)


# In[66]:


county[['AbsenteeApplications', 'BallotsSent', 'BallotsReturned', 'InPersonAbsentee', 'Registered Voters']] = county[['AbsenteeApplications', 'BallotsSent', 'BallotsReturned', 'InPersonAbsentee', 'Registered Voters']].astype(int)


# ### Municipalities

# In[71]:


muni.reset_index(inplace=True)


# In[73]:


muni.columns = ['HINDI', 'Registered Voters', 'vr_date']


# In[83]:


muni = muni.append(cty.loc[73], ignore_index=True)


# In[85]:


munis = pd.merge(avev_munis_df, muni, how='left', on='HINDI')


# In[86]:


munis.fillna(0, inplace=True)


# In[87]:


munis[['AbsenteeApplications', 'BallotsSent', 'BallotsReturned', 'InPersonAbsentee', 'Registered Voters']] = munis[['AbsenteeApplications', 'BallotsSent', 'BallotsReturned', 'InPersonAbsentee', 'Registered Voters']].astype(int)

