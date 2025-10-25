import requests
import allure
import pytest
import logging
from data.URL import url
from data.courier_data import generation_new_data_courier, register_new_courier_and_return_login_password


@pytest.fixture
def registered_courier_data():
    login, password, first_name = register_new_courier_and_return_login_password()
    return {
        "login": login, 
        "password": password, 
        "firstName": first_name
        }


class TestCreateCourier:

    @allure.title('Создание курьера')
    @allure.step('Проверка создания курьера (201, ok=True)')
    def test_create_courier(self):
        data = generation_new_data_courier()
        data.pop("firstName")
        payload = data
        logging.info(f"Data for courier creation: {data}")

        #создание курьера
        response = requests.post(f"{url}/api/v1/courier", data=payload)
        assert response.status_code == 201, f"Ожидали 201, получили {response.status_code}"
        assert response.json() == {"ok": True}, "Неверное содержимое ответа при создании курьера."

        # Проверка авторизации
        login_response = requests.post(f"{url}/api/v1/courier/login", data={"login": payload["login"], "password": payload["password"]})
        assert login_response.status_code == 200, "Login failed."
        courier_id = login_response.json().get("id")
        assert courier_id, "Courier ID not found in login response."
        
        # Удаляем тестового курьера
        delete_response = requests.delete(f"{url}/api/v1/courier/{courier_id}")
        assert delete_response.status_code == 200, "Failed to delete courier."


    @allure.title("Невозможно создать курьера с уже существующими логином и паролем")
    def test_create_courier_duplicate_login(self, registered_courier_data):
        response = requests.post(f"{url}/api/v1/courier", data=registered_courier_data)

        assert response.status_code == 409, f"Ожидали 409, получили {response.status_code}"
        assert response.json() == {
            "code": 409,
            "message": "Этот логин уже используется. Попробуйте другой."
        }, "Неверное содержимое ответа при создании дубликата."


    @allure.title("Невозможно создать курьера без обязательных полей")
    def test_create_courier_without_password(self):
        data = generation_new_data_courier()
        payload = {"login": data["login"], "firstName": data["firstName"]}

        response = requests.post(f"{url}/api/v1/courier", data=payload)

        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}"
        assert response.json() == {
            "code": 400,
            "message": "Недостаточно данных для создания учетной записи"
        }, "Неверное содержимое ответа при неполных данных."