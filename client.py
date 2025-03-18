import asyncio
import websockets
import json

async def send_message(prompt):
    async with websockets.connect("ws://localhost:8080") as websocket:
        await websocket.send(json.dumps({"prompt": prompt}))
        
        response = await websocket.recv()
        print(f"Resposta recebida do servidor: {response}")
        
        try:
            data = json.loads(response)
            print(f"Dados convertidos com sucesso: {data}")
        except json.JSONDecodeError:
            print("Erro ao converter a resposta para JSON. Resposta recebida:", response)



async def main():
    print("Conectando ao servidor WebSocket...")
    while True:
        prompt = input("Você: ")
        if prompt.lower() in ['sair', 'exit', 'quit']:
            print("Encerrando conexão...")
            break
        await send_message(prompt)


if __name__ == "__main__":
    asyncio.run(main())
