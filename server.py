import asyncio
import json
import websockets
from langchain.llms import Ollama
from langchain.agents import initialize_agent, Tool, AgentType

llm = Ollama(model="llama3:8b", temperature=0.7)

def responder_pergunta(pergunta: str) -> str:
    return llm(pergunta)

tools = [
    Tool(
        name="Respondedor de Perguntas",
        description="Responde perguntas gerais sobre o mundo.",
        func=responder_pergunta
    )
]

agent = initialize_agent(tools, llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, max_iterations=3)

async def handle_connection(websocket, path=None):  
    try:
        async for message in websocket:
            data = json.loads(message)
            prompt = data.get("prompt")
            print(f"prompt que chegou no server: {prompt}")

            if prompt:
                response = agent.run(prompt)

                await websocket.send(json.dumps({"response": response}))

    except websockets.ConnectionClosedOK:
        print("Conexão encerrada normalmente.")
    except Exception as e:
        print(f"Erro: {e}")



async def main():
    async with websockets.serve(handle_connection, "localhost", 8080, ping_interval=None):
        print("Servidor WebSocket iniciado na porta 8080")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
