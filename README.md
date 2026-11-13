🎬 Movie Recommendation System

The Movie Recommendation System is a Machine Learning project that recommends movies based on the user's selected movie. It uses Content-Based Filtering to find movies with similar genres and descriptions.

The system uses Natural Language Processing (NLP) techniques, including CountVectorizer, to convert movie descriptions and genres into numerical vectors. It then applies Cosine Similarity to calculate the similarity between movies and recommend the top 5 most similar movies. 

You can run the app here- https://movie-recommender-system-em5jyzskttgqiuor546mfk.streamlit.app/

The project is developed using Python, Pandas, Scikit-learn and Streamlit. It also integrates the TMDB API to fetch and display movie posters, providing an interactive and user-friendly interface.

File Name	Description
• app.py-	Main Streamlit application that allows users to select a movie and get the top 5 similar movie recommendations with their posters using the TMDB API.

• main.py-	Python script that loads the movie dataset using Pandas and displays the dataset for basic inspection.

• Main.ipynb-	Jupyter Notebook containing the complete machine learning workflow, including data preprocessing, feature selection, CountVectorizer, Cosine Similarity and model generation.

• dataset.csv-	Contains 10,000 movie records with details such as movie ID, title, genre, overview, release date, popularity and ratings. 

• movies_list.pkl-	Pickle file that stores the processed movie dataset, including movie IDs, titles and combined text features (tags), used by the recommendation 
system. 

• Streamlit– Python framework used to create an interactive web application where users can select movies and view recommendations.

• TMDB API– Used to fetch movie details and posters from The Movie Database (TMDB) and display them in the application.

• .gitattributes– Configuration file that defines how Git handles specific files, including line-ending normalization and file type settings.


• similarity.pkl-	Stores the precomputed Cosine Similarity scores between movies, which are used to find and recommend similar movies.

• secrets.toml-	Stores the TMDB API key securely, allowing the application to fetch movie details and posters from the TMDB API.
