import asyncio
import websockets
import json
import pyautogui

SERVER_IP = "192.168.0.2"

async def handle_client(websocket, path):

    while True:
        data = await websocket.recv()
        data_dict = json.loads(data)
        mouse_position = data_dict.get("mouse_position", {})
        x = mouse_position.get("x", 0)
        y = mouse_position.get("y", 0)
        print(f"Received Data - Mouse Position: X={x}, Y={y}")
        if x != 0 and y != 0:
            pyautogui.moveTo(x, y) 
        

# Create a WebSocket server
start_server = websockets.serve(handle_client, SERVER_IP, 8765)
print(f"running server {SERVER_IP}:8765")

# Run the server
loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()
