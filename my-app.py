import streamlit as st
import pandas as pd

# TODO use entire dataset once testing is complete
TARGET = 'title.basics.tsv_10000'
num_recommendations = 3

watch_list = ['tt0010034']
recommendations = []

st.title("Movie Recommendation System")

st.write("*uses data from imdb non-commercial database*")
df = pd.read_csv(TARGET, sep='\t', header=0, low_memory=False)
st.dataframe(df)
if st.button('Get Random Recommendations'):
    # TODO make recommendations using k-means clustering
    # randomize recommendations for now
    recommendations = df.sample(n=num_recommendations)['tconst']
    for r in recommendations:
        rec = df['primaryTitle'].loc[df['tconst'] == r]
        rec_str = rec.to_string(index=False)
        rec_str
