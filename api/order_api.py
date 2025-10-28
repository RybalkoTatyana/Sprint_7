import requests
from data.URL import url, create_order_endpoint


class OrderAPI:
    base_url = f"{url}{create_order_endpoint}"

    @staticmethod
    def create(payload):
        return requests.post(OrderAPI.base_url, json=payload)

    @staticmethod
    def get_list():
        return requests.get(OrderAPI.base_url)
