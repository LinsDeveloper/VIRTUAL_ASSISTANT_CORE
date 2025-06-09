from langchain import LLMChain, PromptTemplate
from langchain_community.chat_models import ChatOllama
from datetime import datetime, timedelta
from core.enum.llm_type_enum import InstanceTypeLLM
from llms.main_llm import build_model
from dotenv import load_dotenv
import os
load_dotenv()

class ReminderBodyBuilderChain:
    def __init__(self):
        llm = build_model(InstanceTypeLLM.OLLAMA, "llama3:8b", temperature=0.7)

        prompt = PromptTemplate(
            input_variables=["text", "current_time"],
            template=(
                "Você receberá uma solicitação de lembrete do usuário.\n"
                "Gere as seguintes informações no formato: Título|Mensagem|DataHoraUTC\n"
                "Regras:\n"
                "- O TÍTULO deve ser uma frase curta sobre o que lembrar (ex: lembrete de tomar remédio).\n"
                "- A MENSAGEM deve ser criativa e gentil, lembrando o usuário da ação.\n"
                "- A DataHoraUTC deve ser um datetime em formato ISO 8601 (ex: 2025-06-09T20:30:00Z), baseado no tempo atual que é: {current_time}.\n"
                "- NÃO retorne nada além do formato esperado.\n\n"
                "Exemplo:\n"
                "Input: 'Me lembre daqui 1 minuto de tomar o remédio'\n"
                "Output: lembrete de tomar remédio|Hora de cuidar da sua saúde! Não esqueça de tomar o remédio.|2025-06-09T20:30:00Z\n\n"
                "Input: {text}\n"
                "Output:"
            )
        )

        self.chain = LLMChain(llm=llm, prompt=prompt)

    def run(self, text: str) -> dict:
        current_utc = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        response = self.chain.invoke({"text": text, "current_time": current_utc})
        print("Resposta do modelo:", response)

        if isinstance(response, dict):
            response_text = response.get("text") or response.get("output") or str(response)
            print("Resposta do modelo2:", response_text)
        else:
            response_text = str(response)

        parts = response_text.strip().split("|")
        if len(parts) != 3:
            raise ValueError(f"Resposta inesperada do extractor: {response_text}")

        title, message, iso_datetime = map(str.strip, parts)

        try:
            reminder_time = datetime.fromisoformat(iso_datetime.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError(f"Formato de data inválido: {iso_datetime}")

        return {
            "Title": title,
            "Message": message,
            "ReminderTimer": reminder_time
        }
