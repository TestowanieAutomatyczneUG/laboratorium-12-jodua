from typing import Callable


class DatabaseError(Exception):
    pass


class Subscriber:
    def __init__(self,
                 send_message: Callable[[str, str], str],
                 add_client: Callable[[str], bool],
                 remove_client: Callable[[str], bool]
                 ) -> None:
        self._clients = []
        self._send_message = send_message
        self._add_client = add_client
        self._remove_client = remove_client

    def add_client(self, client: str) -> str:
        if not isinstance(client, str):
            raise TypeError("Client must be string")
        if client in self._clients:
            raise ValueError("Client already exist")
        try:
            if self._add_client(client):
                self._clients.append(client)
                return client
            else:
                raise DatabaseError("Something went wrong in database")
        except ConnectionError:
            raise

    def remove_client(self, client: str) -> str:
        if not isinstance(client, str):
            raise TypeError("Client must be string")
        if client not in self._clients:
            raise ValueError("Client does not exist")
        try:
            if self._remove_client(client):
                self._clients.remove(client)
                return client
            else:
                raise DatabaseError("Something went wrong in database")
        except ConnectionError:
            raise

    def send_message(self, client: str, message: str) -> str:
        if not isinstance(client, str):
            raise TypeError("Client must be string")
        if not isinstance(message, str):
            raise TypeError("Message must be string")
        if client not in self._clients:
            raise ValueError("Client does not exist")
        try:
            return self._send_message(client, message)
        except ConnectionError:
            raise
