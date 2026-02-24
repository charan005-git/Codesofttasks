import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Step 1: Create Dataset
# -----------------------------
data = {
    "movie_title": [
        "Inception",
        "Interstellar",
        "The Dark Knight",
        "Titanic",
        "The Notebook",
        "Avengers",
        "Iron Man",
        "The Conjuring"
    ],
    "genre": [
        "Sci-Fi Thriller",
        "Sci-Fi Drama",
        "Action Crime",
        "Romance Drama",
        "Romance Drama",
        "Action Superhero",
        "Action Superhero",
        "Horror Thriller"
    ]
}

df = pd.DataFrame(data)

# -----------------------------
# Step 2: Convert Text to Numbers
# -----------------------------
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["genre"])

# -----------------------------
# Step 3: Calculate Similarity
# -----------------------------
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# -----------------------------
# Step 4: Recommendation Function
# -----------------------------
def recommend_movies(movie_name, top_n=3):
    if movie_name not in df["movie_title"].values:
        print("\n❌ Movie not found in dataset.")
        print("Available movies:")
        print(", ".join(df["movie_title"]))
        return

    idx = df[df["movie_title"] == movie_name].index[0]
    similarity_scores = list(enumerate(cosine_sim[idx]))

    # Sort by similarity score (highest first)
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    print("\n" + "="*50)
    print(f"🎬 Recommended movies for: {movie_name}")
    print("="*50)

    for i in similarity_scores[1:top_n+1]:
        print(f"⭐ {df['movie_title'][i[0]]}")

    print("="*50 + "\n")


# -----------------------------
# Step 5: Interactive Loop
# -----------------------------
if __name__ == "__main__":
    while True:
        print("\nAvailable Movies:")
        print(", ".join(df["movie_title"]))

        user_input = input("\nEnter a movie name (or type 'exit' to quit): ")

        if user_input.lower() == "exit":
            print("\n👋 Thank you for using Movie Recommendation System!")
            break

        recommend_movies(user_input)
