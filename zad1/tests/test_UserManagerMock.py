from unittest import TestCase
from unittest.mock import MagicMock, patch
from assertpy import assert_that
from src.UserManager import UserManager
import json


class TestUserManagerMock(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_um = UserManager()
        cls.user_male_ca = json.loads('{"gender":"male","name":{"title":"Mr","first":"Samuel","last":"Chan"},"location":{"street":{"number":8063,"name":"Bay Ave"},"city":"Waterloo","state":"Yukon","country":"Canada","postcode":"R7Q 9J4","coordinates":{"latitude":"29.3359","longitude":"-165.1886"},"timezone":{"offset":"+5:30","description":"Bombay, Calcutta, Madras, New Delhi"}},"email":"samuel.chan@example.com","login":{"uuid":"d2bc3ff6-8603-4df5-bf54-52bc51804056","username":"goldenfish433","password":"xiao","salt":"HAcm18uR","md5":"2cb75929e3ee28405c37fdafa401f9bb","sha1":"fd5061861c7712e42eddb3419237430d896b8f69","sha256":"550810b449f82be91a72ee4442ff7eac2c7a0fe23b79d0533f0a3d539a4a2c15"},"dob":{"date":"1954-03-19T18:38:22.184Z","age":67},"registered":{"date":"2015-04-21T08:02:42.360Z","age":6},"phone":"305-030-3301","cell":"800-670-1435","id":{"name":"","value":null},"picture":{"large":"https://randomuser.me/api/portraits/men/79.jpg","medium":"https://randomuser.me/api/portraits/med/men/79.jpg","thumbnail":"https://randomuser.me/api/portraits/thumb/men/79.jpg"},"nat":"CA"}')
        cls.user_female = {"gender": "female"}

    def test_get_data(self) -> None:
        with patch.object(UserManager, '_get_data', MagicMock(return_value={"results": [self.user_male_ca]})) as get_data_mock:
            result = self.temp_um._get_data()
        assert_that(result).is_not_none()

    def test_get_data_invalid_type(self) -> None:
        assert_that(self.temp_um._get_data).raises(
            TypeError).when_called_with(123)

    def test_get_user(self) -> None:
        with patch.object(UserManager, '_get_data', MagicMock(return_value={"results": [self.user_male_ca]})) as get_data_mock:
            result = self.temp_um.get_user()
        assert_that(len(result.get("results"))).is_equal_to(1)

    def test_get_n_users_not_none(self) -> None:
        with patch.object(UserManager, '_get_data', MagicMock(return_value={"results": [self.user_male_ca, self.user_male_ca]})) as get_data_mock:
            result = self.temp_um.get_n_users(2)
        assert_that(result).is_not_none()

    def test_get_n_users_length(self) -> None:
        with patch.object(UserManager, '_get_data', MagicMock(return_value={"results": [self.user_male_ca, self.user_male_ca]})) as get_data_mock:
            result = self.temp_um.get_n_users(2)
        assert_that(len(result.get("results"))).is_equal_to(2)

    def test_get_n_users_invalid_type(self) -> None:
        assert_that(self.temp_um.get_n_users).raises(
            TypeError).when_called_with("str")

    def test_get_n_users_invalid_value(self) -> None:
        assert_that(self.temp_um.get_n_users).raises(
            ValueError).when_called_with(-111)

    def test_get_user_by_gender_male(self) -> None:
        with patch.object(UserManager, '_get_data', MagicMock(return_value={"results": [self.user_male_ca]})) as get_data_mock:
            result = self.temp_um.get_user_by_gender("male")
            result_gender = result.get("results")[0].get("gender")
        assert_that(result_gender).is_equal_to("male")

    def test_get_user_by_gender_female(self) -> None:
        with patch.object(UserManager, '_get_data', MagicMock(return_value={"results": [self.user_female]})) as get_data_mock:
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
        with patch.object(UserManager, '_get_data', MagicMock(return_value={"results": [self.user_male_ca]})) as get_data_mock:
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
