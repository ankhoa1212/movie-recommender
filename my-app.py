import streamlit as st
import pandas as pd
import random
from sklearn.neighbors import NearestNeighbors

# TODO use entire dataset once testing is complete
targets = ['title.basics_1000.tsv', 'title.ratings_1000.tsv']
search_title = ''
user_ratings = []
recommendations = []
ind_to_id_dict = {}

def get_recommendations(index):
    recommendations = []
    knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10, n_jobs=-1)
    
    matrix = df.drop('tconst', axis=1)
    knn.fit(matrix)
    if index == -1:
        z = random.randrange(0, len(df))
        st.write(f'Showing recommendations based on "{ind_to_title(z)}":')
        x = matrix[z:z+1]
    else:
        st.write(f'Showing recommendations based on "{search_title}":')
        x = matrix[index:index+1]
    _, indices = knn.kneighbors(x, n_neighbors=num_recommendations + 1)
    for i in range(1, indices.size):
        ind = indices[0][i]
        recommendations.append(ind_to_id_dict[ind])

    for i, r in enumerate(recommendations):
        rec = df2['primaryTitle'].loc[df['tconst'] == r]
        rec_str = str(i + 1) + ". " + rec.to_string(index=False)
        rec_str

def ind_to_title(i):
    return df2['primaryTitle'].iloc[i]

st.title("Basic Movie Recommendation")
st.write("uses data from imdb non-commercial database at https://datasets.imdbws.com/")
df = pd.read_csv(targets[1], sep='\t', header=0, low_memory=False)
df2 = pd.read_csv(targets[0], sep='\t', header=0, low_memory=False)
display = df2.drop(['tconst','titleType', 'originalTitle'], axis=1)
display
for ind, id in enumerate(df2['tconst']):
    ind_to_id_dict[ind] = id
# TODO add extra col data
for col in ['isAdult', 'startYear']:
    df.insert(len(df.columns), col, df2[col])
num_recommendations = st.slider("Number of recommendations to show:", min_value=1, value=5, max_value=len(df), step=1)
if st.button('Get Random Recommendations'):
    get_recommendations(-1)
col1, col2 = st.columns(2)
with col1:
    search_title = st.text_input('Enter a movie title in the text box below, then click "Search"', value='')
with col2:
    if st.button('Search'):
        search_title_found = -1
        for i, item in enumerate(list(df2['primaryTitle'])):
            if search_title == item:
                search_title_found = i
                break
        if search_title_found == -1:
            st.write(f'"{search_title}" not found. Try checking for spelling or search for a different title.')
            search_title = ''
        else:
            get_recommendations(i)
        
