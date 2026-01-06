import socket
import json
import sys
import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# allow importing from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from shared.logger import log_event

HOST = "127.0.0.1"
PORT = 5000

KEY = b"thisisasecretkey"  # 16 bytes = AES-128
SEQ_NUM = 0


def encrypt_payload(payload: dict):
    iv = get_random_bytes(16)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(json.dumps(payload).encode(), 16))

    return iv, ciphertext


def send_command(command):
    global SEQ_NUM
    SEQ_NUM += 1

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    payload = {"command": command}
    iv, encrypted_payload = encrypt_payload(payload)

    packet = {
        "seq": SEQ_NUM,
        "iv": base64.b64encode(iv).decode(),
        "data": base64.b64encode(encrypted_payload).decode(),
    }

    print(f"[GROUND] Sending encrypted packet: seq={SEQ_NUM}")
    log_event("GROUND", "ENCRYPTED_SEND", packet)

    client.send(json.dumps(packet).encode())

    response = json.loads(client.recv(1024).decode())
    print(f"[GROUND] Response: {response}")
    log_event("GROUND", "RECEIVED", response)

    client.close()


if __name__ == "__main__":
    send_command("PING")
    send_command("GET_TELEMETRY")
    send_command("REBOOT")
