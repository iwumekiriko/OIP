from collections import defaultdict, Counter


class LemmaProcessor:
    def __init__(self, lemmatizer):
        self.lemmatizer = lemmatizer

    def build_lemma_map(self, tokens):
        lemma_map = defaultdict(list)

        for token in tokens:
            lemma = self.lemmatizer.lemmatizer.lemmatize(token)
            lemma_map[lemma].append(token)

        return lemma_map

    def compute_lemma_tf(self, token_counter: Counter, lemma_map: dict, total_tokens: int):
        tf = {}

        for lemma, forms in lemma_map.items():
            count = sum(token_counter.get(form, 0) for form in forms)
            tf[lemma] = count / total_tokens

        return tf