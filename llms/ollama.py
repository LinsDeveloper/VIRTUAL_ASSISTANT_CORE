from langchain.llms import Ollama

def build_model_ollama(model_id: str, temperature: float = 0.7) -> Ollama:
    """
    Build the Ollama model with the specified parameters.
    """
    llm = Ollama(
        model=model_id,
        temperature=temperature,
    )
    
    return llm