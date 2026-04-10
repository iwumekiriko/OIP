from flask import Flask, render_template, request
from search_engine import VectorIndex, SearchEngine
from document_mapper import DocumentMapper
from config import DOCS_DIR

mapper = DocumentMapper(DOCS_DIR)

app = Flask(__name__)

index = VectorIndex()
index.load()

engine = SearchEngine(index)


@app.route("/", methods=["GET", "POST"])
def home():
    results = []

    if request.method == "POST":
        query = request.form.get("query")
        raw_results = engine.search(query) # type: ignore

        results = [
            {
                "url": mapper.get_url(doc_id),
                "score": score
            }
            for doc_id, score in raw_results
        ]

    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)