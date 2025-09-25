import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

# Load .env
load_dotenv()

BROKER = os.getenv("BROKER")
PORT = int(os.getenv("PORT"))
USERNAME = "juaaju"
PASSWORD = os.getenv("PASSWORD")
TOPIC = os.getenv("TOPIC")

def publish_message(message):
    """Publish pesan sekali ke broker"""
    client = mqtt.Client()
    client.tls_set()
    client.username_pw_set(USERNAME, PASSWORD)
    client.connect(BROKER, PORT)
    client.publish(TOPIC, message)
    client.disconnect()
    print(f"Sent: {message}")
