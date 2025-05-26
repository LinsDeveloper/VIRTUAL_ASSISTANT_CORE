from langchain import LLMChain, PromptTemplate
from langchain_community.chat_models import ChatOllama


class ExtractArtistMusicChain:
    def __init__(self, model_name="llama3:8b", temperature=0.7):
        llm = ChatOllama(model=model_name, temperature=temperature)

        prompt = PromptTemplate(
            input_variables=["text"],
            template=(
                "Você receberá um texto de um usuário pedindo para tocar uma música.\n"
                "Extraia o ARTISTA e o NOME DA MÚSICA.\n"
                "Responda SOMENTE no formato: artista|música\n"
                "Se não encontrar um deles, retorne 'desconhecido' no lugar.\n"
                "NÃO responda nada além disso.\n\n"
                "Exemplos:\n"
                "Input: 'Coloque a música fã número 1 do christian e cristiano.'\n"
                "Output: christian e cristiano|fã número 1\n\n"
                "Input: {text}\n"
                "Output:"
            )
        )

        self.chain = LLMChain(llm=llm, prompt=prompt)

    def run(self, text: str) -> tuple[str, str]:
        response = self.chain.invoke({"text": text})
        
        # Extrai o texto da resposta
        if isinstance(response, dict):
            # A chave pode variar, adapte conforme sua chain
            response_text = response.get("text") or response.get("output") or str(response)
        else:
            response_text = str(response)
        
        parts = response_text.strip().split("|")
        if len(parts) != 2:
            raise ValueError(f"Resposta inesperada do extractor: {response_text}")
        artist, music = parts
        return artist.strip(), music.strip()
