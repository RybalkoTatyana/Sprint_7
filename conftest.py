import pytest
from api.courier_api import CourierAPI
from data.courier_data import generation_new_data_courier, register_new_courier_and_return_login_password


@pytest.fixture
def courier_data():
    #создаем нового курьера
    data = generation_new_data_courier()
    payload = {
        "login": data["login"], 
        "password": data["password"], 
        "firstName": data["firstName"]
    }

    yield payload

    #после теста удаляю курьера
    response = CourierAPI.login(payload)
    courier_id = response.json().get("id") if response.status_code == 200 else None
    if courier_id:
        CourierAPI.delete(courier_id)


@pytest.fixture
def registered_courier_data():
    #создаем нового курьера на сервере
    login, password, firstName = register_new_courier_and_return_login_password()
    payload = {
        "login": login, 
        "password": password, 
        "firstName": firstName
    }

    # регистрация на сервере
    CourierAPI.create(payload)
    yield payload

    #после теста удаляю курьера
    response = CourierAPI.login(payload)
    courier_id = response.json().get("id") if response.status_code == 200 else None
    if courier_id:
        CourierAPI.delete(courier_id)
