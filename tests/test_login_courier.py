import requests
import pytest
import allure
from data.URL import url
from data.courier_data import register_new_courier_and_return_login_password


@pytest.fixture
def courier_data():
    #Создаёт курьера и удаляет его после теста.
    login, password, _ = register_new_courier_and_return_login_password()
    credentials = {"login": login, "password": password}

    yield credentials

    response = requests.post(f"{url}/api/v1/courier/login", data=credentials)
    if response.status_code == 200:
        courier_id = response.json().get("id")
        if courier_id:
            requests.delete(f"{url}/api/v1/courier/{courier_id}")


class TestLoginCourier:

    @allure.title("Авторизация курьера с корректными данными")
    def test_login_success(self, courier_data):
        response = requests.post(f"{url}/api/v1/courier/login", data=courier_data)
        assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"
        assert "id" in response.json(), "Ответ не содержит ID курьера."

    @allure.title("Авторизация неуспешна при неверном пароле")
    def test_login_invalid_password(self):
        login, _, _ = register_new_courier_and_return_login_password()
        payload = {"login": login, "password": "wrongpass"}

        response = requests.post(f"{url}/api/v1/courier/login", data=payload)
        assert response.status_code == 404, f"Ожидали 404, получили {response.status_code}"
        assert response.json() == {
            "code": 404,
            "message": "Учетная запись не найдена"
        }, "Неверное содержимое ответа при неверном пароле."

    @allure.title("Авторизация неуспешна без обязательного поля password")
    def test_login_without_password(self):
        login, _, _ = register_new_courier_and_return_login_password()
        payload = {"login": login, "password": ""}

        response = requests.post(f"{url}/api/v1/courier/login", data=payload)
        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}"
        assert response.json() == {
            "code": 400,
            "message": "Недостаточно данных для входа"
        }, "Неверное содержимое ответа при отсутствии пароля."

    @allure.title("Авторизация неуспешна без обязательного поля login")
    def test_login_without_login(self):
        _, password, _ = register_new_courier_and_return_login_password()
        payload = {"login": "", "password": password}

        response = requests.post(f"{url}/api/v1/courier/login", data=payload)
        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}"
        assert response.json() == {
            "code": 400,
            "message": "Недостаточно данных для входа"
        }, "Неверное содержимое ответа при отсутствии логина."

    @allure.title("Авторизация неуспешна под несуществующим пользователем")
    def test_login_nonexistent_user(self):
        payload = {"login": "nonexistent_user_123", "password": "randompass"}
        response = requests.post(f"{url}/api/v1/courier/login", data=payload)

        assert response.status_code == 404, f"Ожидали 404, получили {response.status_code}"
        assert response.json() == {
            "code": 404,
            "message": "Учетная запись не найдена"
        }, "Неверное содержимое ответа при несуществующем пользователе."