import pickle
import numpy as np
import streamlit as st
import requests

st.header("Movies Recommendation System Using Machine Learning")
movies = pickle.load(open('artifact/movie_list.pkl','rb'))
similarity = np.load("artifact/similarity.npz", allow_pickle=True)["similarity"]

movie_list=movies['title'].values
selected_movie=st.selectbox(
    'Type or select a movie to get a recommendation',
    movie_list
)
def fetch_poster(movie_id):    
        url = "https://api.themoviedb.org/3/movie/{}?api_key=abbecff06143390eb77e67d14a5392f4".format(movie_id)
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        data=response.json()
        poster_path=data['poster_path']
        full_path='http://image.tmdb.org/t/p/w500/'+poster_path
        return full_path

def recommend(movie):
    index=movies[movies['title']==movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])
    recommended_movies_name=[]
    recommended_movies_poster=[]
    for i in distances[1:6]:
        movie_id=movies.iloc[i[0]]['id']
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)
    return recommended_movies_name,recommended_movies_poster

recommended_movies_name,recommended_movies_poster=recommend(selected_movie)
col1,col2,col3,col4,col5=st.columns(5)
with col1:
    st.image(recommended_movies_poster[0])
    st.text(recommended_movies_name[0])
with col2:
    st.image(recommended_movies_poster[1])
    st.text(recommended_movies_name[1])
with col3:
    st.image(recommended_movies_poster[2])
    st.text(recommended_movies_name[2])
with col4:
    st.image(recommended_movies_poster[3])
    st.text(recommended_movies_name[3])
with col5:
    st.image(recommended_movies_poster[4])
    st.text(recommended_movies_name[4])
