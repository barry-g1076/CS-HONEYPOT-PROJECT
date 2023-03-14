import socket
import datetime
import subprocess
import smtplib
from email.mime.text import MIMEText
from scapy.all import *

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

# Initialize the packet capture filter and intrusion detection rules
capture_filter = "tcp port 22 or tcp port 80 or tcp port 443"
intrusion_rules = {
    "ET POLICY Binary Download Smuggling": {
        "ports": [80, 443],
        "payloads": [b"Content-Disposition: attachment", b"Content-Disposition: form-data; name="]
    },
    "ET INFO Session Traversal Utilities for NAT (STUN Binding Request)": {
        "ports": [3478],
        "payloads": [b"\x00\x01\x00\x00\x21\x12\xa4\x42\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"]
    }
}

# Initialize the email alert settings
alert_email = "youremail@example.com"
alert_password = "yourpassword"
alert_recipients = ["youremail@example.com"]

# Function to send email alerts


def send_alert(subject, message):
    msg = MIMEText(message)
    msg['From'] = alert_email
    msg['To'] = ", ".join(alert_recipients)
    msg['Subject'] = subject
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(alert_email, alert_password)
    server.sendmail(alert_email, alert_recipients, msg.as_string())
    server.quit()


# Loop forever, accepting incoming connections, capturing packets, and detecting intrusions
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
            # Check for intrusion attempts
            if s.getsockname()[1] in [80, 443]:
                for rule in intrusion_rules.values():
                    if s.getsockname()[1] in rule["ports"] and data.startswith(rule["payload"]):
                        # Intrusion detected, log the event and send an alert
                        print(
                            f"Intrusion detected on port {s.getsockname()[1]}: {rule['name']}")
                        with open("intrusions.log", "a") as f:
                            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            f.write(
                                f"{timestamp} Intrusion detected on port {s.getsockname()[1]}: {rule['name']}\n")
                        send_alert("Honeypot Alert: Intrusion Detected",
                                   f"Intrusion detected on port {s.getsockname()[1]}: {rule['name']}")
