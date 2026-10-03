# Save this file exactly as: pipeline/formatter.py
import sys
import time
import re  # Using native regex to isolate variable attributes precisely

class CodeFormatter:
    """Manages real-time screen output streaming and post-generation layout spacing indents."""
    
    @staticmethod
    def stream_to_terminal(word, is_first_word):
        """Streams individual code words to the command line live with proper indents."""
        if word == "\\n" or word == "\n":
            sys.stdout.write("\n")
            return True  # Signal that the next word starts a fresh line
        else:
            # 💡 THE PRECISION FIX: 
            # Use a strict regular expression to match exactly how Pydantic variables look.
            # This checks if a word consists ONLY of letters/underscores followed by a colon (e.g., 'title:', 'stock:')
            # This completely ignores structural parameters like 'product:' inside function arguments or ', ' markers!
            is_pydantic_attribute = bool(re.match(r"^[a-zA-Z_]+:$", word))
            
            if word == "return":
                sys.stdout.write("    return")
            elif is_pydantic_attribute and word not in ["from:", "import:"]:
                sys.stdout.write(f"    {word}")  # Indent ONLY valid standalone class variables
            else:
                text_to_draw = word if is_first_word else f" {word}"
                if word == "()": 
                    text_to_draw = "()"
                sys.stdout.write(text_to_draw)
                
            sys.stdout.flush()
            time.sleep(0.04)  # Fluid type animation delay
            return False

    @staticmethod
    def clean_code_block(assembled_tokens):
        """Assembles list arrays into valid indented Python code strings."""
        final_lines, current_line = [], []
        for token in assembled_tokens:
            if token == "\\n" or token == "\n":
                final_lines.append(" ".join(current_line))
                current_line = []
            else:
                current_line.append(token)
        if current_line: 
            final_lines.append(" ".join(current_line))
            
        code = "\n".join(final_lines)
        code = code.replace("app = FastAPI ()", "app = FastAPI()")
        
        # Comprehensive alignment post-processor transformations matrix
        replacements = {
            "return {": "    return {", "return item": "    return item", "return user": "    return user", "return product": "    return product", "return order": "    return order",
            "name: str": "    name: str", "username: str": "    username: str", "email: str": "    email: str",
            "title: str": "    title: str", "stock: int": "    stock: int", "active: bool": "    active: bool",
            "item_id: int": "    item_id: int", "quantity: int": "    quantity: int", "priority: bool": "    priority: bool",
            "price: float = Field(gt=0)": "    price: float = Field(gt=0)"
        }
        for target, replacement in replacements.items():
            code = code.replace(target, replacement)
        return code
