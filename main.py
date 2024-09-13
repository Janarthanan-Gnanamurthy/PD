from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json
from typing import List

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class SensorData(BaseModel):
    tremor: float
    BPM: int
    EMG: float


class Contact(BaseModel):
    name: str
    phone: str
    email: str


patients = {}  # This would be replaced with a database in a production environment
connected_clients = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            sensor_data = json.loads(data)
            print(f"Received data: {sensor_data}")
            # Process the data as needed
            # For example, you could check if the tremor value exceeds a threshold
            # if sensor_data["tremor"] > 400:  # Adjust this threshold as needed
            # await send_alert(data)
            for ws_client in connected_clients:
                try:
                    await ws_client.send_text(data)
                except:
                    connected_clients.remove(ws_client)
    except Exception as e:
        print(f"Error: {e}")


@app.post("/patient/{patient_id}/contacts")
async def add_contact(patient_id: str, contact: Contact):
    if patient_id not in patients:
        patients[patient_id] = []
    patients[patient_id].append(contact)
    return {"message": "Contact added successfully"}


@app.get("/patient/{patient_id}/contacts")
async def get_contacts(patient_id: str):
    return patients.get(patient_id, [])


async def send_alert(patient_id: str):
    contacts = patients.get(patient_id, [])
    # In a real application, you would implement the logic to send
    # messages or make calls to the contacts here
    print(f"Alert sent to {len(contacts)} contacts for patient {patient_id}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.50.231", port=8000)
