# Save this file exactly as: main.py
import os
import sys
from trainer import train_model
from pipeline.inference import CodeGenerator

# Setup environment tags to keep the terminal workspace clean
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "true"

def run_training_pipeline():
    """Triggers the trainer block and caches text size boundaries dynamically."""
    max_en, max_py = train_model()
    with open(".limits", "w") as f:
        f.write(f"{max_en},{max_py}")
    return max_en, max_py

print("=" * 65)
print("🤖 Custom FastAPI GenAI Interface Initializing...")
print("=" * 65)

# Path to the compiled binary model weights file
WEIGHTS_PATH = "models/weights/fastapi_model.pt"

# Baseline loop step: Try loading the infrastructure cleanly
try:
    if not os.path.exists(WEIGHTS_PATH):
        print("ℹ️ Weights file not found. Launching training sequence...")
        max_en, max_py = run_training_pipeline()
    else:
        with open(".limits", "r") as f:
            max_en, max_py = map(int, f.read().split(","))
            
    # Attempt to initialize the generator block (this acts as our architecture check)
    generator = CodeGenerator(max_en, max_py)

except RuntimeError as e:
    # 💡 THE AUTOMATIC FIX: Catch shape mismatch errors gracefully
    if "size mismatch" in str(e) or "Error(s) in loading state_dict" in str(e):
        print("\n🔄 Shape Mismatch Detected! Your dataset vocabulary has expanded.")
        print("Status: Wiping incompatible old weights and re-optimizing neural matrices...")
        
        # Safely remove the outdated checkpoint file if it exists
        if os.path.exists(WEIGHTS_PATH):
            os.remove(WEIGHTS_PATH)
            
        # Re-run training to generate compatible weight structures
        max_en, max_py = run_training_pipeline()
        
        # Hot-reload the generator engine with updated limits
        generator = CodeGenerator(max_en, max_py)
        print("✨ Hot-Reload Complete! Architecture models perfectly aligned.")
    else:
        # Pass unrelated structural runtime crashes along to standard console diagnostics
        raise e

print("\n🤖 System Ready! Type your request. Type 'exit' to shut down.")
print("💡 Tip: Type '--train' at any time to instantly re-train on dataset updates!")
print("=" * 65)

# Active Continuous Interaction Chat Loop Block
while True:
    try:
        user_prompt = input("GenAI Prompt > ").strip()
        
        if user_prompt.lower() in ["exit", "quit", "close"]:
            print("\n👋 Closing Generative AI cell space. Happy hacking!")
            break
            
        if not user_prompt:
            continue
            
        if user_prompt.lower() == "--train":
            print("\n♻️ Re-training request intercepted. Processing updates...")
            max_en, max_py = run_training_pipeline()
            generator = CodeGenerator(max_en, max_py)
            print("✨ Hot-Reload Complete! The model and weights folder are fully updated.")
            print("=" * 65)
            continue
            
        active_temp = 0.5 
        if "--temp" in user_prompt:
            try:
                base_part, temp_part = user_prompt.split("--temp")
                user_prompt = base_part.strip()
                active_temp = float(temp_part.strip())
            except ValueError:
                active_temp = 0.5
        
        generator.stream_code(user_prompt, temperature=active_temp)
        
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 System interrupted. Exiting session environment loop.")
        break
