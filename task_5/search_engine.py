import math
from vector_index import VectorIndex
from collections import Counter


class SearchEngine:
    def __init__(self, index: VectorIndex):
        self.index = index

    def vectorize(self, query):
        tokens = [w.lower() for w in query.split() if w.isalpha()]
        total = len(tokens)

        counter = Counter(tokens)

        vec = {}
        for t, c in counter.items():
            tf = c / total
            idf = self.index.idf.get(t, 0)
            vec[t] = tf * idf

        return vec

    def cosine(self, q, d, d_norm) -> float:
        dot = 0
        for t in q:
            if t in d:
                dot += q[t] * d[t]

        q_norm = math.sqrt(sum(v*v for v in q.values()))

        if q_norm == 0 or d_norm == 0:
            return 0

        return dot / (q_norm * d_norm)

    def search(self, query: str) -> list:
        q_vec = self.vectorize(query)

        results = []

        for doc_id, d_vec in self.index.documents.items():
            score = self.cosine(q_vec, d_vec, self.index.doc_norms[doc_id])
            if score > 0:
                results.append((doc_id, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:10]