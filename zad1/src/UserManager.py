import requests


class UserManager:
    def __init__(self) -> None:
        self._url = "https://randomuser.me/api/?noinfo"
        self._nationalities = ['AU', 'BR', 'CA', 'CH', 'DE', 'DK', 'ES',
                               'FI', 'FR', 'GB', 'IE', 'IR', 'NO', 'NL', 'NZ', 'TR', 'US']
        self._genders = ["male", "female"]

    def _get_data(self, params: str = "") -> dict:
        if not isinstance(params, str):
            raise TypeError("Params must be string")
        api_request = requests.get(f"{self._url}{params}")
        if not api_request.ok:
            raise ConnectionError("Something went wrong")
        return api_request.json()

    def get_user(self) -> dict:
        return self._get_data()

    def get_n_users(self, amount: int) -> dict:
        if not isinstance(amount, int):
            raise TypeError("Amount must be integer")
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        return self._get_data(f"&results={amount}")

    def get_user_by_gender(self, gender: str) -> dict:
        if not isinstance(gender, str):
            raise TypeError("Gener must be string")
        if gender not in self._genders:
            raise ValueError("Invalid gender")
        return self._get_data(f"&gender={gender}")

    def get_user_by_nationality(self, nationality: str) -> dict:
        if not isinstance(nationality, str):
            raise TypeError("Nationality must be string")
        if nationality.upper() not in self._nationalities:
            raise ValueError("Invalid nationality")
        return self._get_data(f"&nationality={nationality}")
