import os


class ResultWriter:
    def __init__(self, output_dir: str) -> None:
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def write(self, doc_id: int, data: dict) -> None:
        filepath = os.path.join(self.output_dir, f"{doc_id}.txt")

        with open(filepath, "w", encoding="utf-8") as f:
            for term, (idf, tfidf) in sorted(data.items()):
                f.write(f"{term} {idf:.6f} {tfidf:.6f}\n")