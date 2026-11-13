🎬 Movie Recommendation System
The Movie Recommendation System is a Machine Learning project that recommends movies based on the user's selected movie. It uses Content-Based Filtering to find movies with similar genres and descriptions.

The system uses Natural Language Processing (NLP) techniques, including CountVectorizer, to convert movie descriptions and genres into numerical vectors. It then applies Cosine Similarity to calculate the similarity between movies and recommend the top 5 most similar movies. 
You can run the app here- 

The project is developed using Python, Pandas, Scikit-learn and Streamlit. It also integrates the TMDB API to fetch and display movie posters, providing an interactive and user-friendly interface.
Project Files Description
File Name	Description
app.py	Main Streamlit application that allows users to select a movie and get the top 5 similar movie recommendations with their posters using the TMDB API.
main.py	Python script that loads the movie dataset using Pandas and displays the dataset for basic inspection.
Main.ipynb	Jupyter Notebook containing the complete machine learning workflow, including data preprocessing, feature selection, CountVectorizer, Cosine Similarity and model generation.
dataset.csv	Contains 10,000 movie records with details such as movie ID, title, genre, overview, release date, popularity and ratings.
movies_list.pkl	Pickle file that stores the processed movie dataset, including movie IDs, titles and combined text features (tags), used by the recommendation system.
similarity.pkl	Stores the precomputed Cosine Similarity scores between movies, which are used to find and recommend similar movies.
secrets.toml	Stores the TMDB API key securely, allowing the application to fetch movie details and posters from the TMDB API.
