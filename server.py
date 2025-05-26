import asyncio
import json
import websockets

from agents.main.main_agent import AgentMain


async def handle_connection(websocket, path=None):  
    try:
        agent = AgentMain()
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
    async with websockets.serve(handle_connection, "0.0.0.0", 8080, ping_interval=None):
        print("Servidor WebSocket iniciado na porta 8080")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
