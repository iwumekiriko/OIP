import os
import math
from config import TFIDF_DIR


class VectorIndex:
    def __init__(self):
        self.documents = {}
        self.doc_norms = {}
        self.idf = {}

    def load(self):
        for filename in os.listdir(TFIDF_DIR):
            if not filename.endswith(".txt"):
                continue

            doc_id = int(filename.split(".")[0])
            path = os.path.join(TFIDF_DIR, filename)

            vector = {}

            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    term, idf, tfidf = line.strip().split()
                    vector[term] = float(tfidf)
                    self.idf[term] = float(idf)

            self.documents[doc_id] = vector

        for doc_id, vec in self.documents.items():
            self.doc_norms[doc_id] = math.sqrt(sum(v*v for v in vec.values()))