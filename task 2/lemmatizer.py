from nltk.stem import WordNetLemmatizer
from collections import defaultdict


class Lemmatizer:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def build_lemma_dict(self, tokens: list) -> dict:
        lemma_dict = defaultdict(set)

        for token in tokens:
            lemma = self.lemmatizer.lemmatize(token)
            lemma_dict[lemma].add(token)

        return lemma_dict
    
    def save_lemmas(self, lemma_dict: dict, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            for lemma in sorted(lemma_dict.keys()):
                tokens = sorted(lemma_dict[lemma])
                line = lemma + " " + " ".join(tokens)
                f.write(line + "\n")