from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import socket
import re
import threading

app = FastAPI()

# Enable CORS for Vue.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust with actual frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

relatives_data = []
connected_clients = []  # Store connected WebSocket clients

# Socket server to listen for EMG data


async def start_socket_server():
    s = socket.socket()
    s.bind(('192.168.50.231', 8000))
    print("Socket server running")
    s.listen(0)

    emg = []
    flag = False

    while True:
        client, addr = s.accept()

        while True:
            content = client.recv(1024).decode()

            if len(content) == 0:
                break
            else:
                if "EMG:" in content:
                    flag = True
                if flag:
                    emg.append(content)
                    flag = False
                if len(emg) > 10:
                    emg_readings = [re.search(r'EMG:(\d+\.\d+)', line).group(1)
                                    for line in emg if re.search(r'EMG:(\d+\.\d+)', line)]
                    emg_readings_float = [float(reading)
                                          for reading in emg_readings]
                    average_emg = sum(emg_readings_float) / \
                        len(emg_readings_float)
                    print("Average EMG: ", average_emg)

                    # Send EMG data to connected WebSocket clients
                    for ws_client in connected_clients:
                        try:
                            await ws_client.send_text(f"EMG: {content}")  # Send raw data
                            await ws_client.send_text(f"Average EMG: {average_emg}")  # Send average EMG
                        except:
                            connected_clients.remove(ws_client)

                    emg = []
        client.close()

# WebSocket endpoint for real-time EMG data


@app.websocket("/ws/emg")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    try:
        while True:
            # For now, we are just sending a test message every time
            await websocket.send_text(f"Sending real-time EMG data")
    except:
        connected_clients.remove(websocket)

# API to add relatives


@app.post("/add-relative/")
def add_relative(name: str, contact: str):
    relative = {"name": name, "contact": contact}
    relatives_data.append(relative)
    return {"message": "Relative added successfully"}

# API to get relatives


@app.get("/get-relatives/")
def get_relatives():
    return {"relatives": relatives_data}


socket_thread = threading.Thread(target=start_socket_server)
socket_thread.start()
if __name__ == "__main__":
    # Start the socket server in a separate thread

    # Start the FastAPI server (use 'uvicorn filename:app --reload' to run)
    import uvicorn
    uvicorn.run(app, host="192.168.50.231", port=80)
