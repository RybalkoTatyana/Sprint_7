import allure
import pytest
from api.order_api import OrderAPI
from data.order_data import default_order_payload


class TestCreateOrder:

    @pytest.mark.parametrize('color', [
        ['BLACK'],
        ['GREY'],
        ['BLACK', 'GRAY'],
        []
    ])
    @allure.title('Создание заказа')
    def test_create_order(self, color):
        payload = default_order_payload(color=color)
        response = OrderAPI.create(payload)

        assert response.status_code == 201
        assert "track" in response.json()
