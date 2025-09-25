import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import time

# Load .env
load_dotenv()

BROKER = os.getenv("BROKER")
PORT = int(os.getenv("PORT"))
USERNAME = "juaaju"
PASSWORD = os.getenv("PASSWORD")
TOPIC = os.getenv("TOPIC")

def publish_message(message):
    print("[INFO] Membuat client MQTT...")
    client = mqtt.Client()
    client.tls_set()
    client.username_pw_set(USERNAME, PASSWORD)

    print(f"[INFO] Menghubungkan ke broker {BROKER}:{PORT} ...")
    client.connect(BROKER, PORT)

    client.loop_start()  # jalankan loop supaya publish bisa terkirim
    result = client.publish(TOPIC, message)
    result.wait_for_publish()  # tunggu pesan terkirim
    print(f"[INFO] Pesan terkirim: {message}")

    time.sleep(0.2)  # kasih jeda singkat agar loop sempat jalan
    client.loop_stop()
    client.disconnect()
    print("[INFO] Koneksi ditutup.")

if __name__ == "__main__":
    publish_message("Halo dari main.py")
