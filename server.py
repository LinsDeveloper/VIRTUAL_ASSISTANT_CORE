import asyncio
import json
import websockets

from agents.main.main_agent import invoke_agent_main



async def handle_connection(websocket, path=None):  
    try:
        async for message in websocket:
            data = json.loads(message)
            prompt = data.get("prompt")
            print(f"prompt que chegou no server: {prompt}")

            if prompt:
                response = invoke_agent_main(prompt)

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
