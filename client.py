# This is a python script.
# Author: PRATHAM BHISE
# This python script is used to manage client side socket;
# While communicating with server socket


"""Imports-> constants from connection_details.py; threading module; socket module."""


from connection_details import HOST, PORT
import threading
import socket


class ClientDefinition:
    def __init__(self, destination_details: str, port_no: int) -> None:
        """
            Initialise socket object for client side.
            'socket.socket()' class from socket module.
            'AF_INET' - AddressFamily for internet socket.
            'SOCK_STREAM' - SocketKind for TCP protocol.

            :param destination_details: str
            :param port_no: int
            :return: None
        """
        self.client_main = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.destination_address = destination_details
        self.destination_port_no = port_no
        self.client_name = input("ENTER YOUR NAME: ")

    def client_run(self) -> None:
        """
            Commencement method for instance of ClientDefinition.

            :return: None
        """
        connection = self.client_connect()
        # establish connection with the server
        if connection != "SUCCESS":
            exit()
        print("---- WELCOME ----")
        print("ENTER 'quit()' TO EXIT")
        receive_thread = threading.Thread(target=self.client_receive, args=(True,))
        receive_thread.start()
        # sub-thread 1 => receive_thread; self.client_receive(True)
        send_thread = threading.Thread(target=self.client_send, args=(True,))
        send_thread.start()
        # sub-thread 2 => send_thread; self.client_send(True)

    def client_connect(self) -> str:
        """
            Establish connection between self.client_main socket and server socket.

            :return: str
        """
        try:
            self.client_main.connect((self.destination_address, self.destination_port_no))
            # socket.connect(destination_address_tuple)
            return "SUCCESS"
        except ConnectionRefusedError:
            # TODO: Make sure there is a server socket active.
            print(f"Your connection was refused by {self.destination_address}:{self.destination_port_no}")
            print("Please try again later with different address or port number.")

    def client_exit(self, flag: bool) -> None:
        """
            Send negative boolean to the forever while loops to terminate the sub-threads.
            End the script.

            :param flag: bool
            :return: None
        """
        self.client_main.close()
        self.client_receive(flag)
        self.client_send(flag)
        exit()

    def client_receive(self, flag_condition: bool) -> None:
        """
            Receive broadcasts from the server.
            Send self.client_name to the server.
            Notice if the server is not active.

            :param flag_condition: bool
            :return: None
        """
        while flag_condition:
            try:
                message = self.client_main.recv(1024).decode("ascii")
                if message == "NEW_CLIENT_REQUEST":
                    self.client_main.send(self.client_name.encode("ascii"))
                elif message == "quit()":
                    print("--- SERVER HAS SHUTDOWN ---")
                    self.client_exit(False)
                else:
                    print(message)
            except OSError:
                # close connection if error occurs while
                # trying to receive when server is closed
                print("SERVER NO LONGER RESPONDING...")
                self.client_main.close()
                self.client_exit(False)

    def client_send(self, flag_condition) -> None:
        """
            Get messages from the user.
            Broadcast messages to the server.
            Notice if the user wants to quit.

            :param flag_condition: bool
            :return: None
        """
        while flag_condition:
            try:
                text = input("")
                if text == "quit()":
                    print("--- GOODBYE ---")
                    self.client_exit(False)
                else:
                    message = f"{self.client_name}: {text}"
                    self.client_main.send(message.encode("ascii"))
            except OSError:
                # close connection if error occurs while
                # trying to send when server is closed
                print("SERVER NO LONGER RESPONDING...")
                self.client_main.close()
                self.client_exit(False)


if __name__ == "__main__":
    # help(ClientDefinition)
    client1 = ClientDefinition(HOST, PORT)

    try:
        client1.client_run()
    except (KeyboardInterrupt, SystemExit):
        exit()
