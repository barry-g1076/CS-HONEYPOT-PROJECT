import socket

# Define the ports to listen on
PORTS = [22, 80, 443]

# Create a socket for each port and start listening for incoming connections
for port in PORTS:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(5)
    print(f"Listening on port {port}...")

# Loop forever, accepting incoming connections and logging any data received
while True:
    for s in sockets:
        conn, addr = s.accept()
        print(f"Connection received from {addr[0]}:{addr[1]} on port {port}...")
        data = conn.recv(1024)
        print(f"Data received:\n{data.decode()}")
