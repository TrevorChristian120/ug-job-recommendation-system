from flask import Flask, render_template, request
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load jobs once when application starts
jobs = pd.read_csv("jobs.csv")

# Remove rows missing title or skills
jobs = jobs.dropna(subset=["title", "skills"])


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        candidate_skills = request.form["skills"]

        # Create vectorizer
        vectorizer = TfidfVectorizer()

        # Candidate + jobs
        documents = [candidate_skills] + jobs["skills"].tolist()

        print("\nDOCUMENTS BEING SENT TO TF-IDF:\n")

        for i, doc in enumerate(documents):
            print(f"{i}: {repr(doc)} ({type(doc)})")

        # Convert text into vectors
        tfidf_matrix = vectorizer.fit_transform(documents)

        # Candidate vector
        candidate_vector = tfidf_matrix[0]

        # All job vectors
        job_vectors = tfidf_matrix[1:]

        # Calculate similarity
        scores = cosine_similarity(
            candidate_vector,
            job_vectors
        )

        # Create copy so we don't permanently modify dataframe
        results = jobs.copy()

        results["similarity"] = scores[0]

        top_jobs = results.sort_values(
            by="similarity",
            ascending=False
        )

        return render_template(
            "results.html",
            jobs=top_jobs.to_dict(orient="records")
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)