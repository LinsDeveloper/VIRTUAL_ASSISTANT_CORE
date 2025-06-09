from typing import Optional
from agents.reminder.resources.reminder_resource import create_reminder_from_query
from langchain.tools import Tool


def call_tool_reminder(query: str) -> str:
    try:
        response = create_reminder_from_query(query)
        return response.response if hasattr(response, "response") else str(response)
    except Exception as e:
        return f"Erro ao criar lembrete: {str(e)}"


def get_reminder_tools():
    return [
        Tool(
            name="create_reminder",
            func=call_tool_reminder,
            description="Cria um lembrete com base em um comando do usuário, como 'me lembre de algo às 18h'."
        )
    ]


__all__ = ["get_reminder_tools"]
