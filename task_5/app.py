from flask import Flask, render_template, request
from search_engine import VectorIndex, SearchEngine

app = Flask(__name__)

index = VectorIndex()
index.load()

engine = SearchEngine(index)


@app.route("/", methods=["GET", "POST"])
def home():
    results = []

    if request.method == "POST":
        query = request.form.get("query")
        results = engine.search(query) # type: ignore

    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)