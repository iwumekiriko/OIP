from nltk.stem import WordNetLemmatizer


class LemmaCache:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.cache = {}

    def get(self, token):
        if token not in self.cache:
            self.cache[token] = self.lemmatizer.lemmatize(token)
        return self.cache[token]