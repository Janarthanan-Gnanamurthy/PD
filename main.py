from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model import model
import numpy as np
import pandas as pd
import requests
import asyncio
import json
from typing import List, Dict
from dotenv import load_dotenv
import google.generativeai as genai
import os


load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class MessageRequest(BaseModel):
    message: str


SYSTEM_PROMPT = (
    "You are a supportive and empathetic assistant designed to help people with Parkinson's disease. and also can solve all logical problems as well"
    "answer only the questions asked"
    "this website helps to predict the tremors and bradykinisia using the wearable device"
    "we use sensors such as EMG, BPM and accelerometer "
    "this website can alert to your loved ones and hospitals incase of emergency"
)


class SensorData(BaseModel):
    tremor: float
    BPM: int
    EMG: float


class ContactBase(BaseModel):
    name: str
    phone: str
    email: str
    relationship: str


class Contact(ContactBase):
    id: str


# This would be replaced with a database in a production environment
patients: Dict[str, List[Contact]] = {}
connected_clients = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            sensor_data = json.loads(data)

            # Prepare the data for prediction (reshape the data as needed by your model)
            input_data = np.array(
                [[sensor_data['tremor'], sensor_data['BPM'], sensor_data['EMG']]])

            # Make a prediction (you might need to scale or transform the data first)
            severity_prediction = model.predict(
                pd.DataFrame({'Value 1': [sensor_data['tremor']]}))

            # Append the severity prediction to the sensor data
            sensor_data_with_severity = {
                **sensor_data,  # Original sensor data
                # Add severity level to the data
                "severity_level": int(severity_prediction[0])
            }
            print(sensor_data_with_severity)
            # Send an alert if the severity level is high (e.g., 4)
            if severity_prediction == 3:
                await call_feature()

            # Send the updated sensor data along with severity to all connected clients
            for ws_client in connected_clients:
                try:
                    await ws_client.send_text(json.dumps(sensor_data_with_severity))
                except:
                    connected_clients.remove(ws_client)

    except Exception as e:
        print(f"Error: {e}")


@app.post("/patient/{patient_id}/contacts")
async def add_contact(patient_id: str, contact: ContactBase):
    if patient_id not in patients:
        patients[patient_id] = []
    # Generate a new ID for the contact
    new_contact = Contact(
        id=str(len(patients[patient_id]) + 1), **contact.dict())
    patients[patient_id].append(new_contact)
    return {"message": "Contact added successfully", "contact": new_contact}


@app.get("/patient/{patient_id}/contacts")
async def get_contacts(patient_id: str):
    return patients.get(patient_id, [])


@app.delete("/patient/{patient_id}/contacts/{contact_id}")
async def remove_contact(patient_id: str, contact_id: str):
    if patient_id not in patients:
        return {"error": "Patient not found"}, 404

    contact_list = patients[patient_id]
    contact_to_remove = next(
        (contact for contact in contact_list if contact.id == contact_id), None)

    if not contact_to_remove:
        return {"error": "Contact not found"}, 404

    patients[patient_id] = [
        contact for contact in contact_list if contact.id != contact_id]
    return {"message": "Contact removed successfully"}


async def send_alert(patient_id: str):
    contacts = patients.get(patient_id, [])
    # In a real application, you would implement the logic to send
    # messages or make calls to the contacts here
    print(f"Alert sent to {len(contacts)} contacts for patient {patient_id}")


@app.get("/call/")
def call_feature():
    print("Emergency call has been initiated")
    key = "332244e2-6b42-4747-99a6-18cfc66027db"
    secret = "cpKCvV7t50ON6eNrf7YUAQ=="
    from_number = "+447441421533"
    to = "+919043324402"
    locale = "en-US"
    url = "https://calling.api.sinch.com/calling/v1/callouts"
    # to = "+91" + str(num)
    payload = {
        "method": "ttsCallout",
        "ttsCallout": {
            "cli": from_number,
            "destination": {
                "type": "number",
                "endpoint": to
            },
            "locale": locale,
            "text": "This is a emergency your freind with PD is in Danger"
        }
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(
        url, json=payload, headers=headers, auth=(key, secret))

    data = response.json()
    print(data)


@app.post("/chat")
def chat_with_gemini(request: MessageRequest):
    model = genai.GenerativeModel("gemini-pro")

    # Generate the response using the system prompt and user input
    response = model.generate_content(
        f"{SYSTEM_PROMPT} User: {request.message}")

    return {"response": response.text}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.50.231", port=8000)
