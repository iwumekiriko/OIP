class DocumentMapper:
    def __init__(self, filepath):
        self.map = {}
        self.load(filepath)

    def load(self, filepath: str) -> None:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                doc_id, url = line.strip().split(maxsplit=1)
                self.map[int(doc_id)] = url

    def get_url(self, doc_id: int) -> str:
        return self.map.get(doc_id, "#")