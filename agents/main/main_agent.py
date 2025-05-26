

from langchain.agents import initialize_agent
from langchain_community.chat_models import ChatOllama
from agents.main.tools.tools_spotify import AgentSpotifyTool
from helpers.agents.format_json_output import get_result_message_output

class AgentMain:
    def __init__(self, model_name: str = "llama3:8b", temperature: float = 0.7):
        self.spotify_tool = AgentSpotifyTool()

        llm = ChatOllama(model=model_name, temperature=temperature)

        system_message = """
        Você é um agente principal que tem uma ferramentas.
        Quando receber uma mensagem, deve usar ferramentas para processar o comando e
        retornar a resposta exatamente como ela vier, sem alterações.
        Sempre retorne o resultado JSON que a ferramenta retornar.
        """

        self.agent_executor = initialize_agent(
            tools=[self.spotify_tool],
            llm=llm,
            agent="zero-shot-react-description",
            verbose=True,
            system_message=system_message,
            max_iterations=1,
            handle_parsing_errors=True,
        )

    def run(self, user_input: str) -> str:
        result = self.spotify_tool.run(user_input)
        intermediate_steps = result.get("intermediate_steps", [])
        
        if intermediate_steps:
            last_tool_response = intermediate_steps[-1][1]
            return last_tool_response
        
        return result.get("output", "Nenhuma resposta obtida na ação.")

