from collections import defaultdict
import os


class InvertedIndex:
    def __init__(self, tokenizer) -> None:
        self.index = defaultdict(set)
        self.documents = set()
        self.tokenizer = tokenizer

    def build(self, directory: str) -> None:
        for filename in os.listdir(directory):
            if not filename.endswith(".txt"):
                continue

            doc_id = int(filename.split(".")[0])
            self.documents.add(doc_id)

            filepath = os.path.join(directory, filename)
            tokens = set(self.tokenizer.process_file(filepath))

            for token in tokens:
                self.index[token].add(doc_id)

    def save(self, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            for term in sorted(self.index.keys()):
                docs = sorted(self.index[term])
                line = term + " " + " ".join(map(str, docs))
                f.write(line + "\n")

    def get_docs(self, term) -> set:
        return self.index.get(term, set())