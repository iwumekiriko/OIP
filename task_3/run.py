import sys
import os

sys.path.append(os.path.abspath(".."))
from task_2.tokenizer import Tokenizer

from config import *
from inv_index import InvertedIndex

if __name__ == "__main__":
    tokenizer = Tokenizer()
    inv_index = InvertedIndex(tokenizer)

    inv_index.build(INPUT_DIR)
    inv_index.save(INDEX_FILE)

    print("Index ready!")