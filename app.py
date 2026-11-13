import os
import pickle
from pathlib import Path

import requests
import streamlit as st

st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬", layout="wide")

BASE_DIR = Path(__file__).resolve().parent
MOVIES_FILE = BASE_DIR / "movies_list.pkl"
SIMILARITY_FILE = BASE_DIR / "similarity.pkl"
TMDB_API = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
PLACEHOLDER = "https://placehold.co/500x750/20242c/ffffff?text=Poster+Unavailable"

# Load key from secrets/environment; sidebar also allows manual entry.
try:
    saved_key = st.secrets.get("TMDB_API_KEY", "")
except Exception:
    saved_key = ""
saved_key = saved_key or os.getenv("TMDB_API_KEY", "")

with st.sidebar:
    st.header("Project diagnostics")
    manual_key = st.text_input(
        "TMDB API Key (v3 auth)",
        type="password",
        help="Paste the short API Key (v3 auth), not the long API Read Access Token.",
    )

api_key = manual_key.strip() or saved_key

st.markdown("""
<style>
.stApp {background:linear-gradient(135deg,#10131b 0%,#191d29 100%);}
.main-title {text-align:center;font-size:2.5rem;font-weight:800;}
.sub-title {text-align:center;color:#b8c0d4;margin-bottom:1.5rem;}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="main-title">🎬 Movie Recommendation System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Discover your next favourite movie.</div>', unsafe_allow_html=True)

@st.cache_resource
def load_data(movie_file, similarity_file):
    with open(movie_file, "rb") as f:
        movie_data = pickle.load(f)
    with open(similarity_file, "rb") as f:
        similarity_data = pickle.load(f)
    return movie_data, similarity_data

if not MOVIES_FILE.exists() or not SIMILARITY_FILE.exists():
    st.error("movies_list.pkl or similarity.pkl is missing. Keep both beside app.py.")
    st.stop()

try:
    movies, similarity = load_data(str(MOVIES_FILE), str(SIMILARITY_FILE))
except Exception as exc:
    st.error("Could not load pickle files.")
    st.code(str(exc))
    st.stop()

if not hasattr(movies, "columns") or not {"title", "id"}.issubset(movies.columns):
    st.error("movies_list.pkl must contain 'title' and 'id' columns.")
    st.stop()
if len(movies) != len(similarity):
    st.error("movies_list.pkl and similarity.pkl do not match. Regenerate them together using main.py.")
    st.stop()

titles = movies["title"].dropna().astype(str).drop_duplicates().tolist()
if not titles:
    st.error("No movie titles found in movies_list.pkl.")
    st.stop()

def tmdb_details(movie_id, key):
    if not key:
        return None, "API key missing. Paste TMDB API Key (v3 auth) in the sidebar."
    try:
        response = requests.get(
            f"{TMDB_API}/movie/{int(float(movie_id))}",
            params={"api_key": key, "language": "en-US"},
            timeout=15,
        )
        if response.status_code == 401:
            return None, "TMDB 401: API key invalid. Check API Key (v3 auth)."
        if response.status_code == 404:
            return None, f"TMDB 404: movie ID {movie_id} not found."
        if response.status_code == 429:
            return None, "TMDB rate limit reached. Wait and retry."
        response.raise_for_status()
        return response.json(), None
    except (ValueError, TypeError):
        return None, f"Invalid movie ID: {movie_id}"
    except requests.RequestException as exc:
        return None, f"Network/API error: {exc}"

@st.cache_data(ttl=3600, show_spinner=False)
def poster_for(movie_id, key):
    details, error = tmdb_details(movie_id, key)
    if error:
        return None, error
    path = details.get("poster_path")
    if not path:
        return None, "TMDB has no poster for this movie."
    return IMAGE_BASE + path, None

def show_poster(movie_id, key):
    url, error = poster_for(movie_id, key)
    if url:
        st.image(url, use_container_width=True)
    else:
        st.image(PLACEHOLDER, use_container_width=True)
        with st.expander("Why is this poster missing?"):
            st.caption(error)

def recommend(title, count=5):
    found = movies.index[movies["title"].astype(str) == title].tolist()
    if not found:
        return []
    movie_index = found[0]
    ranked = sorted(enumerate(similarity[movie_index]), key=lambda x: x[1], reverse=True)
    output = []
    for index, score in ranked:
        if index == movie_index:
            continue
        row = movies.iloc[index]
        output.append({"title": str(row["title"]), "id": row["id"]})
        if len(output) >= count:
            break
    return output

with st.sidebar:
    if api_key:
        st.success("TMDB API key available")
    else:
        st.error("TMDB API key NOT loaded")
        st.caption("Paste your short API Key (v3 auth) in the field above.")
    if st.button("Test TMDB connection", use_container_width=True):
        data, error = tmdb_details(550, api_key)
        if data:
            st.success("TMDB connection successful!")
            st.write("Test movie:", data.get("title", "Fight Club"))
            if data.get("poster_path"):
                st.image(IMAGE_BASE + data["poster_path"], use_container_width=True)
        else:
            st.error(error)
    if st.button("Clear poster cache", use_container_width=True):
        st.cache_data.clear()
        st.success("Poster cache cleared.")

st.divider()
selected = st.selectbox("Choose a movie", titles)
if st.button("✨ Show Recommendations", type="primary", use_container_width=True):
    results = recommend(selected, 5)
    if not results:
        st.error("No recommendations found. Check similarity.pkl.")
    else:
        st.subheader(f"Movies similar to {selected}")
        cols = st.columns(5)
        for col, movie in zip(cols, results):
            with col:
                show_poster(movie["id"], api_key)
                st.markdown(f"**{movie['title']}**")

st.divider()
st.caption("Academic project | Python • Streamlit • Content-based filtering • TMDB")
