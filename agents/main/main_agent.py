

from langchain.agents import initialize_agent
from langchain_community.chat_models import ChatOllama
from agents.main.tools.tools_friend import AgentFriendTool
from agents.main.tools.tools_questions import AgentQuestionsTool
from agents.main.tools.tools_spotify import AgentSpotifyTool
from core.enum.llm_type_enum import InstanceTypeLLM
from helpers.agents.format_json_output import get_result_message_output
from llms.main_llm import build_model
from dotenv import load_dotenv
import os
load_dotenv()

class AgentMain:
    def __init__(self):
        self.spotify_tool = AgentSpotifyTool()
        self.friend_tool = AgentFriendTool()
        self.questions_tool = AgentQuestionsTool()

        llm = build_model(InstanceTypeLLM.GROQ, "llama3-70b-8192", temperature=0.7)

        system_message = """
        Você é um agente principal que tem ferramentas.
        Quando receber uma mensagem, deve usar ferramentas para processar o comando e
        retornar a resposta exatamente como ela vier, sem alterações.
        Sempre retorne o resultado JSON que a ferramenta retornar.
        Sempre responda em português brasileiro. Nunca responda em inglês ou outro idioma.
        """

        self.agent_executor = initialize_agent(
            tools=[self.questions_tool, self.friend_tool, self.spotify_tool],
            llm=llm,
            agent="zero-shot-react-description",
            verbose=True,
            system_message=system_message,
            max_iterations=1,
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )

    def run(self, user_input: str) -> str:
        try:
            result = self.agent_executor.invoke({"input": user_input})

            intermediate_steps = result.get("intermediate_steps", [])
            if intermediate_steps:
                last_tool_response = intermediate_steps[-1][1]
                return last_tool_response
            
            return result.get("output", "Nenhuma resposta obtida.")

        except Exception as e:
            return f"Ocorreu um erro ao executar o agente: {str(e)}"


