

from langchain.tools import BaseTool
from typing import ClassVar

from pydantic import PrivateAttr
from agents.spotify.spotify_agent import AgentSpotify


class AgentSpotifyTool(BaseTool):
    name: str = "agent_spotify"
    description: str = (
        "Ferramenta que executa comandos referente a música. "
        "Execute essa ferramenta sempre que precisar pausar, retomar ou colocar uma música específica."
    )
    
    _spotify_agent: AgentSpotify = PrivateAttr()

    def __init__(self):
        super().__init__()
        self._spotify_agent = AgentSpotify()

    def _run(self, query: str) -> str:
        return self._spotify_agent.run(query)

    async def _arun(self, query: str) -> str:
        return self._run(query)