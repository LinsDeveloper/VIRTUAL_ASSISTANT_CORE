from pydantic import BaseModel, Field
from typing import Optional
from langchain.agents import initialize_agent
from langchain_community.chat_models import ChatOllama
from agents.spotify.tools.tools_play_music import get_spotify_tools
from core.enum.llm_type_enum import InstanceTypeLLM
from helpers.agents.format_json_output import get_result_message_output
from llms.main_llm import build_model
from models.AgentResponseModel import ResponseModel
import os
from dotenv import load_dotenv
from models.AgentResponseModel import ResponseModel
import json

load_dotenv()


class AgentSpotify:
    def __init__(self) -> None:
        llm = build_model(InstanceTypeLLM.GROQ, "llama3-70b-8192", temperature=0.7)
        tools = get_spotify_tools()

        system_message = """
        Você é um assistente que controla músicas no Spotify.
        Use as funções disponíveis para pausar ou tocar músicas.
        Não responda diretamente ao usuário — apenas chame a função correta com os argumentos apropriados.
        Responda SEMPRE em JSON no formato:
        {
            "thought": "<seu pensamento ou explicação interna>",
            "action": "<nome_da_ferramenta>",
            "action_input": "<string ou json com argumentos>",
            "output_response": {
                "success": true,
                "response": "<mensagem para o usuário>"
            }
        }
        Apenas retorne o JSON, sem explicações.
        """

        self.agent_executor = initialize_agent(
            tools=tools,
            llm=llm,
            agent="zero-shot-react-description",
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=1,
            return_intermediate_steps=True,
            system_message=system_message
        )



    def run(self, user_input: str) -> str:
        try:
            result = self.agent_executor.invoke({"input": user_input})

            if isinstance(result, dict):
                intermediate_steps = result.get("intermediate_steps", [])
                if intermediate_steps:
                    last_tool_response = intermediate_steps[-1][1]
                    if isinstance(last_tool_response, dict):
                        return json.dumps(last_tool_response, ensure_ascii=False)
                    else:
                        try:
                            parsed = json.loads(last_tool_response)
                            return json.dumps(parsed, ensure_ascii=False)
                        except:
                            return last_tool_response
                
                output = result.get("output")
                if output:
                    try:
                        parsed = json.loads(output)
                        return json.dumps(parsed, ensure_ascii=False)
                    except:
                        return output
            
            return str(result)

        except Exception as e:
            return json.dumps({
                "thought": "Erro ao executar o comando.",
                "action": "spotify_tool",
                "action_input": user_input,
                "output_response": {
                    "success": False,
                    "response": f"Ocorreu um erro ao executar o comando: {str(e)}"
                }
            }, ensure_ascii=False)
