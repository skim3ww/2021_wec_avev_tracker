# 2021 Spring Wisconsin Absentee Ballot Tracker

This project scrapes 2021 Spring county- and muni-level [absentee data](https://elections.wi.gov/index.php/publications/statistics/absentee) from the Wisconsin Elections Commission website. Data on the [total number of registred voters](https://elections.wi.gov/index.php/publications/statistics/registration) by county and muni is also scraped from the website, too. The registered voter population and Spring 2021 absentee statistics serve as layers for the plotly map and dashboard.

The plotly app will then be hosted on an [EC2 server](http://3.142.236.84:8050/).

## Getting Started

Create a conda environment, and install required packages
```
conda create --name wec_scrapper
conda activate wec_scrapper
pip3 install -r requirements.txt
```
BTW, I used ```Python 3.8.5``` for this project

### Packages
The requirements.txt file contains these packages:
```
appdirs                  1.4.4               
argon2-cffi              20.1.0              
async-generator          1.10                
attrs                    20.3.0              
Automat                  0.8.0               
backcall                 0.2.0               
beautifulsoup4           4.9.3               
bleach                   3.2.1               
blinker                  1.4                 
boxsdk                   2.10.0              
Brotli                   1.0.9               
bs4                      0.0.1               
cachetools               4.2.1               
certifi                  2020.12.5           
cffi                     1.14.4              
chardet                  4.0.0               
Click                    7.0                 
click-plugins            1.1.1               
cligj                    0.7.1               
cloud-init               20.4                
colorama                 0.4.3               
command-not-found        0.3                 
configobj                5.0.6               
constantly               15.1.0              
cryptography             2.8                 
cssselect                1.1.0               
cycler                   0.10.0              
dash                     1.19.0              
dash-core-components     1.15.0              
dash-html-components     1.1.2               
dash-renderer            1.9.0               
dash-table               4.11.2              
DateTime                 4.3                 
dbus-python              1.2.16              
decorator                4.4.2               
defusedxml               0.6.0               
Deprecated               1.2.10              
df2gspread               1.0.4               
distro                   1.4.0               
distro-info              0.23ubuntu1         
entrypoints              0.3                 
et-xmlfile               1.0.1               
fake-useragent           0.1.11              
Fiona                    1.8.18              
flake8                   3.7.7               
Flask                    1.1.2               
Flask-Compress           1.9.0               
future                   0.18.2              
geojson-rewind           1.0.0               
geopandas                0.9.0               
google-api-core          1.23.0              
google-api-python-client 1.6.7               
google-auth              1.26.1              
google-auth-oauthlib     0.4.2               
google-cloud-bigquery    1.21.0              
google-cloud-core        1.4.4               
google-cloud-storage     1.17.0              
google-resumable-media   0.4.1               
googleapis-common-protos 1.52.0              
gspread                  3.6.0               
httplib2                 0.19.0              
hyperlink                19.0.0              
idna                     2.10                
importlib-metadata       1.5.0               
incremental              16.10.1             
ipykernel                5.4.3               
ipython                  7.20.0              
ipython-genutils         0.2.0               
itsdangerous             1.1.0               
jedi                     0.18.0              
Jinja2                   2.10.1              
json5                    0.9.5               
jsonpatch                1.22                
jsonpointer              2.0                 
jsonschema               3.2.0               
jupyter-client           6.1.11              
jupyter-core             4.7.1               
jupyterlab               2.2.9               
jupyterlab-pygments      0.1.2               
jupyterlab-server        1.2.0               
keyring                  18.0.1              
kiwisolver               1.3.1               
language-selector        0.1                 
launchpadlib             1.10.13             
lazr.restfulclient       0.14.2              
lazr.uri                 1.0.3               
lxml                     4.6.2               
MarkupSafe               1.1.0               
matplotlib               3.3.3               
mccabe                   0.6.1               
mistune                  0.8.4               
more-itertools           4.2.0               
munch                    2.5.0               
nbclient                 0.5.1               
nbconvert                6.0.7               
nbformat                 5.0.8               
nest-asyncio             1.4.3               
netifaces                0.10.4              
notebook                 6.1.5               
numpy                    1.20.1              
oauth2client             4.1.3               
oauthlib                 3.1.0               
openpyxl                 3.0.7               
packaging                20.8                
pandas                   1.2.2               
pandocfilters            1.4.3               
parse                    1.19.0              
parso                    0.8.1               
pexpect                  4.8.0               
pickleshare              0.7.5               
Pillow                   8.1.0               
pip                      20.0.2              
plotly                   4.14.3              
prometheus-client        0.9.0               
prompt-toolkit           3.0.16              
protobuf                 3.14.0              
psycopg2-binary          2.8.5               
ptyprocess               0.6.0               
pyasn1                   0.4.8               
pyasn1-modules           0.2.8               
pycodestyle              2.5.0               
pycparser                2.20                
pyee                     8.1.0               
pyflakes                 2.1.1               
PyGithub                 1.51                
Pygments                 2.8.0               
PyGObject                3.36.0              
PyHamcrest               1.9.0               
PyJWT                    2.0.1               
pymacaroons              0.13.0              
PyNaCl                   1.3.0               
pyOpenSSL                19.0.0              
pyparsing                2.4.7               
pyppeteer                0.2.5               
pyproj                   3.0.1               
pyquery                  1.4.3               
pyrsistent               0.15.5              
pyserial                 3.4                 
python-apt               2.0.0+ubuntu0.20.4.4
python-dateutil          2.8.1               
python-debian            0.1.36ubuntu1       
pytz                     2021.1              
PyYAML                   5.3.1               
pyzmq                    22.0.3              
requests                 2.25.1              
requests-html            0.10.0              
requests-oauthlib        1.3.0               
requests-toolbelt        0.5.0               
requests-unixsocket      0.2.0               
retrying                 1.3.3               
rsa                      4.5                 
SecretStorage            2.3.1               
Send2Trash               1.5.0               
service-identity         18.1.0              
setuptools               45.2.0              
Shapely                  1.7.1               
simplejson               3.16.0              
six                      1.15.0              
sos                      4.0                 
soupsieve                2.2                 
ssh-import-id            5.10                
systemd-python           234                 
terminado                0.9.1               
testpath                 0.4.4               
tornado                  6.1                 
tqdm                     4.56.2              
traitlets                5.0.5               
Twisted                  18.9.0              
ubuntu-advantage-tools   20.3                
ufw                      0.36                
unattended-upgrades      0.1                 
uritemplate              3.0.1               
urllib3                  1.26.3              
validate-email           1.3                 
w3lib                    1.22.0              
wadllib                  1.3.3               
wcwidth                  0.2.5               
webencodings             0.5.1               
websockets               8.1                 
Werkzeug                 1.0.1               
wheel                    0.34.2              
wincertstore             0.2                 
wrapt                    1.12.1              
xlrd                     1.2.0               
xmltodict                0.11.0              
zipp                     1.0.0               
zope.interface           5.2.0               
```

### Troubleshooting
Use this to get pycairo installed:
```
sudo apt-get install libcairo2-dev libgirepository1.0-dev
```
