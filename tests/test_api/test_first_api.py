"""
Страница тестирвоания API покрывающая методы
Swagger Petstore
https://petstore.swagger.io/
"""
import allure
import pytest
import requests

#@pytest.mark.xfail
@allure.epic("Пользователи")
@allure.feature("Создание пользователей")
@allure.suite("Смоук тесты")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "api")
@allure.label("owner", "QA - evgeny_gord")
@allure.title("Проверка создания пользователя")
@allure.description("""
Этот тест проверяет:
- API на создание пользователя
""")
@pytest.mark.api
def test_create_user(api_url_petstore):
    payload_json = {
        "id": 0,
        "username": "evgeny_gord",
        "firstName": "evgeny",
        "lastName": "gordenko",
        "email": "jeka21.02.81@mail.ru",
        "password": "qwerty1234",
        "phone": "+79999999999",
        "userStatus": 200
    }
    response = requests.post(f"{api_url_petstore}/user", json=payload_json)

    assert response.status_code == 200
    print(response.json())


@allure.epic("Пользователи")
@allure.feature("Авторизация")
@allure.suite("Смоук тесты")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "api")
@allure.label("owner", "QA - evgeny_gord")
@allure.title("Проверка авторизации пользователя")
@allure.description("""
Этот тест проверяет:
- API на авторизацию пользователя
""")
@pytest.mark.api
def test_login_user(api_url_petstore):
    query_params = {
        "username": "evgeny_gord",
        "password": "qwerty1234"
    }

    response = requests.get(f"{api_url_petstore}/user/login", params=query_params)

    assert response.status_code == 200
    print(response.json())

@allure.epic("Пользователи")
@allure.feature("Авторизация")
@allure.suite("Смоук тесты")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "api")
@allure.label("owner", "QA - evgeny_gord")
@allure.title("Проверка выхода пользователя из системы")
@allure.description("""
Этот тест проверяет:
- API на выход из системы
""")
@pytest.mark.api
def test_logout_user(api_url_petstore):
    response = requests.get(f"{api_url_petstore}/user/logout")
    assert response.status_code == 200
    print(response.json())










# pytest -v -k test_name --alluredir=allure-results --clean-alluredir
# allure generate allure-results -o allure-report --clean
# allure open allure-report
# pytest -v test_first.py::test_positive_registration --alluredir=allure-results --clean-alluredir