import urllib.request
import os.path
import gzip
import pandas as pd
from bs4 import BeautifulSoup

# beautifulsoup4 

DATASET_URL = 'https://datasets.imdbws.com/'
TARGET = 'title.basics.tsv.gz'

if not os.path.isfile(TARGET[:TARGET.rfind('.')]):
    exit()

# get html from webpage with dataset files
with urllib.request.urlopen(DATASET_URL) as f:
    html = f.read()

# create BeautifulSoup object for parsing
soup = BeautifulSoup(html,features='html.parser')

# find target file to download
download_link = ''
for link in soup.find_all('a'):
    link_check = link.get('href')
    if TARGET in link_check:
        print(f'downloading file: {TARGET}')
        break

urllib.request.urlretrieve(DATASET_URL + TARGET, TARGET)
print('unzipping...')
unzipped_file = gzip.open(TARGET)
df = pd.read_csv(TARGET, sep='\t', header=0)
df['endYear'] = df['endYear'].replace(['\\N'],None)
df['runtimeMinutes'] = df['runtimeMinutes'].replace(['\\N'],None)
df['isAdult'] = df['isAdult'].replace(['0'],False)
df['isAdult'] = df['isAdult'].replace(['1'],True)
print(f'saving {TARGET} as file...')
# save tsv file
df.to_csv(TARGET[:TARGET.rfind('.')], sep='\t', index=False)
df.head(100).to_csv(TARGET[:TARGET.rfind('.')] + "_100", sep='\t', index=False)
df.head(1000).to_csv(TARGET[:TARGET.rfind('.')] + "_1000", sep='\t', index=False)
df.head(10000).to_csv(TARGET[:TARGET.rfind('.')] + "_10000", sep='\t', index=False)
# remove downloaded file
os.remove(TARGET)
print(df)