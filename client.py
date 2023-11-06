import asyncio
import websockets
import json
import pyautogui

import sys

SERVER_IP = "192.168.0.2"

if len(sys.argv) > 1:
    SERVER_IP = sys.argv[1]

SCREEN_SIZE = pyautogui.size()

def translate_position(x,y):
    global SCREEN_SIZE
    x_screen = int(SCREEN_SIZE[0] * x)
    y_screen = int(SCREEN_SIZE[1] * y)
    return (x_screen, y_screen)

async def handle_client(websocket, path):

    while True:
        data = await websocket.recv()
        data_dict = json.loads(data)
        mouse_position = data_dict.get("mouse_position", {})
        clicks = data_dict.get("click_count")
        x = mouse_position.get("x", 0)
        y = mouse_position.get("y", 0)
        print(f"Received Data: X={x}, Y={y}, Clicks={clicks}")
        if x != 0 and y != 0:
            m_pos = translate_position(x,y)
            pyautogui.moveTo(m_pos[0], m_pos[1])
        if clicks > 0:
            pyautogui.click(clicks=clicks)
        

# Create a WebSocket server
start_server = websockets.serve(handle_client, SERVER_IP, 8765)
print(f"running server {SERVER_IP}:8765")

# Run the server
loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()
