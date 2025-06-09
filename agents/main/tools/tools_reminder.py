

from agents.reminder.remember_agent import AgentReminder
from langchain.tools import BaseTool
from pydantic import PrivateAttr


class AgentReminderTool(BaseTool):
    name: str = "reminder_agent"
    description: str = "Use essa ferramenta para criar lembretes ou ajudar a lembrar de algo."

    _spotify_agent: AgentReminder = PrivateAttr()

    def __init__(self):
        super().__init__()
        self._reminder_agent = AgentReminder()

    def _run(self, query: str) -> str:
        return self._reminder_agent.run(query)

    async def _arun(self, query: str) -> str:
        return self._run(query)