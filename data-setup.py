import urllib.request
import os.path
import gzip
import pandas as pd
from bs4 import BeautifulSoup

# the beautifulsoup4 library should be installed before running this script

# URL to check for the dataset link
DATASET_URL = 'https://datasets.imdbws.com/'

# target dataset link to download
TARGETS = ['title.basics.tsv.gz', 'title.ratings.tsv.gz']

for target in TARGETS:
    if os.path.isfile(target[:target.rfind('.')]):
        continue

    # get html from webpage with dataset files
    with urllib.request.urlopen(DATASET_URL) as f:
        html = f.read()

    # create BeautifulSoup object for parsing
    soup = BeautifulSoup(html,features='html.parser')

    # find target file to download
    download_link = ''
    for link in soup.find_all('a'):
        link_check = link.get('href')
        if target in link_check:
            print(f'downloading file: {target}')
            break

    urllib.request.urlretrieve(DATASET_URL + target, target)
    print('unzipping...')
    unzipped_file = gzip.open(target)
    df = pd.read_csv(target, sep='\t', header=0)
    df = df.replace('\\N', None)
    if 'isAdult' in df.columns:
        df['isAdult'] = df['isAdult'].replace(['0'],False)
        df['isAdult'] = df['isAdult'].replace(['1'],True)
    print(f'saving {target} as file...')
    # save tsv file
    df.to_csv(target[:target.rfind('.')], sep='\t', index=False)
    # TODO remove this section when testing is complete
    df.head(100).to_csv(target[:target.find('.tsv')] + "_100.tsv", sep='\t', index=False)
    df.head(1000).to_csv(target[:target.find('.tsv')] + "_1000.tsv", sep='\t', index=False)
    df.head(10000).to_csv(target[:target.find('.tsv')] + "_10000.tsv", sep='\t', index=False)
    # remove downloaded file
    os.remove(target)
    print(df)