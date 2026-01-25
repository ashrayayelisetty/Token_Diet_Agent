import tiktoken

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """Returns the number of tokens in a string."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def calculate_cost(tokens: int, model: str) -> float:
    """Calculates approximate cost in USD."""
    # Prices per 1M tokens (Approx 2026 rates)
    prices = {
        "gpt-4o-mini": 0.15 / 1_000_000,
        "gpt-4o": 2.50 / 1_000_000
    }
    return tokens * prices.get(model, 0)