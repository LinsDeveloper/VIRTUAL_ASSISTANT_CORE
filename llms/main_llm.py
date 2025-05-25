import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv
from core.enum.llm_type_enum import InstanceTypeLLM
from llms.groq_llms import build_model_groq
from llms.ollama import build_model_ollama

load_dotenv()

def build_model(instance_type: str, model_id: str, temperature: float = 0.7) -> any:
    """
    Build the model with the specified parameters.
    """
    
    match instance_type:
        case InstanceTypeLLM.OLLAMA:
            return build_model_ollama(model_id, temperature)
        case InstanceTypeLLM.GROQ:
            return build_model_groq(model_id, temperature)
        
    raise ValueError(f"Unknown instance type: {instance_type}")