from flask import Flask, render_template, request
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load jobs
jobs = pd.read_csv("jobs.csv")

jobs["title"] = jobs["title"].fillna("").astype(str)
jobs["skills"] = jobs["skills"].fillna("").astype(str)

jobs = jobs[
    (jobs["title"] != "") &
    (jobs["skills"] != "")
]


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        candidate_skills = request.form["skills"]

        # TF-IDF Recommendation Engine
        vectorizer = TfidfVectorizer()

        documents = [candidate_skills] + jobs["skills"].tolist()

        tfidf_matrix = vectorizer.fit_transform(documents)

        candidate_vector = tfidf_matrix[0]

        job_vectors = tfidf_matrix[1:]

        similarity_scores = cosine_similarity(
            candidate_vector,
            job_vectors
        )

        results = jobs.copy()

        results["similarity"] = similarity_scores[0]

        # Skill Gap Analysis
        candidate_set = set(
            candidate_skills.lower().split()
        )

        missing_skills_list = []

        course_map = {

            "restapi":
                "REST API Development",

            "tensorflow":
                "TensorFlow Fundamentals",

            "machinelearning":
                "Machine Learning Basics",

            "react":
                "React Frontend Development",

            "powerbi":
                "Microsoft Power BI",

            "statistics":
                "Statistics for Data Science",

            "linux":
                "Linux Administration",

            "networking":
                "Computer Networking Fundamentals"

            }

        for _, row in results.iterrows():

            job_set = set(
                row["skills"].lower().split()
            )

            matched = candidate_set.intersection(job_set)

            missing = job_set - candidate_set

            recommended_courses = []

            for skill in missing:

                if skill in course_map:

                    recommended_courses.append(
                        course_map[skill]
                )

            match_percentage = (
                len(matched) /
                len(job_set)
            ) * 100

            missing_skills_list.append({

                "title": row["title"],

                "skills": row["skills"],

                "similarity": row["similarity"],

                "matched": sorted(list(matched)),

                "missing": sorted(list(missing)),

                "match_percentage": round(match_percentage, 2),

                "courses": recommended_courses

                })

        missing_skills_list = sorted(
            missing_skills_list,
            key=lambda x: x["similarity"],
            reverse=True
        )

        # Keep only top 5 matches
        missing_skills_list = missing_skills_list[:5]

        return render_template(
            "results.html",
            jobs=missing_skills_list
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
