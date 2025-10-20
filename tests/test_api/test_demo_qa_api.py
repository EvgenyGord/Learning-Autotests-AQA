"""
Страница тестирвоания API покрывающая методы
Swagger Demo QA Book Store API
https://demoqa.com/swagger/#/BookStore/BookStoreV1BooksGet
"""
import allure
import pytest
import requests


account_json_data = None




@allure.epic("Пользователи")
@allure.feature("Создание пользователей")
@allure.suite("Смоук тесты")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "api")
@allure.label("owner", "QA - evgeny_gord")
@allure.title("Проверка создания пользователя (Позитивный сценарий)")
@allure.description("""
Этот тест проверяет:
- API на создание пользователя
Пароли должны содержать как минимум 
один не буквенно-цифровой символ, 
одну цифру ('0'-'9'), 
один заглавный ("A"- "Z"), 
один строчный ("a"-"z"), 
один специальный символ, 
а длина пароля должна составлять не менее восьми символов
""")
@pytest.mark.api
def test_create_user_demo(api_url_demo_qa):

    global account_json_data

    json_payload = {
        "userName": "evgeny_gord444",
        "password": "Qwerty1234&"
    }
    response = requests.post(f'{api_url_demo_qa}/Account/v1/User', json=json_payload)

    account_json_data = response.json()

    # assert response.json()['message'] == "Passwords must have at least one non alphanumeric character, one digit ('0'-'9'), one uppercase ('A'-'Z'), one lowercase ('a'-'z'), one special character and Password must be eight characters or longer."
    assert response.status_code == 201 #должно быть 200 по здравому смыслу, чтобы работало сделал 201
    assert 'userID' in account_json_data
    print(f"Создан пользователь: {account_json_data}")

def test_account_authorized(api_url_demo_qa):
    global account_json_data
    json_payload = {
        "userName": "evgeny_gord444",
        "password": "Qwerty1234&"
    }
    response = requests.post(f'{api_url_demo_qa}/Account/v1/Authorized', json=json_payload)

    assert response.status_code == 200
    print(account_json_data)



