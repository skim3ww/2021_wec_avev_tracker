#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
import datetime
import glob
import re 
import os
import time
from csv import reader

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
# I'm scraping all of the Voter Registration Statistics table rows and putting the date, title, and link into 
# the vr_tbl.csv file. I'm going to use the file to loop through the links to get to the files.

from requests_html import HTML, HTMLSession
import csv
import urllib

# Go to https://elections.wi.gov/index.php/publications/statistics/registration
session = HTMLSession()
r = session.get('https://elections.wi.gov/index.php/publications/statistics/registration')

# Capture the table of Registered Voter Population Statistics over the past
table = r.html.find('tbody', first=True)
rows = table.find('tr')

# Capture the most recent, top entry
most_recent_date = rows[0].find('time', first=True).text
most_recent = rows[0].find('a', first=True).attrs['href']

# ### Get County and Wards Files

# stores url to get to the page with the files
starter_url = 'https://elections.wi.gov'
url = starter_url + most_recent

# turns American style date to normal dates like this: 20210301
date_pattern = re.compile(r'(\d{2})/(\d{2})/(\d{4})')
date = date_pattern.sub(r'\3\1\2', most_recent_date)

# Captures the tables with the files
month = session.get(url)
table = month.html.find('tbody', first=True)
file_rows = table.find('tr')

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
# Go the page with all of the AVEV entries
avev_url = 'https://elections.wi.gov/publications/statistics/absentee'
avev = session.get(avev_url)

# Captures the table with all of the AVEV entries
avev_tbl = avev.html.find('tbody', first=True)
rows = avev_tbl.find('tr')

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
files = glob.glob('scrapped_files/*')

# ## Dataframe the Files
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

avev_ctys_df = pd.concat(avev_ctys)
avev_munis_df = pd.concat(avev_munis)

# ## Join the Dataframes

# ### Counties
cty.columns = ['HINDI', 'County', 'Registered Voters', 'vr_date']
cty.loc[73, 'HINDI'] = '99999'
cty = cty[['HINDI', 'Registered Voters', 'vr_date']]

county = pd.merge(avev_ctys_df, cty, how='left', on='HINDI')

county.fillna(0, inplace=True)
county[['AbsenteeApplications', 'BallotsSent', 'BallotsReturned', 'InPersonAbsentee', 'Registered Voters']] = county[['AbsenteeApplications', 'BallotsSent', 'BallotsReturned', 'InPersonAbsentee', 'Registered Voters']].astype(int)

county['HINDI'] = county['HINDI'].astype(int)

# ### Municipalities
muni.reset_index(inplace=True)
muni.columns = ['HINDI', 'Registered Voters', 'vr_date']
muni = muni.append(cty.loc[73], ignore_index=True)

munis = pd.merge(avev_munis_df, muni, how='left', on='HINDI')
munis.fillna(0, inplace=True)
munis[['AbsenteeApplications', 'BallotsSent', 'BallotsReturned', 'InPersonAbsentee', 'Registered Voters']] = munis[['AbsenteeApplications', 'BallotsSent', 'BallotsReturned', 'InPersonAbsentee', 'Registered Voters']].astype(int)

# ------------------------------------------------------------------------------------------------------------------------------------
# Getting Shapes
import geopandas as gpd
from urllib.request import urlopen
import json
with urlopen('https://opendata.arcgis.com/datasets/8b8a0896378449538cf1138a969afbc6_3.geojson') as response:
    counties = json.load(response)

from geojson_rewind import rewind
counties = rewind(counties, rfc7946=False)

#counties = gpd.read_file(counties)

#counties = json.loads(counties.to_json())
#counties['features'] = [f for f in counties['features'] if f['properties']['STATE'] == '55']
#print(counties['features'][0])

# ------------------------------------------------------------------------------------------------------------------------------------
# Visualize the Data
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
## App layout
app.layout = html.Div([

    html.H1('February 2021 Primaries Absentee Voting', style={'text-align':'center'}),

    dcc.Dropdown(
        id='date',
        options=[
            {'label': '2021-01-27', 'value':'20210127'}, 
            {'label': '2021-01-28', 'value':'20210128'}, 
            {'label': '2021-01-29', 'value':'20210129'}, 
            {'label': '2021-02-01', 'value':'20210201'}, 
            {'label': '2021-02-03', 'value':'20210203'}, 
            {'label': '2021-02-08', 'value':'20210208'}, 
            {'label': '2021-02-15', 'value':'20210215'}, 
            {'label': '2021-02-16', 'value':'20210216'}, 
            {'label': '2021-02-18', 'value':'20210218'}
        ],
        multi=False,
        value='20210218',
        style={'width': '40%'}
    ),

    html.Div(id='output_container'),
    html.Br(),

    dcc.Graph(id='wi_map')
])
# --------------------------------------------------------------------------------------------------------------
## Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='wi_map', component_property='figure')
    ],
    [Input(component_id='date', component_property='value')]
)

def update_graph(option_day):
    print(option_day)
    print(type(option_day))

    container = 'Absentee ballots on {}'.format(option_day)

    cdf = county[:-1].copy()
    cdf = cdf.loc[cdf['avev_date'] == option_day]

    # Plotly Express
    fig = px.choropleth(
        data_frame=cdf,
        geojson=counties,
        #locationmode='USA-states',
        locations='HINDI',
        featureidkey='properties.DNR_CNTY_CODE',
        scope='usa', 
        color='AbsenteeApplications',
        hover_data = ['Jurisdiction', 'Registered Voters','AbsenteeApplications', 'BallotsSent', 'BallotsReturned', 'InPersonAbsentee'],
        color_continuous_scale='emrld'
    )

    fig.update_geos(fitbounds='locations', visible=False)


    return container, fig



# --------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)