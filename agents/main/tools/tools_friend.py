from langchain.tools import BaseTool
from pydantic import PrivateAttr
from agents.friend.friend_agent import AgentFriend


class AgentFriendTool(BaseTool):
    name: str = "agent_friend"
    description: str = (
        "Use essa ferramenta quando precisar apenas bater papo ou conversar sobre assuntos diversos que não seja pedir coisas relacionadas a música."
        "Não a utilize para comandos específicos ou técnicos."
    )

    _friend_agent: AgentFriend = PrivateAttr()

    def __init__(self):
        super().__init__()
        self._friend_agent = AgentFriend()

    def _run(self, query: str) -> str:
        return self._friend_agent.run(query)

    async def _arun(self, query: str) -> str:
        return self._run(query)
