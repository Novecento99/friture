import socket


# example of a class that receveis data over UDP


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


a = UDPReceiver("127.0.0.1", 5005)
while True:
    data = a.receive_data(1)
    if data:
        print(f"Received data: {data}")
    input("Press Enter to receive another message or Ctrl+C to exit")
