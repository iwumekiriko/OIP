from collections import Counter


class TFCalculator:
    def compute_tf(self, tokens: list) -> tuple[dict, Counter]:
        total = len(tokens)
        counter = Counter(tokens)

        tf = {}
        for term, count in counter.items():
            tf[term] = count / total

        return tf, counter