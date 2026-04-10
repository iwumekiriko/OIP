class DocumentProcessor:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def process_document(self, filepath: str) -> list:
        tokens = self.tokenizer.process_file(filepath)
        return tokens