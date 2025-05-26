

from langchain.tools import BaseTool
from typing import ClassVar

from pydantic import PrivateAttr
from agents.spotify.spotify_agent import AgentSpotify


class AgentSpotifyTool(BaseTool):
    name: ClassVar[str] = "agent_spotify"
    description: ClassVar[str] = "Ferramenta que executa comandos do agente Spotify e retorna a resposta em JSON."

    _spotify_agent: AgentSpotify = PrivateAttr()

    def __init__(self):
        super().__init__()
        self._spotify_agent = AgentSpotify()

    def _run(self, query: str) -> str:
        return self._spotify_agent.run(query)

    async def _arun(self, query: str) -> str:
        return self._run(query)