from unittest import TestCase
from unittest.mock import MagicMock
from assertpy import assert_that
from src.Subscriber import Subscriber, DatabaseError


class TestSubscriber(TestCase):
    def setUp(self) -> None:
        self.temp_subscriber = Subscriber(None, None, None)

    def test_add_client(self) -> None:
        self.temp_subscriber._add_client = MagicMock(return_value=True)
        self.temp_subscriber.add_client("Wojtek")
        assert_that(self.temp_subscriber._clients).contains("Wojtek")

    def test_add_client_invalid_type(self) -> None:
        assert_that(self.temp_subscriber.add_client).raises(
            TypeError).when_called_with(123)

    def test_add_client_already_exist(self) -> None:
        self.temp_subscriber._clients = ["Wojtek"]
        assert_that(self.temp_subscriber.add_client).raises(
            ValueError).when_called_with("Wojtek")

    def test_add_client_database_error(self) -> None:
        self.temp_subscriber._add_client = MagicMock(return_value=False)
        assert_that(self.temp_subscriber.add_client).raises(
            DatabaseError).when_called_with("Wojtek")

    def test_add_client_connection_error(self) -> None:
        self.temp_subscriber._add_client = MagicMock(
            side_effect=ConnectionError)
        assert_that(self.temp_subscriber.add_client).raises(
            ConnectionError).when_called_with("Wojtek")

    def test_remove_client(self) -> None:
        self.temp_subscriber._clients = ["Patryk"]
        self.temp_subscriber._remove_client = MagicMock(return_value=True)
        self.temp_subscriber.remove_client("Patryk")
        assert_that(self.temp_subscriber._clients).is_equal_to([])

    def test_remove_client_invalid_type(self) -> None:
        assert_that(self.temp_subscriber.remove_client).raises(
            TypeError).when_called_with(123)

    def test_add_client_does_not_exist(self) -> None:
        assert_that(self.temp_subscriber.remove_client).raises(
            ValueError).when_called_with("Patryk")

    def test_remove_client_database_error(self) -> None:
        self.temp_subscriber._clients = ["Patryk"]
        self.temp_subscriber._remove_client = MagicMock(return_value=False)
        assert_that(self.temp_subscriber.remove_client).raises(
            DatabaseError).when_called_with("Patryk")

    def test_remove_client_connection_error(self) -> None:
        self.temp_subscriber._clients = ["Patryk"]
        self.temp_subscriber._remove_client = MagicMock(
            side_effect=ConnectionError)
        assert_that(self.temp_subscriber.remove_client).raises(
            ConnectionError).when_called_with("Patryk")

    def test_send_message(self) -> None:
        self.temp_subscriber._send_message = MagicMock(
            side_effect=lambda c, m: f"{c}: {m}")
        self.temp_subscriber._clients = ["Marcin"]
        result = self.temp_subscriber.send_message("Marcin", "Hello")
        assert_that(result).is_equal_to("Marcin: Hello")

    def test_send_message_invalid_client_type(self) -> None:
        assert_that(self.temp_subscriber.send_message).raises(
            TypeError).when_called_with(123, "message")

    def test_send_message_invalid_message_type(self) -> None:
        assert_that(self.temp_subscriber.send_message).raises(
            TypeError).when_called_with("client", 999)

    def test_send_message_client_does_not_exist(self) -> None:
        assert_that(self.temp_subscriber.send_message).raises(
            ValueError).when_called_with("client", "message")

    def test_send_message_connection_error(self) -> None:
        self.temp_subscriber._send_message = MagicMock(
            side_effect=ConnectionError)
        self.temp_subscriber._clients = "Marcin"
        assert_that(self.temp_subscriber.send_message).raises(
            ConnectionError).when_called_with("Marcin", "message")

    def tearDown(self) -> None:
        self.temp_subscriber = None
