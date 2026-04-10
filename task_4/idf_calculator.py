import math
from collections import defaultdict


class IDFCalculator:
    def compute_idf(self, documents_tokens: dict) -> dict:
        N = len(documents_tokens)
        df = defaultdict(int)

        for tokens in documents_tokens.values():
            unique_terms = set(tokens)
            for term in unique_terms:
                df[term] += 1

        idf = {}
        for term, freq in df.items():
            idf[term] = math.log(N / freq)

        return idf