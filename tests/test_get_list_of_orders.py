import allure
from api.order_api import OrderAPI
from data.order_data import default_order_payload


class TestGetListOfOrders:

    @allure.title('Получение списка заказов')
    def test_get_list_of_orders(self):
        payload = default_order_payload(color="BLACK")
        OrderAPI.create(payload)
        response = OrderAPI.get_list()

        assert response.status_code == 200
        assert "orders" in response.json()
