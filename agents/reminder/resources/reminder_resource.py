from typing import Optional
from agents.reminder.chains.reminder_chain import ReminderBodyBuilderChain
from langchain.tools import Tool
from models.AgentResponseModel import ResponseModel
import requests
from helpers.cache.cache_store import token_cache




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

        if not all(k in reminder_data for k in ("title", "message", "reminder_timer")):
            raise ValueError("❌ O modelo não retornou os campos esperados (title, message, reminder_timer)")

        body = {
            "title": reminder_data["title"],
            "message": reminder_data["message"],
            "reminder_timer": reminder_data["reminder_timer"]
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            "http://localhost:5186/api/v1/auth/integration-reminder",
            json=body,
            headers=headers
        )
        response.raise_for_status()

        return ResponseModel(success=True, response="⏰ Lembrete criado com sucesso!")

    except Exception as e:
        return ResponseModel(success=False, response=f"❌ Erro ao criar lembrete: {str(e)}")

