# Save this file exactly as: trainer.py
import torch
import torch.nn as nn
from models.tokenizer import CodeTokenizer
from models.architecture import DynamicCodeTransformer

def train_model():
    """Trains the Transformer decoder matrices and saves weights inside models/weights/."""
    tok = CodeTokenizer()
    tok.load_data("data/data.txt")

    max_en = max(len(p.split()) for p, _ in tok.dataset)
    max_py = max(len(t) for _, t in tok.dataset)

    src_list, tgt_list = [], []
    for en_phrase, py_tokens in tok.dataset:
        src_list.append(tok.pad([tok.en_w2i.get(w, tok.en_w2i["<unk>"]) for w in en_phrase.lower().split()], max_en, tok.en_w2i["<pad>"]))
        tgt_list.append(tok.pad([tok.py_w2i[w] for w in py_tokens], max_py, tok.py_w2i["<pad>"]))

    src_tensor = torch.tensor(src_list, dtype=torch.long)
    tgt_tensor = torch.tensor(tgt_list, dtype=torch.long)

    model = DynamicCodeTransformer(len(tok.english_vocab), len(tok.python_vocab), d_model=64)
    criterion = nn.CrossEntropyLoss(ignore_index=tok.py_w2i["<pad>"])
    optimizer = torch.optim.Adam(model.parameters(), lr=0.002)

    print("Status: 🏋️ Training Transformer parameters on local dataset...")
    print("-" * 75)

    model.train()
    for epoch in range(350):
        optimizer.zero_grad()
        inputs = tgt_tensor[:, :-1]
        targets = tgt_tensor[:, 1:]
        outputs = model(src_tensor, inputs)
        
        loss = criterion(outputs.reshape(-1, len(tok.python_vocab)), targets.reshape(-1))
        
        predictions = torch.argmax(outputs, dim=-1)
        non_pad_mask = (targets != tok.py_w2i["<pad>"])
        correct_token_hits = (predictions == targets) & non_pad_mask
        
        total_valid_tokens = non_pad_mask.sum().item()
        accuracy = (correct_token_hits.sum().item() / total_valid_tokens) * 100 if total_valid_tokens > 0 else 0.0
        
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 50 == 0:
            print(f"  -> Epoch {epoch+1:03d}/350 | Loss: {loss.item():.6f} | Token Training Accuracy: {accuracy:.2f}%")

    print("-" * 75)
    # Save network weights into subfolder folder
    torch.save(model.state_dict(), "models/weights/fastapi_model.pt")
    print("Status: 💾 Model weights saved to 'models/weights/fastapi_model.pt'.")
    return max_en, max_py

if __name__ == "__main__":
    train_model()
