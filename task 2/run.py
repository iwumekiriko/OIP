from config import *
from tokenizer import Tokenizer
from lemmatizer import Lemmatizer

if __name__ == "__main__":
    tokenizer = Tokenizer()
    tokens = tokenizer.process_directory(INPUT_DIR)
    tokenizer.save_tokens(tokens, TOKENS_FILE)

    print(f"Total tokens: {len(tokens)}")

    lemmatizer = Lemmatizer()
    lemmas = lemmatizer.build_lemma_dict(tokens)
    lemmatizer.save_lemmas(lemmas, LEMMAS_FILE)

    print(f"Total lemmas: {len(lemmas.keys())}")

    print("\nDone!")