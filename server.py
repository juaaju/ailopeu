import datetime
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def home():
    return "Server deteksi aktif..."

# Fungsi ini dipanggil kalau ada deteksi bahaya
def send_alert(message):
    data = {
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "alert": message
    }
    print("Mengirim alert:", data)
    socketio.emit("alert_event", data)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
