import requests
import allure
import pytest
from data.URL import url

class TestCreateOrder:

    @pytest.mark.parametrize('color', [
        ['BLACK'],
        ['GREY'],
        ['BLACK', 'GRAY'],
        []
    ])

    @allure.title('Создание заказа')
    def test_create_order(self, color):
        payload = {
            "firstName": "Tatyana",
            "lastName": "Archangel",
            "address": "Moscow, 11 apt.",
            "metroStation": 1,
            "phone": "+7 900 800 11 12",
            "rentTime": 3,
            "deliveryDate": "2025-10-25",
            "comment": "No comment",
            "color": color
        }

        response = requests.post(f"{url}/api/v1/orders", json=payload)

        assert response.status_code == 201, f"Ожидали 201, получили {response.status_code}"
        assert "track" in response.json(), "Ответ не содержит track"