from nltk.corpus import stopwords
import bs4
import re
import os


class Tokenizer:
    def __init__(self):
        self.stop_words = set(stopwords.words("english"))
        self.bad_tokens = {
            "html", "body", "div", "span", "href", "http",
            "https", "www", "img", "src"
        }

    def clean_html(self, html: str) -> str:
        soup = bs4.BeautifulSoup(html, "html.parser")

        for tag in soup(["script", "style"]):
            tag.decompose()

        return soup.get_text(separator=" ")
    
    def tokenize(self, text: str) -> list:
        return re.findall(r"[a-zA-Z]+", text.lower())
    
    def is_valid_token(self, token) -> bool:
        if token in self.stop_words:
            return False
        
        if len(token) < 2:
            return False
        
        if token in self.bad_tokens:
            return False
        
        return True
    
    def process_file(self, filepath: str) -> list:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()

        text = self.clean_html(html)
        tokens = self.tokenize(text)

        return [t for t in tokens if self.is_valid_token(t)]
    
    def process_directory(self, directory: str) -> list:
        all_tokens = set()

        for filename in os.listdir(directory):
            if not filename.endswith(".txt"):
                continue

            filepath = os.path.join(directory, filename)
            tokens = self.process_file(filepath)

            all_tokens.update(tokens)

        return sorted(all_tokens)
    
    def save_tokens(self, tokens: list, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            for token in tokens:
                f.write(token + "\n")
