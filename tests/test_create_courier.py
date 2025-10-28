import allure
from api.courier_api import CourierAPI
from data.courier_data import generation_new_data_courier


class TestCreateCourier:

    @allure.title("Создание курьера (201, ok=True)")
    def test_create_courier(self, courier_data):
        response = CourierAPI.create(courier_data)
        assert response.status_code == 201, f"Ожидали 201, получили {response.status_code}"
        assert response.json() == {"ok": True}, "Неверное содержимое ответа при создании курьера."

    @allure.title("Невозможно создать курьера с уже существующими логином и паролем")
    def test_create_courier_duplicate_login(self, registered_courier_data):
        response = CourierAPI.create(registered_courier_data)
        assert response.status_code == 409, f"Ожидали 409, получили {response.status_code}"
        assert response.json() == {
            "code": 409,
            "message": "Этот логин уже используется. Попробуйте другой."
        }, "Неверное содержимое ответа при создании дубликата."

    @allure.title("Невозможно создать курьера без обязательных полей")
    def test_create_courier_without_password(self):
        data = generation_new_data_courier()
        payload = {"login": data["login"], "firstName": data["firstName"]}
        response = CourierAPI.create(payload)
        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}"
        assert response.json() == {
            "code": 400,
            "message": "Недостаточно данных для создания учетной записи"
        }, "Неверное содержимое ответа при неполных данных."
