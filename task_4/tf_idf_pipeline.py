import os
import math
import sys

sys.path.append(os.path.abspath(".."))

from task_2.tokenizer import Tokenizer
from task_2.lemmatizer import Lemmatizer

from document_processor import DocumentProcessor
from tf_calculator import TFCalculator
from idf_calculator import IDFCalculator
from tf_idf_calculator import TFIDFCalculator
from lemma_processor import LemmaProcessor
from result_writer import ResultWriter

from config import *


class TFIDFPipeline:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.lemmatizer = Lemmatizer()

        self.doc_processor = DocumentProcessor(self.tokenizer)
        self.tf_calc = TFCalculator()
        self.idf_calc = IDFCalculator()
        self.tfidf_calc = TFIDFCalculator()
        self.lemma_processor = LemmaProcessor(self.lemmatizer)

        self.token_writer = ResultWriter(TOKENS_OUT)
        self.lemma_writer = ResultWriter(LEMMAS_OUT)

    def run(self) -> None:
        documents_tokens = {}

        for filename in os.listdir(INPUT_DIR):
            if not filename.endswith(".txt"):
                continue

            doc_id = int(filename.split(".")[0])
            filepath = os.path.join(INPUT_DIR, filename)

            tokens = self.doc_processor.process_document(filepath)
            documents_tokens[doc_id] = tokens

        print(f"Loaded {len(documents_tokens)} documents")

        idf = self.idf_calc.compute_idf(documents_tokens)

        for doc_id, tokens in documents_tokens.items():
            tf, counter = self.tf_calc.compute_tf(tokens)
            tfidf = self.tfidf_calc.compute(tf, idf)

            token_data = {
                term: (idf.get(term, 0), tfidf.get(term, 0))
                for term in tf
            }
            self.token_writer.write(doc_id, token_data)

            lemma_map = self.lemma_processor.build_lemma_map(tokens)
            lemma_tf = self.lemma_processor.compute_lemma_tf(
                counter, lemma_map, len(tokens)
            )

            lemma_idf = {}
            for lemma in lemma_map:
                df = sum(1 for t in documents_tokens.values()
                         if lemma in set(self.lemmatizer.lemmatizer.lemmatize(x) for x in t))
                lemma_idf[lemma] = math.log(len(documents_tokens) / df) if df else 0

            lemma_tfidf = {
                lemma: lemma_tf[lemma] * lemma_idf.get(lemma, 0)
                for lemma in lemma_tf
            }

            lemma_data = {
                lemma: (lemma_idf.get(lemma, 0), lemma_tfidf.get(lemma, 0))
                for lemma in lemma_tf
            }

            self.lemma_writer.write(doc_id, lemma_data)

        print("TF-IDF computation complete!")