from config import *
from tokenizer import Tokenizer

if __name__ == "__main__":
    tokenizer = Tokenizer()
    tokens = tokenizer.process_directory(INPUT_DIR)
    tokenizer.save_tokens(tokens, TOKENS_FILE)

    print(f"Total tokens: {len(tokens)}")