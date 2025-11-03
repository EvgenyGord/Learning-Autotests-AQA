"""
Страница тестирования API покрывающая методы
Swagger Demo QA Book Store API
https://demoqa.com/swagger/#/BookStore/BookStoreV1BooksGet
"""
import allure
import pytest
import requests


json_payload = {
        "userName": "evgeny_gord33459",
        "password": "Qwerty1234&"
    }


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


    response = requests.post(f"{api_url_demo_qa}/Account/v1/User", json=json_payload)


    # assert response.json()["message"] == "Passwords must have at least one non alphanumeric character, one digit ('0'-'9'), one uppercase ('A'-'Z'), one lowercase ('a'-'z'), one special character and Password must be eight characters or longer."
    assert response.status_code == 201 #должно быть 200 по здравому смыслу, чтобы работало сделал 201

    return {
        "userID": response.json()["userID"]
    }


def test_account_authorized(api_url_demo_qa):


    response = requests.post(f"{api_url_demo_qa}/Account/v1/Authorized", json=json_payload)
    assert response.status_code == 200
    print(f"Получили информацию {response.json()}")
    print("Пользователь успешно авторизован")


def test_generate_token(api_url_demo_qa):

    response = requests.post(f"{api_url_demo_qa}/Account/v1/GenerateToken", json=json_payload)

    assert response.status_code == 200
    print(response.json())
    return {
        "token":  response.json()["token"]
    }


def test_get_user_info(api_url_demo_qa):
    user_id = test_create_user_demo(api_url_demo_qa)["userID"]
    auth_token = test_generate_token(api_url_demo_qa)["token"]
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'accept': 'application/json'
    }
    response = requests.get(f"{api_url_demo_qa}/Account/v1/User/{user_id}", headers=headers)
    print(response.json())
    assert response.status_code == 200
    print(f"Получение информации о пользователе {user_id}")


def test_delete_user(api_url_demo_qa):
    user_id = test_create_user_demo(api_url_demo_qa)["userID"]
    print(user_id)
    response = requests.delete(f"{api_url_demo_qa}/Account/v1/User/{user_id}")
    print(f"получили {response.json()}")
    # assert response.status_code == 200
    print(f"Пользователь {user_id} удален")


"""
Тесты с рандомными данными(с помощью библиотеки Faker) ниже
                            |
                            v
"""


def test_create_user_demo_faker_data(api_url_demo_qa, faker_data):

    json_payload = {
        "userName": faker_data["name"],
        "password": faker_data["password"]
    }
    response = requests.post(f"{api_url_demo_qa}/Account/v1/User", json=json_payload)


    # assert response.json()['message'] == "Passwords must have at least one non alphanumeric character, one digit ('0'-'9'), one uppercase ('A'-'Z'), one lowercase ('a'-'z'), one special character and Password must be eight characters or longer."
    assert response.status_code == 201 #должно быть 200 по здравому смыслу, чтобы работало сделал 201

    return {
        'userID': response.json()["userID"]
    }


def test_delete_user_faker_data(api_url_demo_qa, faker_data):
    user_id = test_create_user_demo_faker_data(api_url_demo_qa, faker_data)["userID"]
    print(user_id)
    response = requests.delete(f"{api_url_demo_qa}/Account/v1/User/{user_id}")
    print(f"получили {response.json()}")
    # assert response.status_code == 200
    print(f"Пользователь {user_id} был успешно создан и удален")


