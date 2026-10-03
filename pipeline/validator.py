# Save this file exactly as: pipeline/validator.py
import ast

class CodeValidator:
    """Performs strict grammar checking and logical repetition blocking before file writes."""
    
    @staticmethod
    def validate_and_save(code_string, filename="app.py"):
        """Runs the validation chain layer graph. Returns true if fully stable."""
        try:
            # 1. Structural python compiler grammar validation check
            ast.parse(code_string)
            
            # 2. Logic Check: Intercept high temperature decorator loop traps
            lines = [line.strip() for line in code_string.split("\n") if line.strip()]
            for i in range(len(lines) - 1):
                if lines[i].startswith("@") and lines[i] == lines[i+1]:
                    print(f"📊 Validation Check: 🔴 FAILED (Logical Loop Trap)!")
                    print(f"⚠️ Warning: Duplicate decorator loop detected: '{lines[i]}'")
                    return False
            
            # Save data if everything is pristine
            with open(filename, "w", encoding="utf-8") as f:
                f.write(code_string)
            print("📊 Validation Check: 🟢 PASSED! Structural code logic isolated.")
            print(f"💾 Successfully compiled and saved running script into '{filename}'")
            return True
            
        except SyntaxError as e:
            print("📊 Validation Check: 🔴 FAILED (Syntax Error)!")
            print(f"⚠️ Compiler Warning: Line {e.lineno} -> {e.msg}")
            return False
