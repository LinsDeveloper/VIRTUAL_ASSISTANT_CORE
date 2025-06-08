
from langchain_community.chat_models import ChatOllama

def build_model_ollama(model_id: str, temperature: float = 0.7) -> ChatOllama:
    """
    Build the Ollama model with the specified parameters.
    """
    llm = ChatOllama(
        model=model_id,
        temperature=temperature,
    )
    
    return llm