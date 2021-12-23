from unittest import TestCase
from unittest.mock import MagicMock
from assertpy import assert_that
from src.Messenger import Messenger


class TestMessenger(TestCase):
    def setUp(self) -> None:
        self.msngr = Messenger()

    def test_send_message(self) -> None:
        self.msngr._template_engine.generate = MagicMock(
            side_effect=lambda m: m)
        self.msngr._mail_server.send_message = MagicMock(
            side_effect=lambda c, m: f"{c}: {m}")
        result = self.msngr.send_message("Wojtek", "Hello")
        assert_that(result).is_equal_to("Wojtek: Hello")

    def test_send_message_invalid_to_type(self) -> None:
        assert_that(self.msngr.send_message).raises(
            TypeError).when_called_with(123, "message")

    def test_send_message_invalid_message_type(self) -> None:
        assert_that(self.msngr.send_message).raises(
            TypeError).when_called_with("to", 123)

    def test_send_message_connection_error(self) -> None:
        self.msngr._template_engine.generate = MagicMock(
            side_effect=lambda m: m)
        self.msngr._mail_server.send_message = MagicMock(
            side_effect=ConnectionError("Check mail server connection"))
        assert_that(self.msngr.send_message).raises(
            ConnectionError).when_called_with("client", "message")

    def test_send_message_template_engine_was_called(self) -> None:
        self.msngr._template_engine.generate = MagicMock(
            side_effect=lambda m: m)
        self.msngr._mail_server.send_message = MagicMock(
            side_effect=lambda c, m: f"{c}: {m}")
        self.msngr.send_message("Wojtek", "Hello")
        self.msngr._template_engine.generate.assert_called_once()

    def test_send_message_mail_server_was_called(self) -> None:
        self.msngr._template_engine.generate = MagicMock(
            side_effect=lambda m: m)
        self.msngr._mail_server.send_message = MagicMock(
            side_effect=lambda c, m: f"{c}: {m}")
        self.msngr.send_message("Wojtek", "Hello")
        self.msngr._mail_server.send_message.assert_called_once()

    def test_receive_message(self) -> None:
        self.msngr._mail_server.receive_message = MagicMock(
            return_value="Marek: Hi there")
        result = self.msngr.receive_message("Wojtek")
        assert_that(result).is_equal_to("Marek: Hi there")

    def test_receive_message_invalid_type(self) -> None:
        assert_that(self.msngr.receive_message).raises(
            TypeError).when_called_with(123)

    def test_receive_message_connection_error(self) -> None:
        self.msngr._mail_server.receive_message = MagicMock(
            side_effect=ConnectionError("Check mail server connection"))
        assert_that(self.msngr.receive_message).raises(
            ConnectionError).when_called_with("Wojtek")

    def test_receive_message_no_message(self) -> None:
        self.msngr._mail_server.receive_message = MagicMock(
            return_value=None)
        result = self.msngr.receive_message("Wojtek")
        assert_that(result).is_none()

    def test_receive_message_receive_message_was_called(self) -> None:
        self.msngr._mail_server.receive_message = MagicMock(
            return_value="Marek: test")
        result = self.msngr.receive_message("Wojtek")
        self.msngr._mail_server.receive_message.assert_called_once()

    def test_receive_message_receive_message_one_message(self) -> None:
        self.msngr._mail_server.receive_message = MagicMock(
            side_effect=["Marek: Hello", None])
        result = self.msngr.receive_message("Wojtek")
        result2 = self.msngr.receive_message("Wojtek")
        assert_that([result, result2]).contains("Marek: Hello", None)

    def tearDown(self) -> None:
        self.msngr = None
