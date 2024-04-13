import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=c09cff17cd97fb096c1eb92b23b3cb83'.format(movie_id))
    data = response.json()

    return "https://image.tmdb.org/t/p/w92" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    num_cols = 5
    num_movies = len(names)
    cols = [st.beta_columns(num_cols)] if hasattr(st, 'beta_columns') else [st.columns(num_cols)]

    for i, name, poster in zip(range(num_movies), names, posters):
        col_index = i % num_cols
        with cols[i // num_cols][col_index]:
            st.text(name)
            st.image(poster)