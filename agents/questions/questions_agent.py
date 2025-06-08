from pydantic import BaseModel, Field
from typing import Optional
from langchain.agents import initialize_agent
from langchain_community.chat_models import ChatOllama
from agents.spotify.tools.tools_play_music import get_spotify_tools
from core.enum.llm_type_enum import InstanceTypeLLM
from helpers.agents.format_json_output import get_result_message_output
from llms.main_llm import build_model
from models.AgentResponseModel import ResponseModel
from dotenv import load_dotenv
import os
load_dotenv()


class AgentQuestions:
    def __init__(self) -> None:
        self.llm = build_model(InstanceTypeLLM.GROQ, "llama3-70b-8192", temperature=0.7)

        self.system_message = """
        Você é um assistente que se comporta como um respondedor de perguntas.
        Não dê respostas muito longas.
        Sempre responda em português brasileiro. Nunca responda em inglês ou outro idioma.
        """

    def run(self, user_input: str) -> str:
        try:
            prompt = [
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": user_input}
            ]
            result = self.llm.invoke(prompt)
            return result.content if hasattr(result, 'content') else str(result)
        
        except Exception as e:
            return ResponseModel(success=False, response=f"Ocorreu um erro ao executar o comando: {str(e)}")
