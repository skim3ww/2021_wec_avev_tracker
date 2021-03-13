# 2021 Spring Wisconsin Absentee Ballot Tracker

This project scrapes 2021 Spring county- and muni-level absentee data from the Wisconsin Elections Commission website. Data on the total number of registred voters by county and muni is also scraped from the website, too. The registered voter population and Spring 2021 absentee statistics serve as layers for the plotly map and dashboard.

The plotly app will then be hosted on an EC2 server.

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
appdirs==1.4.4
attrs==20.3.0
backcall==0.2.0
beautifulsoup4==4.9.3
boxsdk==2.10.0
bs4==0.0.1
cachetools==4.2.1
certifi==2020.12.5
chardet==4.0.0
colorama==0.4.3
cssselect==1.1.0
DateTime==4.3
decorator==4.4.2
Deprecated==1.2.10
df2gspread==1.0.4
fake-useragent==0.1.11
flake8==3.7.7
google-api-core==1.23.0
google-api-python-client==1.6.7
google-auth==1.26.1
google-auth-oauthlib==0.4.2
google-cloud-bigquery==1.21.0
google-cloud-core==1.4.4
google-cloud-storage==1.17.0
google-resumable-media==0.4.1
googleapis-common-protos==1.52.0
gspread==3.6.0
httplib2==0.19.0
idna==2.10
ipykernel==5.4.3
ipython==7.20.0
ipython-genutils==0.2.0
jedi==0.18.0
jupyter-client==6.1.11
jupyter-core==4.7.1
lxml==4.6.2
numpy==1.20.1
oauth2client==4.1.3
oauthlib==3.1.0
pandas==1.2.2
parse==1.19.0
parso==0.8.1
pickleshare==0.7.5
prompt-toolkit==3.0.16
protobuf==3.14.0
psycopg2-binary==2.8.5
pyasn1==0.4.8
pyasn1-modules==0.2.8
pycodestyle==2.5.0
pyee==8.1.0
pyflakes==2.1.1
PyGithub==1.51
Pygments==2.8.0
PyJWT==2.0.1
pyparsing==2.4.7
pyppeteer==0.2.5
pyquery==1.4.3
python-dateutil==2.8.1
pytz==2021.1
pyzmq==22.0.3
requests==2.25.1
requests-html==0.10.0
requests-oauthlib==1.3.0
requests-toolbelt==0.5.0
rsa==4.5
six==1.15.0
soupsieve==2.2
tornado==6.1
tqdm==4.56.2
traitlets==5.0.5
uritemplate==3.0.1
urllib3==1.26.3
validate-email==1.3
w3lib==1.22.0
wcwidth==0.2.5
websockets==8.1
wincertstore==0.2
wrapt==1.12.1
xmltodict==0.11.0
zope.interface==5.2.0
```

