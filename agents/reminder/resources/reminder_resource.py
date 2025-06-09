from typing import Optional
from agents.reminder.chains.reminder_chain import ReminderBodyBuilderChain
from langchain.tools import Tool
from models.AgentResponseModel import ResponseModel
from cachetools import TTLCache
import requests


token_cache = TTLCache(maxsize=1000, ttl=6000)


def create_reminder_from_query(query: str) -> ResponseModel:
    """
    Extrai os dados de lembrete com uma chain e envia via POST para o backend.
    """
    extractor_chain = ReminderBodyBuilderChain()

    try:
        token = token_cache.get("accessToken")
        if not token:
            return ResponseModel(success=False, response="❌ Token de autenticação não encontrado no cache.")

        reminder_data = extractor_chain.run(query)
        body = {
            "title": reminder_data.get("title"),
            "message": reminder_data.get("message"),
            "reminder_timer": reminder_data.get("reminder_timer")
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            "http://localhost:8080/api/v1/auth/integration-reminders",
            json=body,
            headers=headers
        )
        response.raise_for_status()

        return ResponseModel(success=True, response="⏰ Lembrete criado com sucesso!")

    except Exception as e:
        return ResponseModel(success=False, response=f"❌ Erro ao criar lembrete: {str(e)}")
