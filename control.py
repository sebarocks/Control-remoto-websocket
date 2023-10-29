import asyncio
import websockets
import json
import tkinter as tk
import pyautogui
import threading

# Global variable to track whether the capture is active
capture_active = False

# Global variables to track mouse click counts and position
click_count = 0
mouse_position = (0, 0)

def resizeXY(x,y):
    x_resize = ( x - window.winfo_x() ) # // window.winfo_width()
    y_resize = ( y - window.winfo_y() ) # // window.winfo_height()
    return x_resize, y_resize


# Function to update the global mouse_position variable
def record_mouse_position(event):
    global mouse_position
    x, y = pyautogui.position()
    mouse_position = resizeXY(x,y)

# Function to handle mouse click events and update the click count
def record_click(event):
    global click_count
    click_count += 1

# Function to start/stop capturing and toggle the button text
def toggle_capture():
    global capture_active
    if capture_active:
        capture_active = False
        capture_button.config(text="Start Capture")
        window.unbind("<Escape>")
    else:
        capture_active = True
        capture_button.config(text="Stop Capture")
        window.bind("<Escape>", stop_capture)

def stop_capture(event):
    global capture_active
    capture_active = False
    capture_button.config(text="Start Capture")
    window.config(cursor="")
    window.unbind("<Escape>")  # Unbind the Escape key

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
window.geometry("800x600")
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

# Start updating mouse position and click count in real-time
update_mouse_position_label()
update_click_count_label()

# Bind mouse click events to the record_click function
window.bind("<Button-1>", record_click)
window.bind("<Motion>", record_mouse_position)


# Function to send mouse data to the server
async def send_mouse_data():
    async with websockets.connect('ws://192.168.0.2:8765') as websocket:
        while capture_active:
            data = {
                "click_count": click_count,
                "mouse_position": mouse_position
            }
            await websocket.send(json.dumps(data))
            await asyncio.sleep(0.1)

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