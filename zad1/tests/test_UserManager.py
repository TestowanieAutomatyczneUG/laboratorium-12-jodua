from unittest import TestCase
from assertpy import assert_that
from src.UserManager import UserManager


class TestUserManager(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_um = UserManager()

    def test_get_data(self) -> None:
        result = self.temp_um._get_data()
        assert_that(result).is_not_none()

    def test_get_data_invalid_type(self) -> None:
        assert_that(self.temp_um._get_data).raises(
            TypeError).when_called_with(123)

    def test_get_user(self) -> None:
        result = self.temp_um.get_user()
        assert_that(len(result.get("results"))).is_equal_to(1)

    def test_get_n_users_not_none(self) -> None:
        result = self.temp_um.get_n_users(2)
        assert_that(result).is_not_none()

    def test_get_n_users_length(self) -> None:
        result = self.temp_um.get_n_users(2)
        assert_that(len(result.get("results"))).is_equal_to(2)

    def test_get_n_users_invalid_type(self) -> None:
        assert_that(self.temp_um.get_n_users).raises(
            TypeError).when_called_with("str")

    def test_get_n_users_invalid_value(self) -> None:
        assert_that(self.temp_um.get_n_users).raises(
            ValueError).when_called_with(-111)

    def test_get_user_by_gender_male(self) -> None:
        result = self.temp_um.get_user_by_gender("male")
        result_gender = result.get("results")[0].get("gender")
        assert_that(result_gender).is_equal_to("male")

    def test_get_user_by_gender_female(self) -> None:
        result = self.temp_um.get_user_by_gender("female")
        result_gender = result.get("results")[0].get("gender")
        assert_that(result_gender).is_equal_to("female")

    def test_get_user_by_gender_invalid_type(self) -> None:
        assert_that(self.temp_um.get_user_by_gender).raises(
            TypeError).when_called_with(123)

    def test_get_user_by_gender_invalid_value(self) -> None:
        assert_that(self.temp_um.get_user_by_gender).raises(
            ValueError).when_called_with("invalid")

    def test_get_user_by_nationality(self) -> None:
        result = self.temp_um.get_user_by_nationality("ca")
        result_nationality = result.get(
            "results")[0].get("location").get("country")
        assert_that(result_nationality).is_equal_to("Canada")

    def test_get_user_by_nationality_invalid_type(self) -> None:
        assert_that(self.temp_um.get_user_by_nationality).raises(
            TypeError).when_called_with(123)

    def test_get_user_by_nationality_invalid_value(self) -> None:
        assert_that(self.temp_um.get_user_by_nationality).raises(
            ValueError).when_called_with("pl")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_um = None
