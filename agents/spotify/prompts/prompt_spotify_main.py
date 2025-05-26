from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser

from pydantic import BaseModel
from typing import Optional, Dict, Any




def build_structured_spotify_prompt(_: Any = None) -> ChatPromptTemplate:
    system_template = """
    Você é um assistente que controla músicas no Spotify.

    Use as funções disponíveis para pausar ou tocar músicas.
    Não responda diretamente ao usuário — apenas chame a função correta com os argumentos apropriados.
    """
    
    human_template = "{input}"

    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(human_template),
    ])

    return prompt

