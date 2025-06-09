from typing import Optional
from langchain.tools import Tool
from agents.email.resources.email_resource import list_emails_tool


def list_email_func(_action: str = None) -> str:
    response = list_emails_tool()
    return response.response 

def get_email_tools():
    return [
        Tool(
            name="list_lasts_emails",
            func=list_email_func,
            description="Utilize essa ferramenta quando precisar listar emails"
        ),
    ]


__all__ = ["get_email_tools"]