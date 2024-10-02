import json
import socket
import threading
import rsa
import time
from pathlib import Path



class UDPClient:
    def __init__(self, server_ip, server_port, local_ip, local_port):
        """
        Initialize the UDP Client with server IP and port.
        :param server_ip: The IP address of the server.
        :param server_port: The port number of the server.
        :param local_ip: The IP address of the client.
        :param local_port: The port number of the client.
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.bind((local_ip, local_port))
        self.listening = False
        
        self.priKey = ""
        self.pubKey = ""
        self.pubKeyB = ""
        self.lastData = ""
        self.isMsg = False
        print(f"UDP Client initialized for server at {self.server_ip}:{self.server_port}")

    def send_data(self, jsonData):
        """
        Send a message to the server.
        :param jsonData: The data to be sent (JSON).
        """
        try:
            self.client_socket.sendto(jsonData, (self.server_ip, self.server_port))
            print(f"Message sent to {self.server_ip}:{self.server_port}")
        except Exception as e:
            print(f"Failed to send message: {e}")

    def _listen_for_messages(self, buffer_size=1024):
        """
        Private method to listen for messages from the server. Intended to run in a separate thread.
        :param buffer_size: The maximum amount of data to be received at once (default is 1024 bytes).
        """
        try:
            print("Started listening for messages from the server...")
            while self.listening:
                data, addr = self.client_socket.recvfrom(buffer_size)
                self.lastData = data
                # Intentar decodificar los datos como UTF-8
                try:
                    # Intentar cargar el JSON, si falla es porque no es un JSON válido
                    jsonData = data.decode('utf-8')
                    try:
                        self.lastData = json.loads(jsonData)
                        print(f"\nJSON message received from {addr}: {self.lastData}")
                    except json.JSONDecodeError:
                        self.lastData = data
                        print(f"\nReceived non-JSON message from {addr}: {jsonData}")
                except UnicodeDecodeError:
                    # Manejar el caso donde los datos no son UTF-8 o no son JSON
                    self.lastData = data
                    self.isMsg = True
                    print(f"Received non-text data from {addr}: {data}")
                finally:
                    self.listening = True
        except Exception as e:
            print(f"Error receiving message: {e}")

    def start_listening(self):
        #Start listening for server messages on a separate thread.
        self.listening = True
        self.listen_thread = threading.Thread(target=self._listen_for_messages)
        self.listen_thread.daemon = True  # Daemon thread will exit when the main program exits
        self.listen_thread.start()

    def stop_listening(self):
        # Stop listening for server messages.
        print(1)
        print(1)
        print(1)
        self.listening = False
        if self.listen_thread.is_alive():
            self.listen_thread.join()  # Wait for the listening thread to finish
        print("Stopped listening for server messages.")

    def close(self):
        #Close the UDP client socket and stop listening.
        print(2)
        print(2)
        print(2)
        self.stop_listening()
        self.client_socket.close()
        print("UDP Client socket closed.")
        
    