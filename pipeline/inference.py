# Save this file exactly as: pipeline/inference.py
import sys
import subprocess  # 💡 NEW: Used to launch the local server in a separate background thread
import time
from pipeline.predictor import TokenPredictor
from pipeline.formatter import CodeFormatter
from pipeline.validator import CodeValidator

class CodeGenerator:
    """Orchestrates predictions, live output formatting streams, and security validators."""
    def __init__(self, max_en, max_py):
        self.predictor = TokenPredictor(max_en, max_py)
        self.server_process = None  # Tracks the active background Uvicorn server

    def stream_code(self, english_prompt, temperature=0.5, export_filename="app.py"):
        # 1. Compute and predict tokens out of our custom network
        raw_words = self.predictor.generate_token_sequence(english_prompt, temperature)
        
        print(f"\n💻 AI Streaming Output (Temperature: {temperature}):")
        print("-" * 35)
        
        # 2. Feed words one-by-one to live typing typewriter stream controller
        is_first_word = True
        for word in raw_words:
            is_first_word = CodeFormatter.stream_to_terminal(word, is_first_word)
            
        print("\n" + "-" * 35)
        
        # 3. Clean line spacing formatting alignments
        clean_python_code = CodeFormatter.clean_code_block(raw_words)
        
        # 4. Filter through grammar guards and track validation passes
        validation_passed = CodeValidator.validate_and_save(clean_python_code, export_filename)
        
        # ==============================================================================
        # 💡 AUTOMATED BACKGROUND UVICORN RUNNER
        # ==============================================================================
        if validation_passed and export_filename == "app.py":
            # If an older server process was already running from a previous prompt, terminate it safely first
            if self.server_process is not None:
                print("♻️ Hot-Swapping Server: Shutting down previous API instance...")
                self.server_process.terminate()
                self.server_process.wait()

            print("🌐 Live Server Engine: Booting Uvicorn on http://127.0.0.1:8000 ...")
            
            # Spin up the newly generated app.py file via a background shell subprocess
            self.server_process = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"],
                stdout=subprocess.DEVNULL,  # Redirect logs to keep your main chat screen clean
                stderr=subprocess.DEVNULL
            )
            
            time.sleep(1.0)  # Give the background process a quick second to securely open the port
            print("🚀 Server Live! You can now send POST payloads directly to http://127.0.0")
