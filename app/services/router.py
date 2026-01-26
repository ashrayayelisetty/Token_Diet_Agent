from app.utils import count_tokens

class ModelRouter:
    def __init__(self):
        # Keywords that signal high reasoning is needed
        self.complex_keywords = [
            "analyze", "debug", "optimize", "calculate", 
            "rewrite", "evaluate", "why", "architect"
        ]

    def select_model(self, prompt: str) -> str:
        # 1. Check length (Volume check)
        token_count = count_tokens(prompt)
        
        # 2. Check intent (Keyword check)
        is_complex = any(kw in prompt.lower() for kw in self.complex_keywords)
        
        # 3. Final decision
        if token_count > 200 or is_complex:
            return "llama-3.1-405b-reasoning"  # The "Premium" model
        
        return "llama-3.3-70b-versatile" # The "Economy" model

# Test logic for verification
if __name__ == "__main__":
    router = ModelRouter()
    print(f"Test 1: {router.select_model('Hi, how are you?')}") # Should be mini
    print(f"Test 2: {router.select_model('Debug this memory leak in my Python app')}") # Should be 4o