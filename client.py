import asyncio
import websockets
import json

async def handle_client(websocket, path):
    
    while True:
        data = await websocket.recv()
        data_dict = json.loads(data)
        mouse_position = data_dict.get("mouse_position", {})
        x = mouse_position.get("x", 0)
        y = mouse_position.get("y", 0)
        print(f"Received Data - Mouse Position: X={x}, Y={y}")

# Create a WebSocket server
start_server = websockets.serve(handle_client, "localhost", 8765)
print('running server localhost:8765')

# Run the server
loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()
