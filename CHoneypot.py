import socket
import datetime

# Define the ports to listen on
PORTS = [22, 80, 443]

# Create a socket for each port and start listening for incoming connections
sockets = []
for port in PORTS:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(5)
    print(f"Listening on port {port}...")
    sockets.append(s)

# Loop forever, accepting incoming connections and logging any data received
while True:
    for s in sockets:
        conn, addr = s.accept()
        print(
            f"Connection received from {addr[0]}:{addr[1]} on port {s.getsockname()[1]}...")
        # Log the connection information to a file
        with open("connections.log", "a") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(
                f"{timestamp} Connection received from {addr[0]}:{addr[1]} on port {s.getsockname()[1]}\n")
        # Receive and log any data sent by the client
        data = conn.recv(1024)
        if data:
            print(f"Data received:\n{data.decode()}")
            # Log the data to a file
            with open("data.log", "a") as f:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(
                    f"{timestamp} Data received from {addr[0]}:{addr[1]} on port {s.getsockname()[1]}:\n{data.decode()}\n")
        # Send a fake response to the client to make it think it has successfully connected
        conn.send(b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n")
        conn.close()
