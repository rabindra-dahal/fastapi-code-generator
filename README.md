# Custom FastAPI Generative AI Engine (From Scratch)

A professional, self-contained Sequence-to-Sequence (Seq2Seq) Transformer model built entirely from scratch using **PyTorch**. This system processes abstract English text prompts, maps them through customized neural network multi-head attention layers, streams code token-by-token directly to your console, and auto-compiles runnable, syntax-verified **FastAPI** web applications.

---

## 🚀 Features Built So Far

*   **Pure PyTorch Architecture:** Built the underlying structural Transformer cell networks from the ground up, including custom word-order spatial tracking vectors (Sine/Cosine Positional Encoding).
*   **Live Token Typewriter Stream:** Intercepts number-matrix tokens dynamically inside the generation loop and flushes them text-by-text via standard output alongside custom regular expression spacing maps.
*   **Dual-Gate Structural Validation:** Implemented an internal compiler shield. Every generated app passes an abstract grammatical syntax parsing loop (`ast.parse`) and a structural repetition blocker (preventing high-temperature decorator loops) before saving.
*   **Hot-Reload Machine Learning Core:** Dynamically checks for saved file structural anomalies (like vocabulary shape mismatches when changing datasets) on system boot, automatically re-calibrating neural matrices to 100% token accuracy.
*   **Pydantic & POST Schema Pipeline:** Capable of synthesizing complex endpoint trees containing object-oriented request validation schemas (processing integers, booleans, nested attributes, and `Field` constraints like `gt=0`).

---

## 📁 Repository Folder Structure

```text
fastapi-code-generator/
│
├── data/
│   ├── data.txt                 # Deduplicated prompt-to-code dataset lines
│   └── generate_synthetic.py    # Synthetic multi-route dataset engine
│
├── models/
│   ├── architecture.py          # Pure PyTorch Transformer Core (Encoder-Decoder)
│   ├── tokenizer.py             # Custom Vocabulary Word-to-Index Maps
│   └── weights/
│       └── fastapi_model.pt     # Binary weights checkpoint (Auto-generated)
│
├── pipeline/
│   ├── predictor.py             # Temperature sampling probability math
│   ├── formatter.py             # Live console typewriter streaming & formatting
│   ├── validator.py             # AST grammar checks & logic loop blocker
│   └── inference.py             # Main pipeline orchestrator coordinator 
│
├── main.py                      # Main loop interactive prompt interface
├── trainer.py                   # Weight optimization loop & diagnostic reporter
└── requirements.txt             # Project system dependencies tracker
```

---

## ⚙️ Installation & Environment Setup

### 1. Initialize Virtual Environment & Activate
```bash
# Create environment
python -m venv venv

# Activate on Windows (MINGW64 / Git Bash)
source venv/Scripts/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🏋️ How to Run and Interact with the AI

### Step 1: Re-seed the Clean Dataset File
Run the data script to write the pristine, non-repetitive single and compound FastAPI templates into your data folder:
```bash
python data/generate_synthetic.py
```

### Step 2: Boot Up the Custom GenAI Interface
```bash
python main.py
```
*Note: On your very first execution, the system will instantly flag that `fastapi_model.pt` is missing, trigger a clean 350-epoch background optimization pass to drive error cross-entropy loss down near zero, and save the binary weights matrix before opening the prompt.*

### Step 3: Prompting the Transformer Live
Type natural requests straight into your active console screen wrapper. 

**Standard Prompts to Try:**
*   `GenAI Prompt > create a simple fastapi app with a health check path`
*   `GenAI Prompt > build a product post api body`
*   `GenAI Prompt > generate health check and setup with items`

#### Using Operational Flag Modifiers:
*   **Control Creativity:** Add a temperature tag flag at the end of any line to change probability weights (`--temp 0.0` for maximum safety, `--temp 0.8` for choosing alternate synonymous vocabulary combinations).
    *   *Example:* `build a product post api body --temp 0.4`
*   **System Hot-Reload:** Type `--train` at any moment inside the console to immediately run background weight re-training if you manually tweak the text dataset files.
    *   *Example:* `GenAI Prompt > --train`

---

## 💻 Sample Clean Output Format

When prompting for a model schema structure, the live printer formats text segments on-the-fly, generating an error-free **`app.py`** script file ready for active web serving execution:

```python
from fastapi import FastAPI
from pydantic import BaseModel , Field

class Product(BaseModel):
    title: str
    price: float = Field(gt=0)
    stock: int
    active: bool

app = FastAPI()

@app.post("/products")
def add_product(product: Product):
    return {"status": "created", "data": product}
```

You can immediately spin up your AI's code compilation script live on your machine using:
```bash
uvicorn app:app --reload
```
