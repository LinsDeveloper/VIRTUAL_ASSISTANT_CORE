import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

def build_model_groq(model_id: str, temperature: float = 0.7) -> ChatOpenAI:
    """
    Build the Groq model with the specified parameters.
    """
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("API key not found. Please set the GROQ_API_KEY environment variable.")
    
    llm = ChatOpenAI(
        openai_api_key=groq_api_key,
        openai_api_base="https://api.groq.com/openai/v1",
        model_name=model_id,
        temperature=temperature,
    )
    
    return llm