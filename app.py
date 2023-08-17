import streamlit as st
import pandas as pd
import pickle
import requests

movies_list = pd.read_pickle('movies.pkl')
movies = movies_list['title'].values
similarity_vector = pickle.load(open('distance_vector.pkl', 'rb'))


def recommend(movie):
    movie_index = movies_list[movies_list["title"] == movie].index[0]
    distance_vector = similarity_vector[movie_index]
    recommendations = sorted(list(enumerate(distance_vector)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_id = []
    for i in recommendations:
        recommended_movies.append(movies_list.iloc[i[0]].title)
        recommended_movies_id.append(movies_list.iloc[i[0]].id)

    return [recommended_movies, recommended_movies_id]


def fetch_url(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}'
                            f'?api_key=b6d2ade90063da4be231a4b5a5fff0cb&language=en-US')
    data = response.json()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


st.title("Movie Recommender System")
selected_movie = st.selectbox('Select the movie to get similar recommendations.', movies)

if st.button("Select"):
    recommended_list = recommend(selected_movie)
    # st.write(recommended_list)
    cols = st.columns(5, gap='large')
    for i in range(5):
        name = recommended_list[0][i]
        poster_url = fetch_url(recommended_list[1][i])
        with cols[i]:
            st.write(name)
            st.image(poster_url)
