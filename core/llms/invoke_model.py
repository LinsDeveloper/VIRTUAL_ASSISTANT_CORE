import os

def get_model_class(model_name: str, temperature: float = 0.7):
    """
    This function returns the model class based on the model name.
    """
    mocked = os.getenv("MOCKED_LLM")
    
    if mocked:
        from langchain_ollama import OllamaLLM
        return OllamaLLM(model="llama3:8b", temperature=temperature)
    
    match model_name:
        case "llama3:8b":
            from langchain_ollama import OllamaLLM
            return OllamaLLM(model="llama3:8b", temperature=temperature)
        case _:
            raise ValueError(f"Model {model_name} not supported.")
