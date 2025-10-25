import requests
import allure
from data.URL import url

class TestGetListOfOrders:

    @allure.title('Получение списка заказов')
    def test_get_list_of_orders(self):
        payload = {
            "firstName": "Tatyana",
            "lastName": "Archangel",
            "address": "Moscow, 11 apt.",
            "metroStation": 1,
            "phone": "+7 900 800 11 12",
            "rentTime": 3,
            "deliveryDate": "2025-10-25",
            "comment": "No comment",
            "color": "BLACK"
        }
        requests.post(f"{url}/api/v1/orders", json=payload)
        response = requests.get(f"{url}/api/v1/orders")

        assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"
        assert "orders" in response.json(), "Ответ не содержит список заказов"