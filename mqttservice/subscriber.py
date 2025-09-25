import os
import threading
import queue
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from playsound import playsound

# Load file .env
load_dotenv()

BROKER = os.getenv("BROKER")
PORT = int(os.getenv("PORT"))
USERNAME = "juaaju"
PASSWORD = os.getenv("PASSWORD")
TOPIC = os.getenv("TOPIC")

# Queue untuk antrian suara
sound_queue = queue.Queue()

# File suara tunggal
MP3_FILE = "alert_lof.mp3"

def sound_worker():
    """Worker yang memutar suara satu per satu sesuai antrian"""
    while True:
        _ = sound_queue.get()  # ambil item dari queue (isinya dummy, karena filenya tetap sama)
        if os.path.exists(MP3_FILE):
            try:
                playsound(MP3_FILE)
            except Exception as e:
                print(f"Gagal memutar {MP3_FILE}: {e}")
        else:
            print(f"File {MP3_FILE} tidak ditemukan.")
        sound_queue.task_done()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)
    print(f"Subscribed to {TOPIC}")

def on_message(client, userdata, msg):
    pesan = msg.payload.decode().strip()
    print(f"Received: {msg.topic} -> {pesan}")
    # cukup masukkan sinyal ke antrian
    sound_queue.put(1)

# Jalankan worker di thread terpisah
threading.Thread(target=sound_worker, daemon=True).start()

# Setup MQTT client
client = mqtt.Client()
client.tls_set()
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)
client.loop_forever()
