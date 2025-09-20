import paho.mqtt.client as mqtt
import time
import os
from dotenv import load_dotenv

# Load file .env
load_dotenv()

# Ambil value dari env
BROKER = os.getenv("BROKER")
PORT = int(os.getenv("PORT"))
USERNAME = "juaaju"
PASSWORD = os.getenv("PASSWORD")
TOPIC = os.getenv("TOPIC")

client = mqtt.Client()
client.tls_set()
client.username_pw_set(USERNAME, PASSWORD)
client.connect(BROKER, PORT)
client.loop_start()  # mulai loop agar bisa publish

try:
    while True:
        message = input("Ketik pesan untuk dikirim: ")
        client.publish(TOPIC, message)
        print(f"Sent: {message}")
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
