import os

import requests
from assertpy import assert_that

BASE_URL = f"http://{os.environ['HOST']}:{os.environ['PORT']}"


class TestUserEndpoints:
    def test_create_user(self):
        username = "test_user"
        password = "test_password"

        response = requests.post(
            f"{BASE_URL}/users", json={"username": username, "password": password}
        )

        assert_that(response.json()).contains_only("id")
        assert_that(response.json()["id"]).matches(r"user_[2-9A-HJ-NP-Za-km-z]{22}")
