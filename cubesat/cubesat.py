import socket
import json
import sys
import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# allow importing from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from shared.logger import log_event

HOST = "127.0.0.1"
PORT = 5000

KEY = b"thisisasecretkey"  # same pre-shared key
LAST_SEQ = -1


def decrypt_payload(iv_b64, data_b64):
    iv = base64.b64decode(iv_b64)
    ciphertext = base64.b64decode(data_b64)

    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), 16)

    return json.loads(plaintext.decode())


def process_command(command):
    if command == "PING":
        return {"reply": "PONG"}

    elif command == "GET_TELEMETRY":
        return {"battery": 92, "temperature": 24, "status": "NOMINAL"}

    elif command == "REBOOT":
        return {"status": "REBOOTING"}

    else:
        return {"error": "UNKNOWN_COMMAND"}


def start_cubesat():
    global LAST_SEQ

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print("[CUBESAT] Waiting for Ground Station...")

    while True:
        conn, addr = server.accept()
        data = conn.recv(2048)

        if not data:
            conn.close()
            continue

        packet = json.loads(data.decode())
        log_event("CUBESAT", "RECEIVED_PACKET", packet)

        seq = packet.get("seq")

        # ---- REPLAY DEFENCE (before decryption) ----
        if seq is None or seq <= LAST_SEQ:
            response = {"error": "REPLAY_DETECTED"}
            log_event("CUBESAT", "REJECTED_REPLAY", packet)
        else:
            LAST_SEQ = seq
            payload = decrypt_payload(packet["iv"], packet["data"])
            log_event("CUBESAT", "DECRYPTED", payload)

            command = payload.get("command")
            response = process_command(command)

        log_event("CUBESAT", "RESPONSE", response)
        conn.send(json.dumps(response).encode())
        conn.close()


if __name__ == "__main__":
    start_cubesat()
