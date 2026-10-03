# Save this file exactly as: models/architecture.py
import torch
import torch.nn as nn
import math

class PositionalEncoding(nn.Module):
    """Infuses structural timeline context into words via sine/cosine waves."""
    def __init__(self, d_model, max_len=50):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x):
        return x + self.pe[:x.size(1), :]

class DynamicCodeTransformer(nn.Module):
    """Complete Sequence-to-Sequence framework joining Reader and Writer components."""
    def __init__(self, src_vocab_size, tgt_vocab_size, d_model=64):
        super().__init__()
        self.src_embedding = nn.Embedding(src_vocab_size, d_model)
        self.tgt_embedding = nn.Embedding(tgt_vocab_size, d_model)
        self.pos_encoder = PositionalEncoding(d_model)
        
        self.transformer = nn.Transformer(
            d_model=d_model, nhead=4,
            num_encoder_layers=3, num_decoder_layers=3,
            dim_feedforward=128, batch_first=True
        )
        self.classifier = nn.Linear(d_model, tgt_vocab_size)

    def forward(self, src, tgt):
        src_emb = self.pos_encoder(self.src_embedding(src))
        tgt_emb = self.pos_encoder(self.tgt_embedding(tgt))
        
        # Look-ahead causal masking forces the decoder to guess step-by-step
        sz = tgt.size(1)
        tgt_mask = torch.triu(torch.full((sz, sz), float('-inf'), device=tgt.device), diagonal=1)
        
        out = self.transformer(src_emb, tgt_emb, tgt_mask=tgt_mask)
        return self.classifier(out)
