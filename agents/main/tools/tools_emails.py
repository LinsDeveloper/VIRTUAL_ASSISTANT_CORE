

from agents.email.email_agent import AgentEmail
from langchain.tools import BaseTool
from typing import ClassVar

from pydantic import PrivateAttr


class AgentEmailTool(BaseTool):
    name: str = "agent_email"
    description: str = (
        "Ferramenta que executa comandos referente a email. "
        "Execute essa ferramenta sempre que precisar listar emails."
    )
    
    _spotify_agent: AgentEmail = PrivateAttr()

    def __init__(self):
        super().__init__()
        self._spotify_agent = AgentEmail()

    def _run(self, query: str) -> str:
        return self._spotify_agent.run(query)

    async def _arun(self, query: str) -> str:
        return self._run(query)