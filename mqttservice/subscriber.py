import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

# Load file .env
load_dotenv()

# Ambil value dari env
BROKER = os.getenv("BROKER")
PORT = int(os.getenv("PORT"))
USERNAME = "juaaju"
PASSWORD = os.getenv("PASSWORD")
TOPIC = os.getenv("TOPIC")

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)  # subscribe ke topic
    print(f"Subscribed to {TOPIC}")

def on_message(client, userdata, msg):
    print(f"Received: {msg.topic} -> {msg.payload.decode()}")

client = mqtt.Client()
client.tls_set()  # TLS / SSL
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)
client.loop_forever()
