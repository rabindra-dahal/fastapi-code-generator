# Save this file exactly as: models/tokenizer.py
import os

class CodeTokenizer:
    """Handles parsing strings and mapping words to numeric indexes."""
    def __init__(self):
        self.english_vocab = ["<pad>", "<unk>"]
        self.python_vocab  = ["<pad>", "<sos>", "<eos>", "<unk>"]
        self.dataset = []

    def load_data(self, file_path="data/data.txt"):
        """Reads data.txt, isolates text words, and builds the lexicon index dictionary."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Missing training file text baseline: {file_path}")

        with open(file_path, "r") as file:
            for line in file:
                if "|" in line:
                    en_part, py_part = line.strip().split("|")
                    py_tokens = ["<sos>"] + py_part.split() + ["<eos>"]
                    self.dataset.append((en_part, py_tokens))
                    
                    # Grow vocabulary lookup tables dynamically
                    for w in en_part.lower().split():
                        if w not in self.english_vocab: self.english_vocab.append(w)
                    for w in py_tokens:
                        if w not in self.python_vocab: self.python_vocab.append(w)

        # Build quick lookups
        self.en_w2i = {w: i for i, w in enumerate(self.english_vocab)}
        self.en_i2w = {i: w for i, w in enumerate(self.english_vocab)}
        self.py_w2i = {w: i for i, w in enumerate(self.python_vocab)}
        self.py_i2w = {i: w for i, w in enumerate(self.python_vocab)}

    def pad(self, seq, max_len, pad_idx):
        """Appends padding IDs to maintain rectangular tensor shape layouts."""
        return seq + [pad_idx] * (max_len - len(seq))
