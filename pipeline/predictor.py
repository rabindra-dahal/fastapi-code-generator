# Save this file exactly as: pipeline/predictor.py
import torch
import torch.nn.functional as F
from models.tokenizer import CodeTokenizer
from models.architecture import DynamicCodeTransformer

class TokenPredictor:
    """Manages raw token calculations and temperature sampling probability matrix math."""
    def __init__(self, max_en, max_py):
        self.tok = CodeTokenizer()
        self.tok.load_data("data/data.txt")
        self.max_en = max_en
        self.max_py = max_py
        
        self.model = DynamicCodeTransformer(len(self.tok.english_vocab), len(self.tok.python_vocab), d_model=64)
        self.model.load_state_dict(torch.load("models/weights/fastapi_model.pt", weights_only=True))
        self.model.eval()

    def generate_token_sequence(self, english_prompt, temperature=0.5):
        """Processes the English text prompt dynamically into raw word token lists."""
        prompt_tokens = [self.tok.en_w2i.get(w, self.tok.en_w2i["<unk>"]) for w in english_prompt.lower().split()]
        src_in = torch.tensor([self.tok.pad(prompt_tokens, self.max_en, self.tok.en_w2i["<pad>"])], dtype=torch.long)
        
        generated_py = [self.tok.py_w2i["<sos>"]]
        assembled_words = []
        
        for _ in range(self.max_py):
            tgt_in = torch.tensor([generated_py], dtype=torch.long)
            with torch.no_grad():
                logits = self.model(src_in, tgt_in)
                
            last_token_logits = logits[0, -1, :]
            
            if temperature == 0.0:
                next_tok = torch.argmax(last_token_logits).item()
            else:
                scaled_logits = last_token_logits / temperature
                probabilities = F.softmax(scaled_logits, dim=-1)
                next_tok = torch.multinomial(probabilities, num_samples=1).item()
                
            if next_tok == self.tok.py_w2i["<eos>"]: 
                break
                
            word = self.tok.py_i2w[next_tok]
            
            # Shield: Prevent internal control tokens from ever printing or saving
            if word in ["<sos>", "<pad>", "<unk>"]:
                continue
                
            generated_py.append(next_tok)
            assembled_words.append(word)
            
        return assembled_words
