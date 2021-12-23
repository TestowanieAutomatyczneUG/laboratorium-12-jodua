from src.MailServer import MailServer
from src.TemplateEngine import TemplateEngine


class Messenger:
    def __init__(self) -> None:
        self._template_engine = TemplateEngine()
        self._mail_server = MailServer()

    def send_message(self, to: str, message: str) -> str:
        if not isinstance(to, str):
            raise TypeError("Receiver must be string")
        if not isinstance(message, str):
            raise TypeError("Message must be string")
        try:
            generated_message = self._template_engine.generate(message)
            return self._mail_server.send_message(to, generated_message)
        except ConnectionError:
            # Do logging
            raise

    def receive_message(self, client: str) -> str:
        if not isinstance(client, str):
            raise TypeError("Client must be string")
        try:
            return self._mail_server.receive_message(client)
        except ConnectionError:
            # Do logging
            raise
