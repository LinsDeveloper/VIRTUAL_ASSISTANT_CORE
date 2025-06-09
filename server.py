from websockets.server import serve, WebSocketServerProtocol
from urllib.parse import urlparse, parse_qs
import asyncio
import json

from agents.main.main_agent import AgentMain
from helpers.cache.cache_store import token_cache


class CustomProtocol(WebSocketServerProtocol):
    async def process_request(self, path, request_headers):
        query = parse_qs(urlparse(path).query)
        token = query.get("token", [None])[0]
        print(f"Token recebido: {token}")
        if token:
            token_cache["accessToken"] = token
        return None  # Aceita a conexão


async def handle_connection(websocket: WebSocketServerProtocol):
    agent = AgentMain()
    try:
        async for message in websocket:
            data = json.loads(message)
            prompt = data.get("prompt")
            print(f"Prompt que chegou no server: {prompt}")

            if prompt:
                response = agent.run(prompt)
                await websocket.send(json.dumps({"response": response}))

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        pass


async def main():
    async with serve(
        handle_connection,
        "0.0.0.0",
        8080,
        create_protocol=CustomProtocol, 
        ping_interval=None
    ):
        print("Servidor WebSocket iniciado na porta 8080")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
