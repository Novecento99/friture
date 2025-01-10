import socket
import numpy as np


class UDPReceiver:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ip, self.port))

    def receive_data(self, buffer_size):
        try:
            data, _ = self.socket.recvfrom(buffer_size)
            return data
        except Exception as e:
            print(f"Failed to receive data: {e}")
            return None

    def close(self):
        self.socket.close()


if __name__ == "__main__":
    a = UDPReceiver("127.0.0.1", 5005)
    while True:
        data = a.receive_data(1000)
        array = np.frombuffer(data, dtype=np.float64)
        if data:
            print(f"Received data: {array}")
            print(len(array))
        input("Press Enter to receive another message or Ctrl+C to exit")
