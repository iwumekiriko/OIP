import os
import math
import sys
from collections import defaultdict, Counter

sys.path.append(os.path.abspath(".."))

from task_2.tokenizer import Tokenizer
from task_2.lemmatizer import Lemmatizer

from lemma_cache import LemmaCache
from result_writer import ResultWriter

from config import *


class TFIDFPipeline:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.lemma_cache = LemmaCache()

        self.token_writer = ResultWriter(TOKENS_OUT)
        self.lemma_writer = ResultWriter(LEMMAS_OUT)

    def run(self):
        documents_tokens = {}
        documents_lemmas = {}

        token_df = defaultdict(int)
        lemma_df = defaultdict(int)

        print("Processing documents...")

        for filename in os.listdir(INPUT_DIR):
            if not filename.endswith(".txt"):
                continue

            doc_id = int(filename.split(".")[0])
            filepath = os.path.join(INPUT_DIR, filename)

            tokens = self.tokenizer.process_file(filepath)
            documents_tokens[doc_id] = tokens

            for token in set(tokens):
                token_df[token] += 1

            lemmas = [self.lemma_cache.get(t) for t in tokens]
            documents_lemmas[doc_id] = lemmas

            for lemma in set(lemmas):
                lemma_df[lemma] += 1

        N = len(documents_tokens)
        print(f"Loaded {N} documents")

        token_idf = {
            term: math.log(N / df)
            for term, df in token_df.items()
        }

        lemma_idf = {
            lemma: math.log(N / df)
            for lemma, df in lemma_df.items()
        }

        print("Computing TF-IDF...")

        for doc_id in documents_tokens:
            tokens = documents_tokens[doc_id]
            lemmas = documents_lemmas[doc_id]

            total_tokens = len(tokens)

            token_counter = Counter(tokens)

            token_tf = {
                term: count / total_tokens
                for term, count in token_counter.items()
            }

            token_data = {
                term: (token_idf.get(term, 0), token_tf[term] * token_idf.get(term, 0))
                for term in token_tf
            }

            self.token_writer.write(doc_id, token_data)

            lemma_counter = Counter(lemmas)

            lemma_tf = {
                lemma: count / total_tokens
                for lemma, count in lemma_counter.items()
            }

            lemma_data = {
                lemma: (lemma_idf.get(lemma, 0), lemma_tf[lemma] * lemma_idf.get(lemma, 0))
                for lemma in lemma_tf
            }

            self.lemma_writer.write(doc_id, lemma_data)

        print("Done! 🚀")