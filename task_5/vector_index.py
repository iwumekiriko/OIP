import os
import math


class VectorIndex:
    def __init__(self):
        self.documents = {}
        self.doc_norms = {}
        self.idf = {}

    def load(self, directory: str) -> None:
        print("Loading TF-IDF...")

        for filename in os.listdir(directory):
            if not filename.endswith(".txt"):
                continue

            doc_id = int(filename.split(".")[0])
            filepath = os.path.join(directory, filename)

            vector = {}

            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    term, idf, tfidf = line.strip().split()
                    vector[term] = float(tfidf)
                    self.idf[term] = float(idf)

            self.documents[doc_id] = vector

        for doc_id, vec in self.documents.items():
            norm = math.sqrt(sum(v * v for v in vec.values()))
            self.doc_norms[doc_id] = norm

        print(f"Loaded {len(self.documents)} documents")