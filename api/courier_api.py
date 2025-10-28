import requests
from data.URL import url, create_courier_endpoint


class CourierAPI:
    base_url = f"{url}{create_courier_endpoint}"

    @staticmethod
    def create(data):
        return requests.post(CourierAPI.base_url, data=data)

    @staticmethod
    def login(data):
        return requests.post(f"{CourierAPI.base_url}/login", data=data)

    @staticmethod
    def delete(courier_id):
        return requests.delete(f"{CourierAPI.base_url}/{courier_id}")
