import asyncio
import websockets
import json
import tkinter as tk
from tkinter import messagebox
import threading

# Global variable to track whether the capture is active
capture_active = False

# Global variables to track mouse click counts and position
click_count = 0
mouse_position = (0, 0)

def resizeXY(x,y):
    x_resize =  x / 600 
    y_resize =  y / 480 
    return x_resize, y_resize


# Function to handle mouse motion within the canvas area
def on_canvas_motion(event):
    global mouse_position
    if capture_active:
        x, y = event.x, event.y
        mouse_position = resizeXY(x, y)

# Function to handle mouse clicks within the canvas area
def on_canvas_click(event):
    if capture_active:
        global click_count
        click_count += 1

# Function to toggle mouse capture
def toggle_capture():
    global capture_active
    if capture_active:
        capture_active = False
        capture_button.config(text="Start Capture")
        canvas.config(bg="lightgray")  # Change the canvas color to indicate inactive state
    else:
        capture_active = True
        capture_button.config(text="Stop Capture")
        canvas.config(bg="green")  # Change the canvas color to indicate active state


def update_mouse_position_label():
    if capture_active:
        x, y = mouse_position
        mouse_position_label.config(text=f"Mouse Position: X={x}, Y={y}")
    mouse_position_label.after(1000, update_mouse_position_label)

def update_click_count_label():
    global click_count
    if capture_active:
        click_count_label.config(text=f"Click Count: {click_count}")
    click_count_label.after(1000, update_click_count_label)

# Create a Tkinter window with an 800x600 size
window = tk.Tk()
window.geometry("600x580")
window.title("Mouse Movement Capture")

# Create a label for displaying mouse coordinates
mouse_position_label = tk.Label(window, text="Mouse Position: X=0, Y=0")
mouse_position_label.pack()

# Create a label for displaying mouse click count
click_count_label = tk.Label(window, text="Click Count: 0")
click_count_label.pack()

# Create a button to start/stop capture
capture_button = tk.Button(window, text="Start Capture", command=toggle_capture)
capture_button.pack()

# Create a canvas below the button for the rectangular area
canvas = tk.Canvas(window, bg="lightgray", width=600, height=480)
canvas.pack()

# Start updating mouse position and click count in real-time
update_mouse_position_label()
update_click_count_label()

# Bind mouse motion and clicks within the canvas area
canvas.bind("<Motion>", on_canvas_motion)
canvas.bind("<Button-1>", on_canvas_click)

SERVER_IP = "192.168.0.2"

# Function to send mouse data to the server
async def send_mouse_data():
    
    try:            
        async with websockets.connect(f"ws://{SERVER_IP}:8765") as websocket:
            while True:                
                if capture_active:
                    global click_count
                    data = {
                        "click_count": click_count,
                        "mouse_position": {
                            "x" : mouse_position[0],
                            "y" : mouse_position[1]
                        }
                    }
                    await websocket.send(json.dumps(data))
                    click_count = 0
                await asyncio.sleep(0.1)
    except ConnectionRefusedError as e:
        print(e)
        messagebox.showerror("Error de Conexion", e) 

# Create a task for the main function
async def main_task():
    await send_mouse_data()

# Function to run the asyncio event loop for the main task
def run_asyncio_loop():
    asyncio.run(main_task())

# Create a separate thread for the WebSocket client
if __name__ == "__main__":
    thread = threading.Thread(target=run_asyncio_loop)
    thread.start()

    # Run the Tkinter main loop in the main thread
    window.mainloop()