# This is a python script.
# Author: PRATHAM BHISE
# This python script is used to establish server side socket;
# And manage clients connected to the server.


"""Imports-> constants from connection_details.py; threading module; socket module; time module"""


from connection_details import HOST, PORT
import threading
import socket
import time


class ServerDefinition:
    def __init__(self, host_details: str, port_no: int) -> None:
        """
            Initialise socket object for server side.
            'socket.socket()' class from socket module.
            'AF_INET' - AddressFamily for internet socket.
            'SOCK_STREAM' - SocketKind for TCP protocol.

            :param host_details: str
            :param port_no: int
            :return: None
        """
        self.server_main = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_address = host_details
        self.host_port_no = port_no
        self.clients_all = []

    def server_run(self) -> None:
        """
            Commencement method for instance of ServerDefinition.
            :return: None
        """
        self.server_launch()
        server_run_thread = threading.Thread(target=self.client_new_accept, daemon=True)
        server_manage_thread = threading.Thread(target=self.server_manage)
        server_manage_thread.start()
        time.sleep(1)
        server_run_thread.start()

    def server_launch(self) -> None:
        """
            Bind host address and port number to the socket.
            Begin listening on server socket.

            :return: None
        """
        self.server_main.bind((self.host_address, self.host_port_no))
        self.server_main.listen()
        print("--- SERVER CODES ---")
        print("EXIT SERVER: quit()")
        print("DISPLAY CLIENTS: clients()")
        print(f"\n--- SERVER STARTED AT {self.host_address}:{self.host_port_no} ---\n")

    def server_receive(self, client: dict) -> None:
        """
            Receive broadcasts from the client.
            Notice any ConnectionResetError errors.

            :param client: dict
            :return: None
        """
        while True:
            try:
                # broadcasting message
                message = client['socket'].recv(1024).decode('ascii')
                self.server_broadcast(message)
            except AttributeError:
                print("THERE WAS AN AttributeError")
            except ConnectionResetError:
                print("\nA CONNECTION WAS RESET")
                self.client_manage(client)
                break

    def server_broadcast(self, message: str) -> None:
        """
            Broadcast message to all clients.

            :param message: str
            :return: None
        """
        for client in self.clients_all:
            client['socket'].send(message.encode('ascii'))

    def server_manage(self) -> None:
        """
            Accept request to close the server.
            Display all active clients.

            :return: None
        """
        while True:
            server_code = input("")
            if server_code == "quit()":
                self.server_broadcast(server_code)
                exit()
            elif server_code == "clients()":
                print("ONLINE CONNECTIONS")
                for client in self.clients_all:
                    print("NAME:", client['name'])

    def client_new_accept(self) -> None:
        """
            Verify and accept any request to connect to the server.

            :return: None
        """
        while True:
            print("Waiting for a new connection...")
            new_client_socket, new_client_address = self.server_main.accept()

            new_client_socket.send("NEW_CLIENT_REQUEST".encode("ascii"))
            client_name = new_client_socket.recv(1024).decode("ascii")
            new_client = {
                "name": client_name,
                "address": new_client_address,
                "socket": new_client_socket,
            }
            self.client_welcome(new_client)

    def client_welcome(self, client: dict) -> None:
        """
            Display the welcome message for the new connection.

            :param client: dict
            :return: None
        """
        print("\n------- New Client -------")
        print(f"NAME: {client['name']}")
        print(f"ADDRESS: {client['address'][0]}:{client['address'][1]}")
        print("---------------------------\n")
        message = f"---You have joined the chatroom [{self.host_address}:{self.host_port_no}]---" \
                  f"\n---with NAME: {client['name']} | ADDRESS: [{client['address'][0]}:{client['address'][1]}]---\n"
        client['socket'].send(message.encode("ascii"))
        self.server_broadcast(f"SERVER: {client['name']} has joined the chat!")
        self.clients_all.append(client)
        thread = threading.Thread(target=self.server_receive, args=(client,))
        thread.start()

    def client_manage(self, client: dict) -> None:
        """
            Handle the closed connections.

            :param client: dict
            :return: None
        """
        self.clients_all.remove(client)
        print("\n------- Client Exit -------")
        print(f"NAME: {client['name']}")
        print(f"ADDRESS: {client['address'][0]}:{client['address'][1]}")
        print("---------------------------\n")
        print("Waiting for a new connection...")
        message = f"\nSERVER: -{client['name']}- has left the chatroom, xoxo!"
        self.server_broadcast(message)
        client['socket'].close()


if __name__ == "__main__":
    # help(ServerDefinition)
    server1 = ServerDefinition(HOST, PORT)

    try:
        server1.server_run()
    except (KeyboardInterrupt, SystemExit):
        exit()
