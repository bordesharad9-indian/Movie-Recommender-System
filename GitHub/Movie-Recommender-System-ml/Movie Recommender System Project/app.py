import pickle
import streamlit as st
import requests
import pandas as pd

API_KEY = "8265bd1679663a7ea12ac168da84d2e8"
BASE_URL = "https://api.themoviedb.org/3/movie/"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

headers = {
    "accept": "application/json"
}

def fetch_poster(movie_id):
    try:
        url = f"{BASE_URL}{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code != 200:
            return None

        data = response.json()
        poster_path = data.get("poster_path")

        if poster_path is None:
            return None

        return IMAGE_BASE_URL + poster_path

    except requests.exceptions.RequestException:
        return None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters

st.set_page_config(page_title="Movie Recommender", layout="wide")
st.header("Movie Recommender System")

movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))


movie_list = movies["title"].values

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button("Show Recommendation"):
    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    for col, name, poster in zip(
        [col1, col2, col3, col4, col5],
        names,
        posters
    ):
        with col:
            st.text(name)
            if poster:
                st.image(poster)
            else:
                st.warning("Poster not available")
