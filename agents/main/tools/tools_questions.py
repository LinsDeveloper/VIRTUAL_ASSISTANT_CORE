

from langchain.tools import BaseTool
from typing import ClassVar
from pydantic import PrivateAttr
from agents.friend.friend_agent import AgentFriend
from agents.questions.questions_agent import AgentQuestions


class AgentQuestionsTool(BaseTool):
    name: str = "agent_questions"
    description: str = "Use essa ferramenta para responder perguntas apenas no geral sobre qualquer assunto. Use apenas para perguntas."

    _spotify_agent: AgentQuestions = PrivateAttr()

    def __init__(self):
        super().__init__()
        self._spotify_agent = AgentQuestions()

    def _run(self, query: str) -> str:
        return self._spotify_agent.run(query)

    async def _arun(self, query: str) -> str:
        return self._run(query)