# Save this file exactly as: data/generate_synthetic.py

def build_advanced_fastapi_dataset():
    print("🧠 Generating high-density Multi-Route & POST Body Structure data rows...")
    
    actions = ["create", "build", "generate", "setup", "make"]
    apps = ["a simple fastapi app", "a fastapi web application", "a backend API service", "an app", "an api"]
    
    # 1. Base Framework Structural Components
    health_block = '@app.get("/health") \\n def health_check(): \\n     return {"healthy": True}'
    pydantic_import = "from pydantic import BaseModel , Field"
    
    # 2. Comprehensive POST Schema Blocks (Nested data parameters)
    product_schema = 'class Product(BaseModel): \\n     title: str \\n     price: float = Field(gt=0) \\n     stock: int \\n     active: bool'
    order_schema   = 'class Order(BaseModel): \\n     item_id: int \\n     quantity: int \\n     priority: bool'
    
    # 3. Dynamic POST Execution Route Handlers
    post_product_route = '@app.post("/products") \\n def add_product(product: Product): \\n     return {"status": "created", "data": product}'
    post_order_route   = '@app.post("/orders") \\n def place_order(order: Order): \\n     return {"status": "processed", "order_id": order.item_id}'
    
    unique_rows = set()
    
    # Generate classic baseline applications blocks
    for act in actions:
        for app in apps:
            base_code = "from fastapi import FastAPI \\n app = FastAPI()"
            unique_rows.add(f"{act} {app}|{base_code}\n")
            unique_rows.add(f"{act} a health check app|{base_code} \\n {health_block}\n")
            
    # 4. Matrix combination mapping: Cross-multiply prompts with structured POST body workflows
    for act in actions:
        for app in apps:
            # Combo A: Product Data Object Injection
            prompt_prod = f"{act} {app} with a post route for product model body data"
            code_prod = f"from fastapi import FastAPI \\n {pydantic_import} \\n {product_schema} \\n app = FastAPI() \\n {post_product_route}"
            unique_rows.add(f"{prompt_prod}|{code_prod}\n")
            
            # Shorthand version for fuzzy layout inputs
            unique_rows.add(f"{act} a product post api body|{code_prod}\n")
            
            # Combo B: Order Request Body Mapping
            prompt_ord = f"{act} {app} with a post request to place an order object"
            code_ord = f"from fastapi import FastAPI \\n {pydantic_import} \\n {order_schema} \\n app = FastAPI() \\n {post_order_route}"
            unique_rows.add(f"{prompt_ord}|{code_ord}\n")
            
            # Shorthand version for fuzzy layout inputs
            unique_rows.add(f"{act} an order creation body path|{code_ord}\n")

    # Save sorted, completely deduplicated data blocks down inside the data subfolder
    with open("data/data.txt", "w", encoding="utf-8") as file:
        file.writelines(sorted(list(unique_rows)))
        
    print(f"🎉 Success! Generated {len(unique_rows)} unique Single, Multi, and POST Schema workflows inside 'data/data.txt'.")

if __name__ == "__main__":
    build_advanced_fastapi_dataset()
