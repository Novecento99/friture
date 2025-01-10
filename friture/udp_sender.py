import socket


# example of a class that sends data over UDP
class UDPSender:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_data(self, data):
        try:
            self.socket.sendto(data, (self.ip, self.port))
        except Exception as e:
            print(f"Failed to send data: {e}")

    def close(self):
        self.socket.close()


if __name__ == "__main__":
    a = UDPSender("127.0.0.1", 5005)
    while True:
        a.send_data(b"Hello, World!")
        print("Message sent")
        input("Press Enter to send another message or Ctrl+C to exit")

    a.close()
