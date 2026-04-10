class TFIDFCalculator:
    def compute(self, tf: dict, idf: dict) -> dict:
        tfidf = {}
        for term in tf:
            tfidf[term] = tf[term] * idf.get(term, 0)
        return tfidf